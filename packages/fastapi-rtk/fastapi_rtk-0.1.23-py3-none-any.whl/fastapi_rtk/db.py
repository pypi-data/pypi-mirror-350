import asyncio
import collections
import contextlib
import typing
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Literal,
    Optional,
    TypedDict,
    overload,
)

from fastapi import Depends, HTTPException
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import ID, OAP, UP
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import (
    Column,
    Connection,
    Engine,
    MetaData,
    Select,
    create_engine,
    func,
    select,
)
from sqlalchemy import Table as SA_Table
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    Session,
    defer,
    joinedload,
    load_only,
    scoped_session,
    selectinload,
    sessionmaker,
)
from sqlalchemy.orm.strategy_options import _AbstractLoad

from .const import FASTAPI_RTK_TABLES, logger
from .filters import BaseFilter, FilterGlobal
from .model import Table, metadata, metadatas
from .models import Model, OAuthAccount, User
from .schemas import PRIMARY_KEY, FilterSchema
from .utils import T, deep_merge, prettify_dict, safe_call, smart_run

if TYPE_CHECKING:
    from .api import SQLAInterface


__all__ = [
    "UserDatabase",
    "QueryManager",
    "db",
    "get_session",
    "get_user_db",
]

LOAD_TYPE_MAPPING = {
    "defer": 0,
    "some": 1,
    "all": 2,
}


class LoadColumn(TypedDict):
    stmt: Select[T] | _AbstractLoad
    type: typing.Literal["defer", "some", "all"]
    columns: list[str]
    related_columns: collections.defaultdict[str, "LoadColumn"]


def create_load_column(stmt: Select[T] | _AbstractLoad | None = None):
    return LoadColumn(
        stmt=stmt,
        type="defer",
        columns=[],
        related_columns=collections.defaultdict(create_load_column),
    )


class DBExecuteParams(TypedDict):
    list_columns: list[str] | None
    join_columns: list[str] | None
    page: int | None
    page_size: int | None
    order_column: str | None
    order_direction: str | None
    where: tuple[str, Any] | list[tuple[str, Any]] | None
    where_in: tuple[str, list[Any]] | None
    where_id: PRIMARY_KEY | None
    where_id_in: list[PRIMARY_KEY] | None
    filters: list[FilterSchema] | None
    filter_classes: list[tuple[str, BaseFilter, Any]] | None
    global_filter: str | None


class UserDatabase(SQLAlchemyUserDatabase):
    """
    Modified version of the SQLAlchemyUserDatabase class from fastapi_users_db_sqlalchemy.
    - Allow the use of both async and sync database connections.
    - Allow the use of get_by_username method to get a user by username.

    Database adapter for SQLAlchemy.

    :param session: SQLAlchemy session instance.
    :param user_table: SQLAlchemy user model.
    :param oauth_account_table: Optional SQLAlchemy OAuth accounts model.
    """

    session: AsyncSession | Session

    def __init__(
        self,
        session: AsyncSession | Session,
        user_table: type,
        oauth_account_table: type[SQLAlchemyBaseOAuthAccountTable] | None = None,
    ):
        super().__init__(session, user_table, oauth_account_table)

    async def get(self, id: ID) -> Optional[UP]:
        statement = select(self.user_table).where(self.user_table.id == id)
        return await self._get_user(statement)

    async def get_by_email(self, email: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.email) == func.lower(email)
        )
        return await self._get_user(statement)

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[UP]:
        if self.oauth_account_table is None:
            raise NotImplementedError()

        statement = (
            select(self.user_table)
            .join(self.oauth_account_table)
            .where(self.oauth_account_table.oauth_name == oauth)
            .where(self.oauth_account_table.account_id == account_id)
        )
        return await self._get_user(statement)

    async def create(self, create_dict: Dict[str, Any]) -> UP:
        user = self.user_table(**create_dict)
        self.session.add(user)
        await safe_call(self.session.commit())
        await safe_call(self.session.refresh(user))
        return user

    async def update(self, user: UP, update_dict: Dict[str, Any]) -> UP:
        for key, value in update_dict.items():
            setattr(user, key, value)
        self.session.add(user)
        await safe_call(self.session.commit())
        await safe_call(self.session.refresh(user))
        return user

    async def delete(self, user: UP) -> None:
        await self.session.delete(user)
        await safe_call(self.session.commit())

    async def add_oauth_account(self, user: UP, create_dict: Dict[str, Any]) -> UP:
        if self.oauth_account_table is None:
            raise NotImplementedError()

        await safe_call(self.session.refresh(user))
        oauth_account = self.oauth_account_table(**create_dict)
        self.session.add(oauth_account)
        user.oauth_accounts.append(oauth_account)
        self.session.add(user)

        await safe_call(self.session.commit())

        return user

    async def update_oauth_account(
        self, user: UP, oauth_account: OAP, update_dict: Dict[str, Any]
    ) -> UP:
        if self.oauth_account_table is None:
            raise NotImplementedError()

        for key, value in update_dict.items():
            setattr(oauth_account, key, value)
        self.session.add(oauth_account)
        await safe_call(self.session.commit())

        return user

    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return await self._get_user(statement)

    async def _get_user(self, statement: Select) -> Optional[UP]:
        results = await smart_run(self.session.execute, statement)
        return results.unique().scalar_one_or_none()


