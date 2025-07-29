import asyncio
import collections
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Collection, Dict, Sequence, Set, Tuple

from sqlalchemy import Connection, Engine, MetaData
from sqlalchemy import Table as SA_Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import SchemaConst, SchemaItem
from sqlalchemy.util.typing import Literal

__all__ = ["Model", "metadata", "metadatas", "Base"]

camelcase_re = re.compile(r"([A-Z]+)(?=[a-z0-9])")


def camel_to_snake_case(name):
    def _join(match):
        word = match.group()

        if len(word) > 1:
            return ("_%s_%s" % (word[:-1], word[-1])).lower()

        return "_" + word.lower()

    return camelcase_re.sub(_join, name).lstrip("_")


metadatas: dict[str, MetaData] = {
    "default": MetaData(),
}

cache_id_property: dict[str, list[str]] = {}


class BasicModel:
    """
    A basic model class that provides a method to update the model instance with the given data.
    """

    def update(self, data: dict[str, any]):
        """
        Updates the model instance with the given data.

        Args:
            data (dict): The data to update the model instance with.

        Returns:
            None
        """
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def name_(self):
        """
        Returns the string representation of the object.
        """
        return str(self)

    @property
    def id_(self):
        """
        Returns the primary key of the object as a dictionary.

        Useful when it is a composite primary keys.

        Returns:
            dict[str, any]: The primary key of the object as a dictionary.
        """
        try:
            if self.__class__.__name__ in cache_id_property:
                return self._convert_id(
                    [
                        str(getattr(self, k))
                        for k in cache_id_property[self.__class__.__name__]
                    ]
                )

            from .api import SQLAInterface

            cache_id_property[self.__class__.__name__] = SQLAInterface(
                self.__class__
            ).get_pk_attrs()
            return self.id_
        except Exception:
            return None

    def _convert_id(self, ids: list[Any]):
        """
        Convert the primary key from a list to 1 value if it is a single primary key.

        Args:
            ids (list[Any]): The primary key as a list.

        Returns:
            Any: The primary key as a single value. If there is more than 1 primary key, it will return the list.
        """
        if len(ids) == 1:
            return ids[0]
        return ids


class Model(BasicModel, DeclarativeBase):
    """
    Use this class has the base for your models,
    it will define your table names automatically
    MyModel will be called my_model on the database.

    ::

        from sqlalchemy import Integer, String
        from fastapi-rtk import Model

        class MyModel(Model):
            id = Column(Integer, primary_key=True)
            name = Column(String(50), unique = True, nullable=False)

    """

    _relationship_filters: collections.defaultdict[str, list[str]] | None = None

    __bind_key__: str | None = None
    """
    The bind key to use for this model. This allow you to use multiple databases. None means the default database. Default is None.
    """

    metadata = metadatas["default"]

    def __init_subclass__(cls, **kw: Any) -> None:
        # Set the bind key from the metadata __table__ if it exists
        if hasattr(cls, "__table__"):
            for key, metadata in metadatas.items():
                if metadata is cls.__table__.metadata and key != "default":
                    cls.__bind_key__ = key

        # Overwrite the metadata if the bind key is set
        if cls.__bind_key__:
            if cls.__bind_key__ not in metadatas:
                metadatas[cls.__bind_key__] = MetaData()
            cls.metadata = metadatas[cls.__bind_key__]
        return super().__init_subclass__(**kw)

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Returns the table name for the given class.

        The table name is derived from the class name by converting
        any uppercase letters to lowercase and inserting an underscore
        before each uppercase letter.

        Returns:
            str: The table name.
        """
        return camel_to_snake_case(cls.__name__)

    __table_args__ = {"extend_existing": True}

    @classmethod
    def load_options(cls, col: str):
        """
        Load options for a given column with optional relationship filters. To be used when using loader options from `sqlalchemy.orm` such as `joinedLoad` or `selectinload`. The relationship filter can be defined using the `relationship_filter` decorator.

        Args:
            col (str): The name of the column to load options for.

        Returns:
            The attribute of the class with applied relationship filters if any.

        Raises:
            AttributeError: If the specified column does not exist in the class.
        """
        attr = getattr(cls, col)
        if cls._relationship_filters and col in cls._relationship_filters:
            criteria = []
            for func_name in cls._relationship_filters[col]:
                criteria.append(getattr(cls, func_name)())
            attr = attr.and_(*criteria)
        return attr


class Table(SA_Table):
    """
    This class is a wrapper around the SQLAlchemy `Table` class that allows you to autoload the table from the database asynchronously.

    Initialize it like you would a normal `Table` object.
    """

    def __init__(
        self,
        name: str,
        metadata: MetaData,
        *args: SchemaItem,
        schema: str | None | Literal[SchemaConst.BLANK_SCHEMA] = None,
        quote: bool | None = None,
        quote_schema: bool | None = None,
        autoload_with: Engine | Connection | None = None,
        autoload_replace: bool = True,
        keep_existing: bool = False,
        extend_existing: bool = False,
        resolve_fks: bool = True,
        include_columns: Collection[str] | None = None,
        implicit_returning: bool = True,
        comment: str | None = None,
        info: Dict[Any, Any] | None = None,
        listeners: Sequence[Tuple[str, Callable[..., Any]]] | None = None,
        prefixes: Sequence[str] | None = None,
        _extend_on: Set[SA_Table] | None = None,
        _no_init: bool = True,
        **kw: Any,
    ) -> None:
        from .db import DatabaseSessionManager

        db = DatabaseSessionManager()

        if autoload_with:
            if isinstance(autoload_with, Engine):
                db.init_db(autoload_with.url)
            else:
                db.init_db(autoload_with.engine.url)

        with ThreadPoolExecutor() as executor:
            future = executor.submit(
                asyncio.run,
                db.autoload_table(
                    lambda conn: SA_Table.__init__(
                        self,
                        name,
                        metadata,
                        *args,
                        schema=schema,
                        quote=quote,
                        quote_schema=quote_schema,
                        autoload_with=conn,
                        autoload_replace=autoload_replace,
                        keep_existing=keep_existing,
                        extend_existing=extend_existing,
                        resolve_fks=resolve_fks,
                        include_columns=include_columns,
                        implicit_returning=implicit_returning,
                        comment=comment,
                        info=info,
                        listeners=listeners,
                        prefixes=prefixes,
                        _extend_on=_extend_on,
                        _no_init=_no_init,
                        **kw,
                    )
                ),
            )
            future.result()


metadata = metadatas["default"]


"""
    This is for retro compatibility
"""
Base = Model
