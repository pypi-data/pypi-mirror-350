from typing import Any

from fastapi import HTTPException

from ..const import logger
from ..db import DBExecuteParams, QueryManager
from ..schemas import FilterSchema
from .filters import GenericBaseFilter
from .interface import GenericInterface
from .model import GenericModel
from .session import GenericSession

__all__ = ["GenericQueryManager"]


class GenericQueryManager(QueryManager):
    """
    A class to manage database queries for generic. It provides methods to add options for pagination, ordering, and filtering to the query.

    Raises:
        e: If an error occurs during query execution.
    """

    datamodel: GenericInterface
    stmt: GenericSession = None

    def join(self, columns: str | list[str]):
        #! DEPRECATED
        logger.warning(
            "The `join` method is deprecated and will be removed. Use the `load_columns` method instead."
        )
        return {}

    def load_columns(self, stmt, columns, depth=0):
        return stmt

    def order_by(self, stmt: GenericSession, column: str, direction: str):
        col = column.lstrip().rstrip()

        #! If the order column comes from a request, it will be in the format ClassName.column_name
        if col.startswith(self.datamodel.obj.__class__.__name__) or col.startswith(
            self.datamodel.obj.__name__
        ):
            col = col.split(".", 1)[1]

        return stmt.order_by(col, direction)

    def where(self, stmt: GenericSession, column: str, value: Any):
        return stmt.equal(column, value)

    def where_in(self, stmt: GenericSession, column: str, values: list[Any]):
        return stmt.in_(column, values)

    def filter(self, stmt: GenericSession, filter: FilterSchema):
        filter_classes = self.datamodel.filters.get(filter.col)
        filter_class = None
        for f in filter_classes:
            if f.arg_name == filter.opr:
                filter_class = f
                break
        if not filter_class:
            raise HTTPException(
                status_code=400, detail=f"Invalid filter opr: {filter.opr}"
            )

        col = filter.col
        value = filter.value

        return filter_class.apply(stmt, col, value)

    def filter_class(
        self,
        stmt: GenericSession,
        col: str,
        filter_class: GenericBaseFilter,
        value: Any,
    ):
        return filter_class.apply(stmt, col, value)

    def commit(self, session): ...

    def refresh(self, session, item): ...

    def flush(self, session, items): ...

    def delete(self, session: GenericSession, item: GenericModel):
        session.delete(item)

    def count(
        self,
        session: GenericSession,
        filters: list[FilterSchema] | None = None,
        filter_classes: list[tuple[str, GenericBaseFilter, Any]] | None = None,
    ) -> int:
        stmt = session.query(self.datamodel.obj)
        if filters:
            for filter in filters:
                stmt = self.filter(stmt, filter)
        if filter_classes:
            for col, filter_class, value in filter_classes:
                stmt = self.filter_class(stmt, col, filter_class, value)
        return stmt.count()

    def get_many(self, session: GenericSession, params: DBExecuteParams = None):
        if params is None:
            params = {}
        stmt, _ = self._handle_params(session.query(self.datamodel.obj), params)
        return stmt.all()

    def get_one(self, session: GenericSession, params: DBExecuteParams = None):
        if params is None:
            params = {}
        stmt, _ = self._handle_params(session.query(self.datamodel.obj), params)
        return stmt.first()

    async def yield_per(
        self, session: GenericSession, page_size: int, params: DBExecuteParams = None
    ):
        if params is None:
            params = {}
        stmt, _ = self._handle_params(session.query(self.datamodel.obj), params)

        items = stmt.yield_per(page_size)
        while True:
            chunk = items[:page_size]
            items = items[page_size:]
            if not chunk:
                break
            yield chunk

    def _handle_params(self, stmt: GenericSession, params: DBExecuteParams):
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
                stmt = self.filter(stmt, filter)
        if filter_classes:
            for col, filter_class, value in filter_classes:
                stmt = self.filter_class(stmt, col, filter_class, value)

        return stmt, option_cols