class QueryManager:
    """
    A class that manages the execution of queries on a database.
    """

    datamodel: "SQLAInterface"
    _load_options_cache: dict[str, list[list[_AbstractLoad] | _AbstractLoad]] = {}

    def __init__(
        self,
        datamodel: "SQLAInterface",
        select_cols: list[str] | None = None,
    ):
        self.datamodel = datamodel
        if select_cols:
            #! DEPRECATED
            logger.warning(
                "The select_cols parameter is deprecated in QueryManager and will be removed in the future."
            )

    def join(self, columns: str | list[str]):
        """
        Joins a column in the query.

        Args:
            columns (str | list[str]): The column or columns to join.

        Returns:
            dict[str, tuple[Callable, list[Column]]]: A dictionary containing the columns to join.
        """
        logger.warning(
            "The `join` method is deprecated and will be removed in the future. Use the `load_columns` method instead."
        )
        option_cols: dict[str, tuple[_AbstractLoad, list[Column]]] = {}
        if not isinstance(columns, list):
            columns = [columns]

        for col_str in columns:
            col = getattr(self.datamodel.obj, col_str)
            if self.datamodel.is_relation_one_to_one(
                col
            ) or self.datamodel.is_relation_many_to_one(col):
                if not option_cols.get(col_str):
                    option_cols[col_str] = (joinedload(col), [])
            else:
                if not option_cols.get(col_str):
                    option_cols[col_str] = (selectinload(col), [])

            if "." in col_str:
                sub_col = col_str.split(".")[1]
                option_cols[col_str][1].append(getattr(col, sub_col))

        return option_cols

    def load_columns(self, stmt: Select[T] | _AbstractLoad, columns: list[str]):
        """
        Load specified columns into the given SQLAlchemy statement.
        This method processes the provided list of columns, orders them, and
        determines the appropriate loading strategy for each column. It supports
        loading both direct columns and related columns (one-to-one, many-to-one,
        and select-in relationships). The method also handles nested column
        relationships by recursively calling itself.

        Args:
            stmt (Select[T] | _AbstractLoad): The SQLAlchemy statement to which the
                columns will be loaded.
            columns (list[str]): A list of column names to be loaded.

        Returns:
            The modified SQLAlchemy statement with the specified columns loaded.
        """
        # Order the columns first, so that related columns are loaded before their sub-columns
        columns = sorted(columns)

        # Check if the columns have been loaded before
        cache_key = f"{self.datamodel.obj.__name__}-{columns}"
        if cache_key in self._load_options_cache:
            logger.debug(f"Loading columns from cache: {cache_key}")
            for cache_option in self._load_options_cache[cache_key]:
                if isinstance(cache_option, list):
                    stmt = stmt.options(*cache_option)
                else:
                    stmt = stmt.options(cache_option)
            return stmt

        load_column = self._load_columns_recursively(stmt, columns)
        logger.debug(f"Load Column:\n{prettify_dict(load_column)}")
        return self._load_columns_from_dictionary(stmt, load_column, columns)

    def page(self, stmt: Select, page: int, page_size: int):
        """
        Paginates the query results.

        Args:
            stmt (Select): The query statement.
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            Select: The paginated query.
        """
        return stmt.offset(page * page_size).limit(page_size)

    def order_by(self, stmt: Select, column: str, direction: str):
        """
        Orders the query results by a specific column.

        Args:
            stmt (Select): The query statement.
            column (str): The column to order by.
            direction (str): The direction of the ordering.

        Returns:
            Select: The ordered query.
        """
        col = column

        #! If the order column comes from a request, it will be in the format ClassName.column_name
        if col.startswith(self.datamodel.obj.__class__.__name__):
            col = col.split(".", 1)[1]

        # If the column is a relation, get the related interface and add the primary key of the related table
        if self.datamodel.is_relation(col):
            rel_interface = self.datamodel.get_related_interface(col)
            col += f".{rel_interface.get_pk_attr()}"

        # if there is . in the column name, it means it is a relation column
        if "." in col:
            stmt, col = self._join_column(stmt, col)
        else:
            col = getattr(self.datamodel.obj, col)
        if direction == "asc":
            stmt = stmt.order_by(col)
        else:
            stmt = stmt.order_by(col.desc())
        return stmt

    def where(self, stmt: Select, column: str, value: Any):
        """
        Apply a WHERE clause to the query.

        Args:
            stmt (Select): The query statement.
            column (str): The column name to apply the WHERE clause on.
            value (Any): The value to compare against in the WHERE clause.

        Returns:
            Select: The query with the WHERE clause applied.
        """
        column = getattr(self.datamodel.obj, column)
        return stmt.where(column == value)

    def where_in(self, stmt: Select, column: str, values: list[Any]):
        """
        Apply a WHERE IN clause to the query.

        Args:
            stmt (Select): The query statement.
            column (str): The column name to apply the WHERE IN clause on.
            values (list[Any]): The list of values to compare against in the WHERE IN clause.

        Returns:
            Select: The query with the WHERE IN clause applied.
        """
        column = getattr(self.datamodel.obj, column)
        return stmt.where(column.in_(values))

    def where_id(self, stmt: Select, id: PRIMARY_KEY):
        """
        Adds a WHERE clause to the query based on the primary key.

        Args:
            stmt (Select): The query statement.
            id (PRIMARY_KEY): The primary key value to filter by.

        Returns:
            Select: The query with the WHERE clause applied.
        """
        pk_dict = self._convert_id_into_dict(id)
        for col, val in pk_dict.items():
            stmt = self.where(stmt, col, val)
        return stmt

    def where_id_in(self, stmt: Select, ids: list[PRIMARY_KEY]):
        """
        Filters the query by a list of primary key values.

        Args:
            stmt (Select): The query statement.
            ids (list): A list of primary key values.

        Returns:
            None
        """
        to_apply_dict = {}
        for id in self.datamodel.get_pk_attrs():
            to_apply_dict[id] = []

        pk_dicts = [self._convert_id_into_dict(id) for id in ids]
        for pk_dict in pk_dicts:
            for col, val in pk_dict.items():
                to_apply_dict[col].append(val)

        for col, vals in to_apply_dict.items():
            stmt = self.where_in(stmt, col, vals)
        return stmt

    async def filter(self, stmt: Select, filter: FilterSchema):
        """
        Apply a filter to the query.

        Args:
            stmt (Select): The query statement.
            filter (FilterSchema): The filter to apply to the query.
        """
        col = filter.col
        if "." in col:
            col, rel_col = col.split(".", 1)
            rel_interface = self.datamodel.get_related_interface(col)
            rel_interface.filters[rel_col].extend(
                self.datamodel.filters.get(filter.col, [])
            )
            rel_interface.filters[rel_col] = [
                f
                for f in rel_interface.filters[rel_col]
                if f.arg_name not in self.datamodel.exclude_filters.get(filter.col, [])
            ]
            filter_classes = rel_interface.filters.get(rel_col, [])
        else:
            filter_classes = self.datamodel.filters.get(col, [])
        filter_class = None
        for f in filter_classes:
            if f.arg_name == filter.opr:
                filter_class = f
                break
        if not filter_class:
            raise HTTPException(
                status_code=400, detail=f"Invalid filter opr: {filter.opr}"
            )

        if "." in filter.col:
            return await self._handle_relation_filter(
                stmt, filter.col, filter_class, filter.value
            )

        return await self._apply_filter(filter_class, stmt, filter.col, filter.value)

    async def filter_class(
        self, stmt: Select, col: str, filter_class: BaseFilter, value: Any
    ):
        """
        Apply a filter class to the query.

        Args:
            col (str): The column to apply the filter class on.
            filter_class (BaseFilter): The filter class to apply to the query.
            value (Any): The value to compare against in the filter class.
        """
        # If there is . in the column name, it means it should filter on a related table
        if "." in col:
            return await self._handle_relation_filter(stmt, col, filter_class, value)

        return await self._apply_filter(filter_class, stmt, col, value)

    def add(self, session: Session | AsyncSession, item: Model):
        """
        Add an item to the query.

        Args:
            session (Session | AsyncSession): The session to use for the query.
            item (Model): The item to add to the query.
        """
        session.add(item)

    async def delete(self, session: Session | AsyncSession, item: Model):
        """
        Delete an item from the query.

        Args:
            session (Session | AsyncSession): The session to use for the query.
            item (Model): The item to delete from the query.
        """
        await safe_call(session.delete(item))

    async def commit(self, session: Session | AsyncSession):
        """
        Commits the current transaction to the database.

        Args:
            session (Session | AsyncSession): The session to commit.

        Returns:
            None
        """
        await safe_call(session.commit())

    async def flush(
        self, session: Session | AsyncSession, items: list[Model] | None = None
    ):
        """
        Flushes the current transaction to the database.

        Args:
            session (Session | AsyncSession): The session to flush.
            items (list[Model] | None): The list of items to flush. Defaults to None.

        Returns:
            None
        """
        await safe_call(session.flush(items))

    async def refresh(self, session: Session | AsyncSession, item: Model):
        """
        Refreshes the given item in the database.

        Args:
            session (Session | AsyncSession): The session to use for the query.
            item (Model): The item to refresh in the database.
        """
        await safe_call(session.refresh(item))

    async def count(
        self,
        session: AsyncSession | Session,
        filters: list[FilterSchema] | None = None,
        filter_classes: list[tuple[str, BaseFilter, Any]] | None = None,
    ) -> int:
        """
        Counts the number of records in the database table.

        Args:
            session (AsyncSession | Session): The session to use for the query.
            filters (list[FilterSchema], optional): The list of filters to apply to the query. Defaults to [].
            filter_classes (list[tuple[str, BaseFilter, Any]], optional): The list of filter classes to apply to the query. Defaults to [].

        Returns:
            int: The number of records in the table.
        """
        stmt = select(func.count()).select_from(self.datamodel.obj)

        if filters:
            for filter in filters:
                stmt = await safe_call(self.filter(stmt, filter))
        if filter_classes:
            for col, filter_class, value in filter_classes:
                stmt = await safe_call(
                    self.filter_class(stmt, col, filter_class, value)
                )
        result = await smart_run(session.scalar, stmt)
        return result or 0

    async def get_many(
        self, session: Session | AsyncSession, params: DBExecuteParams = None
    ):
        """
        Executes the database query using the provided session and returns the results.

        Args:
            session (Session | AsyncSession): The session to use for the query.
            params (DBExecuteParams, optional): The parameters to apply to the query. Defaults to None.

        Returns:
            list[Model] | None: The result of the query.

        Raises:
            Exception: If an error occurs during query execution.
        """
        if params is None:
            params = {}
        stmt, _ = await self._handle_params(select(self.datamodel.obj), params)

        logger.debug(f"Executing query: {stmt}")
        result = await smart_run(session.scalars, stmt)
        return list(result.all())

    async def get_one(
        self, session: Session | AsyncSession, params: DBExecuteParams = None
    ):
        """
        Executes the database query using the provided session and returns the first result.

        Args:
            session (Session | AsyncSession): The session to use for the query.
            params (DBExecuteParams, optional): The parameters to apply to the query. Defaults to None.

        Returns:
            Model | None: The first result of the query.
        """
        if params is None:
            params = {}
        stmt, _ = await self._handle_params(select(self.datamodel.obj), params)

        logger.debug(f"Executing query: {stmt}")
        result = await smart_run(session.scalars, stmt)
        return result.first()

    async def yield_per(
        self,
        session: Session | AsyncSession,
        page_size: int,
        params: DBExecuteParams = None,
    ):
        """
        Executes the database query using the provided session and yields results in batches of the specified size.

        Note: PLEASE ALWAYS CLOSE THE SESSION AFTER USING THIS METHOD

        Args:
            session (Session | AsyncSession): The session to use for the query.
            page_size (int): The number of items to yield per batch.
            params (DBExecuteParams, optional): The parameters to apply to the query. Defaults to None.

        Returns:
            Generator[Sequence, None, None]: A generator that yields results in batches of the specified size.
        """
        if params is None:
            params = {}
        stmt, _ = await self._handle_params(select(self.datamodel.obj), params)
        stmt = stmt.execution_options(stream_results=True)
        if isinstance(session, AsyncSession):
            result = await session.stream(stmt)
            result = result.scalars()
        else:
            result = session.scalars(stmt)
        while True:
            chunk = await smart_run(result.fetchmany, page_size)
            if not chunk:
                break
            yield chunk

    @overload
    async def _handle_params(
        self, stmt: T, params: DBExecuteParams
    ) -> tuple[T, dict[str, tuple[_AbstractLoad, list[Column]]]]: ...
    async def _handle_params(self, stmt: Select, params: DBExecuteParams):
        option_cols = {}

        list_columns = params.get("list_columns")
        join_columns = params.get("join_columns")
        page = params.get("page")
        page_size = params.get("page_size")
        order_column = params.get("order_column")
        order_direction = params.get("order_direction")
        where = params.get("where")
        where_in = params.get("where_in")
        where_id = params.get("where_id")
        where_id_in = params.get("where_id_in")
        filters = params.get("filters")
        filter_classes = params.get("filter_classes")
        global_filter = params.get("global_filter")

        if list_columns:
            stmt = self.load_columns(stmt, list_columns)
        if join_columns:
            #! DEPRECATED
            option_cols = self.join(join_columns)
        if page is not None and page_size is not None:
            stmt = self.page(stmt, page, page_size)
        if order_column and order_direction:
            stmt = self.order_by(stmt, order_column, order_direction)
        if where:
            if not isinstance(where, list):
                where = [where]
            for w in where:
                stmt = self.where(stmt, *w)
        if where_in:
            stmt = self.where_in(stmt, *where_in)
        if where_id:
            stmt = self.where_id(stmt, where_id)
        if where_id_in:
            stmt = self.where_id_in(stmt, where_id_in)
        if filters:
            for filter in filters:
                stmt = await safe_call(self.filter(stmt, filter))
        if filter_classes:
            for col, filter_class, value in filter_classes:
                stmt = await safe_call(
                    self.filter_class(stmt, col, filter_class, value)
                )
        if global_filter:
            stmt = await self._apply_filter(
                FilterGlobal(self.datamodel), stmt, "", global_filter
            )

        return stmt, option_cols

    async def _handle_relation_filter(
        self,
        stmt,
        col: str,
        filter_class: BaseFilter,
        value,
    ):
        col, rel_col = col.split(".")
        rel_obj = filter_class.datamodel.obj
        rel_pks = filter_class.datamodel.get_pk_attrs()
        rel_statements = [select(getattr(rel_obj, pk)) for pk in rel_pks]
        filter_class.query = self
        rel_statements = [
            await safe_call(self._apply_filter(filter_class, stmt, rel_col, value))
            for stmt in rel_statements
        ]
        rel_statements = [
            getattr(rel_obj, pk).in_(stmt) for pk, stmt in zip(rel_pks, rel_statements)
        ]
        func = (
            getattr(self.datamodel.obj, col).any
            if self.datamodel.is_relation_one_to_many(col)
            or self.datamodel.is_relation_many_to_many(col)
            else getattr(self.datamodel.obj, col).has
        )
        return stmt.filter(func(*rel_statements))

    def _convert_id_into_dict(self, id: PRIMARY_KEY) -> dict[str, Any]:
        """
        Converts the given ID into a dictionary format.

        Args:
            id (PRIMARY_KEY): The ID to be converted.

        Returns:
            dict[str, Any]: The converted ID in dictionary format.

        Raises:
            HTTPException: If the ID is invalid.
        """
        pk_dict = {}
        if self.datamodel.is_pk_composite():
            try:
                # Assume the ID is a string, split the string to ','
                id = id.split(",") if isinstance(id, str) else id
                if len(id) != len(self.datamodel.get_pk_attrs()):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid ID: {id}, expected {len(self.datamodel.get_pk_attrs())} values",
                    )
                for pk_key in self.datamodel.get_pk_attrs():
                    pk_dict[pk_key] = id.pop(0)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid ID")
        else:
            pk_dict[self.datamodel.get_pk_attr()] = id

        return pk_dict

    def _join_column(self, stmt: Select, col: str) -> tuple[Select, Column]:
        """
        Joins a related model and returns the specified column.

        Args:
            col (str): The column to join in the format 'relation.column'.

        Returns:
            tuple[Select, Column]: The updated query statement and the specified column.

        Raises:
            ValueError: If the specified relation does not exist in the datamodel.
        """
        rel, col = col.split(".", 1)
        rel_interface = self.datamodel.get_related_interface(rel)
        fk = self.datamodel.get_fk_column(rel)
        stmt = stmt.join(
            rel_interface.obj,
            getattr(self.datamodel.obj, fk)
            == getattr(rel_interface.obj, rel_interface.get_pk_attr()),
            isouter=True,
        )

        # If there is still a . in the column name, it still need to be joined and recursively call this method
        if "." in col:
            datamodel = self.datamodel
            try:
                self.datamodel = rel_interface
                stmt, obj_col = self._join_column(stmt, col)
            finally:
                self.datamodel = datamodel
        else:
            obj_col = getattr(rel_interface.obj, col)

        return stmt, obj_col

    async def _apply_filter(
        self, cls: BaseFilter, stmt: Select, col: Column, value: Any
    ):
        """
        Helper method to apply a filter class.
        """
        cls.query = self
        if cls.is_heavy:
            return await smart_run(cls.apply, stmt, col, value)

        return await safe_call(cls.apply(stmt, col, value))

    def _load_columns_from_dictionary(
        self,
        stmt: Select[T] | _AbstractLoad,
        load_column: LoadColumn,
        columns: list[str] | None = None,
    ):
        """
        Load specified columns into the given SQLAlchemy statement. This method processes the provided dictionary of columns and related columns, and loads them into the statement.

        Args:
            stmt (Select[T] | _AbstractLoad): The SQLAlchemy statement to which the columns will be loaded.
            load_column (LoadColumn): The dictionary of columns to load.
            columns (list[str] | None, optional): A list of column names to be cached. If none, the columns are not cached. Defaults to None.

        Returns:
            Select | _AbstractLoad: The modified SQLAlchemy statement with the specified columns loaded.
        """
        cache_key = ""
        if columns:
            cache_key = f"{self.datamodel.obj.__name__}-{columns}"
            self._load_options_cache[cache_key] = []
        if load_column["type"] == "defer":
            defers = [
                defer(getattr(self.datamodel.obj, col))
                for col in [
                    x
                    for x in self.datamodel.get_user_column_list()
                    if not self.datamodel.is_relation(x)
                ]
            ]
            stmt = stmt.options(*defers)
            if cache_key:
                self._load_options_cache[cache_key].append(defers)
        elif load_column["type"] == "some":
            load_onlys = [
                getattr(self.datamodel.obj, col) for col in load_column["columns"]
            ]
            stmt = stmt.options(load_only(*load_onlys))
            if cache_key:
                self._load_options_cache[cache_key].append(load_only(*load_onlys))

        for col, load_dict in load_column["related_columns"].items():
            interface = self.datamodel.get_related_interface(col)
            query_manager = QueryManager(interface)
            load_dict["stmt"] = query_manager._load_columns_from_dictionary(
                load_dict["stmt"], load_dict
            )
            stmt = stmt.options(load_dict["stmt"])
            if cache_key:
                self._load_options_cache[cache_key].append(load_dict["stmt"])

        return stmt

    def _load_columns_recursively(
        self, stmt: Select[T] | _AbstractLoad, columns: list[str]
    ):
        """
        Load specified columns into the given SQLAlchemy statement. This returns a dictionary that can be used with the `load_columns_from_dictionary` method.

        Args:
            stmt (Select[T] | _AbstractLoad): The SQLAlchemy statement to which the columns will be loaded.
            columns (list[str]): A list of column names to be loaded.

        Returns:
            dict: A dictionary that can be used with the `load_columns_from_dictionary` method.
        """
        load_column = create_load_column(stmt)
        for col in columns:
            sub_col = ""
            if "." in col:
                col, sub_col = col.split(".", 1)

            # If it is not a relation, load only the column if it is in the user column list, else skip
            if not self.datamodel.is_relation(col):
                if col in self.datamodel.get_user_column_list():
                    load_column["columns"].append(col)
                    load_column["type"] = "some"
                continue

            if self.datamodel.is_relation_one_to_one(
                col
            ) or self.datamodel.is_relation_many_to_one(col):
                load_column["related_columns"][col]["stmt"] = load_column[
                    "related_columns"
                ][col]["stmt"] or joinedload(self.datamodel.obj.load_options(col))
            else:
                load_column["related_columns"][col]["stmt"] = load_column[
                    "related_columns"
                ][col]["stmt"] or selectinload(self.datamodel.obj.load_options(col))

            interface = self.datamodel.get_related_interface(col)

            # If there is a . in the sub column, it means it is a relation column, so we need to load it
            if "." in sub_col or interface.is_relation(sub_col):
                query_manager = QueryManager(interface)
                deep_merge(
                    load_column["related_columns"][col],
                    query_manager._load_columns_recursively(
                        load_column["related_columns"][col]["stmt"], [sub_col]
                    ),
                    rules={
                        "type": lambda x1, x2: LOAD_TYPE_MAPPING[x2]
                        > LOAD_TYPE_MAPPING[x1]
                    },
                )

            # If load_type is all, we load all columns, don't need to specify columns
            if load_column["related_columns"][col]["type"] == "all":
                continue

            # If the sub_col is specified, we load only necessary columns
            if not sub_col:
                load_column["related_columns"][col]["type"] = "all"

            if sub_col:
                # Skip if the sub column is not in the user column list or if it is a relation
                if (
                    sub_col not in interface.get_user_column_list()
                    or interface.is_relation(sub_col)
                ):
                    continue
                load_column["related_columns"][col]["columns"].append(sub_col)
                load_column["related_columns"][col]["type"] = "some"

        return load_column


class DatabaseSessionManager:
    Table = Table

    _engine: AsyncEngine | Engine | None = None
    _sessionmaker: async_sessionmaker[AsyncSession] | sessionmaker[Session] | None = (
        None
    )
    _engine_binds: dict[str, AsyncEngine | Engine] = None
    _sessionmaker_binds: dict[
        str, async_sessionmaker[AsyncSession] | sessionmaker[Session]
    ] = None
    _scoped_session_maker: (
        async_scoped_session[AsyncSession] | scoped_session[Session] | None
    ) = None
    _scoped_session_maker_binds: dict[
        str, async_scoped_session[AsyncSession] | scoped_session[Session]
    ] = None
    _scoped_session: AsyncSession | Session | None = None
    _scoped_session_binds: dict[str, AsyncSession | Session] = None

    def __init__(self) -> None:
        self._engine_binds = {}
        self._sessionmaker_binds = {}
        self._scoped_session_maker_binds = {}
        self._scoped_session_binds = {}

    def init_db(self, url: str, binds: dict[str, str] | None = None):
        """
        Initializes the database engine and session maker.

        Args:
            url (str): The URL of the database.
            binds (dict[str, str] | None, optional): Additional database URLs to bind to. Defaults to None.
        """
        from .setting import Setting

        self._engine = self._init_engine(url, Setting.SQLALCHEMY_ENGINE_OPTIONS)
        self._sessionmaker = self._init_sessionmaker(self._engine)
        self._scoped_session_maker = self._init_scoped_session(self._sessionmaker)

        for key, value in (binds or {}).items():
            self._engine_binds[key] = self._init_engine(
                value,
                Setting.SQLALCHEMY_ENGINE_OPTIONS_BINDS.get(key, {}),
            )
            self._sessionmaker_binds[key] = self._init_sessionmaker(
                self._engine_binds[key]
            )
            self._scoped_session_maker_binds[key] = self._init_scoped_session(
                self._sessionmaker_binds[key]
            )

    def get_engine(self, bind: str | None = None):
        """
        Returns the database engine.

        Args:
            bind (str | None, optional): The database URL to bind to. If None, the default database is used. Defaults to None.

        Returns:
            AsyncEngine | Engine | None: The database engine or None if it does not exist.
        """
        return self._engine_binds.get(bind) if bind else self._engine

    def get_metadata(self, bind: str | None = None):
        """
        Retrieves the metadata associated with the specified bind.

        If bind is specified, but the metadata does not exist, a new metadata is created and associated with the bind.

        Parameters:
            bind (str | None): The bind to retrieve the metadata for. If None, the default metadata is returned.

        Returns:
            The metadata associated with the specified bind. If bind is None, returns the default metadata.
        """
        if bind:
            bind_metadata = metadatas.get(bind)
            if not bind_metadata:
                bind_metadata = MetaData()
                metadatas[bind] = bind_metadata
            return bind_metadata
        return metadata

    async def init_fastapi_rtk_tables(self):
        """
        Initializes the tables required for FastAPI RTK to function.
        """
        tables = [
            table for key, table in metadata.tables.items() if key in FASTAPI_RTK_TABLES
        ]
        fastapi_rtk_metadata = MetaData()
        for table in tables:
            table.to_metadata(fastapi_rtk_metadata)
        async with self.connect() as connection:
            await self._create_all(connection, fastapi_rtk_metadata)

    async def close(self):
        """
        If engine exists, disposes the engine and sets it to None.

        If engine binds exist, disposes all engine binds and sets them to None.
        """
        if self._scoped_session_maker:
            await safe_call(self._scoped_session_maker.remove())
            self._scoped_session_maker = None

        if self._scoped_session_maker_binds:
            for scoped_session_maker in self._scoped_session_maker_binds.values():
                await safe_call(scoped_session_maker.remove())
            self._scoped_session_maker_binds.clear()

        if self._engine:
            await safe_call(self._engine.dispose())
            self._engine = None
            self._sessionmaker = None

        if self._engine_binds:
            for engine in self._engine_binds.values():
                await safe_call(engine.dispose())
            self._engine_binds.clear()
            self._sessionmaker_binds.clear()

    @contextlib.asynccontextmanager
    async def connect(self, bind: str | None = None):
        """
        Establishes a connection to the database.

        ***EVEN IF THE CONNECTION IS SYNC, ASYNC WITH ... AS ... IS STILL NEEDED.***

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            AsyncConnection | Connection: The database connection.
        """
        engine = self._engine_binds.get(bind) if bind else self._engine
        if not engine:
            raise Exception("DatabaseSessionManager is not initialized")

        if isinstance(engine, AsyncEngine):
            async with engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    await connection.rollback()
                    raise
        else:
            with engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    connection.rollback()
                    raise

    @contextlib.asynccontextmanager
    async def session(self, bind: str | None = None):
        """
        Provides a database session for performing database operations.

        ***EVEN IF THE SESSION IS SYNC, ASYNC WITH ... AS ... IS STILL NEEDED.***

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            AsyncSession | Session: The database session.

        Returns:
            None
        """
        session_maker = (
            self._sessionmaker_binds.get(bind) if bind else self._sessionmaker
        )
        if not session_maker:
            raise Exception("DatabaseSessionManager is not initialized")

        session = session_maker()
        try:
            yield session
        except Exception:
            await safe_call(session.rollback())
            raise
        finally:
            await safe_call(session.close())

    @contextlib.asynccontextmanager
    async def scoped_session(self, bind: str | None = None):
        """
        Provides a scoped database session class for performing database operations.

        ***EVEN IF THE SESSION IS SYNC, ASYNC WITH ... AS ... IS STILL NEEDED.***

        Args:
            bind (str, optional): The database URL to bind to. If none, the default database is used. Defaults to None.

        Raises:
            Exception: If the DatabaseSessionManager is not initialized.

        Yields:
            scoped_session[Session] | async_scoped_session[AsyncSession]: The scoped database session.

        Returns:
            None
        """
        scoped_session_maker = (
            self._scoped_session_maker_binds.get(bind)
            if bind
            else self._scoped_session_maker
        )
        if not scoped_session_maker:
            raise Exception("DatabaseSessionManager is not initialized")
        scoped_session = scoped_session_maker()

        try:
            yield scoped_session
        except Exception:
            await safe_call(scoped_session_maker.rollback())
            raise
        finally:
            await safe_call(scoped_session_maker.remove())

    # Used for testing
    async def create_all(self, binds: list[str] | Literal["all"] | None = "all"):
        """
        Creates all tables in the database.

        Args:
            binds (list[str] | Literal["all"] | None, optional): The database URLs to create tables in. Defaults to "all".
        """
        async with self.connect() as connection:
            await self._create_all(connection, metadata)

        if not self._engine_binds or not binds:
            return

        bind_keys = self._engine_binds.keys() if binds == "all" else binds
        for key in bind_keys:
            async with self.connect(key) as connection:
                await self._create_all(connection, metadatas[key])

    async def drop_all(self, binds: list[str] | Literal["all"] | None = "all"):
        """
        Drops all tables in the database.

        Args:
            binds (list[str] | Literal["all"] | None, optional): The database URLs to drop tables in. Defaults to "all".
        """
        async with self.connect() as connection:
            await self._create_all(connection, metadata, drop=True)

        if not self._engine_binds or not binds:
            return

        bind_keys = self._engine_binds.keys() if binds == "all" else binds
        for key in bind_keys:
            async with self.connect(key) as connection:
                await self._create_all(connection, metadatas[key], drop=True)

    async def autoload_table(self, func: Callable[[Connection], SA_Table]):
        """
        Autoloads a table from the database using the provided function.

        As `autoload_with` is not supported in async SQLAlchemy, this method is used to autoload tables asynchronously.

        *If the `db` is not initialized, the function is run without a connection. So it has the same behavior as creating the table without autoloading.*

        *After the table is autoloaded, the database connection is closed. This means `autoload_table` should not be used with primary `db`. Consider using a separate `db` instance instead.*

        Args:
            func (Callable[[Connection], SA_Table]): The function to autoload the table.

        Returns:
            SA_Table: The autoloaded table.
        """
        if not self._engine:
            return func(None)

        try:
            async with self.connect() as conn:
                if isinstance(conn, AsyncConnection):
                    return await conn.run_sync(func)
                else:
                    return func(conn)
        finally:
            await self.close()

    def _init_engine(self, url: str, engine_options: dict[str, Any]):
        """
        Initializes the database engine.

        Args:
            url (str): The URL of the database.
            engine_options (dict[str, Any]): The options to pass to the database engine.

        Returns:
            AsyncEngine | Engine: The database engine. If the URL is an async URL, an async engine is returned.
        """
        try:
            return create_async_engine(url, **engine_options)
        except InvalidRequestError:
            return create_engine(url, **engine_options)

    def _init_sessionmaker(self, engine: AsyncEngine | Engine):
        """
        Initializes the database session maker.

        Args:
            engine (AsyncEngine | Engine): The database engine.

        Returns:
            async_sessionmaker[AsyncSession] | sessionmaker[Session]: The database session maker.
        """
        if isinstance(engine, AsyncEngine):
            return async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return sessionmaker(
            bind=engine,
            class_=Session,
            expire_on_commit=False,
        )

    def _init_scoped_session(
        self, sessionmaker: async_sessionmaker[AsyncSession] | sessionmaker[Session]
    ):
        """
        Initializes the scoped session.

        Args:
            sessionmaker (async_sessionmaker[AsyncSession] | sessionmaker[Session]): The session maker to use.

        Returns:
            scoped_session | async_scoped_session: The scoped session.
        """
        if isinstance(sessionmaker, async_sessionmaker):
            return async_scoped_session(sessionmaker, scopefunc=asyncio.current_task)
        return scoped_session(sessionmaker)

    async def _create_all(
        self, connection: Connection | AsyncConnection, metadata: MetaData, drop=False
    ):
        """
        Creates all tables in the database based on the metadata.

        Args:
            connection (Connection | AsyncConnection): The database connection.
            metadata (MetaData): The metadata object containing the tables to create.
            drop (bool, optional): Whether to drop the tables instead of creating them. Defaults to False.

        Returns:
            None
        """
        func = metadata.drop_all if drop else metadata.create_all
        if isinstance(connection, AsyncConnection):
            return await connection.run_sync(func)
        return func(connection)


db = DatabaseSessionManager()


def get_session(bind: str | None = None):
    """
    A coroutine function that returns a function that yields a database session.

    Can be used as a dependency in FastAPI routes.

    Args:
        bind (str, optional): The database URL to bind to. If None, the default database is used. Defaults to None.

    Returns:
        AsyncGenerator[AsyncSession, Session]: A generator that yields a database session.

    Usage:
    ```python
        @app.get("/items/")
        async def read_items(session: AsyncSession = Depends(get_session())):
            # Use the session to interact with the database
    ```
    """

    async def get_session_dependency():
        async with db.session(bind) as session:
            yield session

    return get_session_dependency


def get_scoped_session(bind: str | None = None):
    """
    A coroutine function that returns a function that yields a scoped database session class.

    Can be used as a dependency in FastAPI routes.

    Args:
        bind (str, optional): The database URL to bind to. If None, the default database is used. Defaults to None.

    Returns:
        AsyncGenerator[scoped_session[Session], async_scoped_session[AsyncSession]]: A generator that yields a scoped database session.

    Usage:
    ```python
        @app.get("/items/")
        async def read_items(session: scoped_session[Session] = Depends(get_scoped_session())):
            # Use the session to interact with the database
    ```
    """

    async def get_scoped_session_dependency():
        async with db.scoped_session(bind) as session:
            yield session

    return get_scoped_session_dependency


async def get_user_db(
    session: AsyncSession | Session = Depends(get_session(User.__bind_key__)),
):
    """
    A dependency for FAST API to get the UserDatabase instance.

    Parameters:
    - session: The async session object for the database connection.

    Yields:
    - UserDatabase: An instance of the UserDatabase class.

    """
    yield UserDatabase(session, User, OAuthAccount)
