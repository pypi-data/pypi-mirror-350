import collections
import enum
import inspect
import json
import typing
from datetime import date, datetime
from typing import Annotated, Any, List, Literal, Optional, Tuple, Type, overload

import marshmallow_sqlalchemy
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    create_model,
)
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import SynonymProperty, class_mapper
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty
from sqlalchemy.sql import sqltypes as sa_types

from ..async_column_handler import AsyncColumnHandler
from ..db import (
    AsyncSession,
    DBExecuteParams,
    QueryManager,
    Session,
)
from ..filters import BaseFilter, SQLAFilterConverter
from ..globals import g
from ..models import Model
from ..schemas import (
    PRIMARY_KEY,
    ColumnEnumInfo,
    ColumnInfo,
    ColumnRelationInfo,
    DatetimeUTC,
    QuerySchema,
)
from ..types import FileColumn, ImageColumn
from ..utils import deep_merge, is_sqla_type, smart_run

__all__ = ["Params", "SQLAInterface"]


class BaseSession:
    """
    Dummy class to represent a session for `GenericModel`. This can be used to bypass the pydantic validation for `get_api_session` method in `ModelRestApi`.
    """


class Params(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: PRIMARY_KEY | None = None
    ids: List[PRIMARY_KEY] | None = None
    q: QuerySchema | None = None
    query: QueryManager | None = None
    session: AsyncSession | Session | BaseSession | None = None
    body: BaseModel | None = None
    item: Model | Any | None = None
    items: List[Model | Any] | None = None
    extra: Any | None = None


class P_ID(Params):
    id: PRIMARY_KEY


class P_IDS(Params):
    ids: List[PRIMARY_KEY]


class P_Q(Params):
    q: QuerySchema


class P_QUERY(Params):
    query: QueryManager


class P_SESSION(Params):
    session: AsyncSession | Session | BaseSession


class P_BODY(Params):
    body: BaseModel


class P_ITEM(Params):
    item: Model | Any


class P_ITEMS(Params):
    items: List[Model | Any]


class PARAM_Q_QUERY(P_Q, P_QUERY):
    pass


class PARAM_IDS_Q_QUERY_SESSION_ITEMS(P_IDS, P_Q, P_QUERY, P_SESSION, P_ITEMS):
    pass


class PARAM_ID_QUERY_SESSION(P_ID, P_QUERY, P_SESSION):
    pass


class PARAM_ID_QUERY_SESSION_ITEM(P_ID, P_QUERY, P_SESSION, P_ITEM):
    pass


class PARAM_BODY_QUERY_SESSION(P_BODY, P_QUERY, P_SESSION):
    pass


class SQLAInterface:
    """
    Represents an interface for a SQLAlchemy model. It provides methods for creating a pydantic schema for the model, as well as for testing the types of the model's columns.
    """

    obj: Type[Model]
    filter_converter: SQLAFilterConverter = SQLAFilterConverter()
    with_fk: bool

    _id_schema: dict[str, type] = {}
    _schema: Type[BaseModel] = None
    _schema_optional: Type[BaseModel] = None
    _list_columns: dict[str, Column] = None
    _list_properties: dict[str, Column] = None
    _filters: collections.defaultdict[str, list[BaseFilter]] = None
    _exclude_filters: collections.defaultdict[str, list[str]] = None
    _cache_schema: dict[str, Type[BaseModel]] = {}
    _cache_field: dict[str, str] = {}

    def __init__(self, obj: Type[Model], with_fk: bool = True):
        self.obj = obj
        self.with_fk = with_fk

    def generate_schema(
        self,
        columns: List[str] | None = None,
        with_name_=True,
        with_id_=True,
        optional=False,
        name="",
        hide_sensitive_columns=True,
    ):
        """
        Generate a pydantic schema for the model with the specified columns and options. If a column is a relation, the schema for the related model is generated as well.

        Args:
            columns (List[str] | None, optional): The list of columns to include in the schema. Defaults to None.
            with_name_ (bool, optional): Whether to include the name_ column. Defaults to True.
            with_id_ (bool, optional): Whether to include the id_ column. Defaults to True.
            optional (bool, optional): Whether the columns should be optional. Defaults to False.
            name (str, optional): The name of the schema. If not specified, the name is generated based on the object's name and the specified options. Defaults to ''.
            hide_sensitive_columns (bool, optional): Whether to hide sensitive columns such as `password`. Defaults to True.

        Returns:
            type[BaseModel]: The Pydantic schema for the model.
        """
        if not name:
            name = f"{self.obj.__name__}-Schema"
            if columns:
                name += f"-{'-'.join(columns)}"
            if with_name_:
                name += "-WithName"
            if with_id_:
                name += "-WithID"
            if optional:
                name += "-Optional"
            if hide_sensitive_columns:
                name += "-HideSensitive"
            if self.with_fk:
                name += "-WithFK"
            if name in self._cache_schema:
                return self._cache_schema[name]

        return self._generate_schema_from_dict(
            self._generate_schema_from_columns(
                columns, with_name_, with_id_, optional, name, hide_sensitive_columns
            )
        )

    def get_type(self, col: str):
        """
        Get the Python type corresponding to the specified column name.

        Args:
            col (str): The name of the column.

        Returns:
            Type: The Python type corresponding to the column.

        """
        if self.is_enum(col):
            col_type = None
            enum_val = self.get_enum_value(col)
            enum_values = list(enum_val)

            for val in enum_values:
                new_val = Literal[val]
                if isinstance(val, enum.Enum):
                    value_type = type(val.value)
                    new_val = (
                        new_val
                        | Annotated[
                            Literal[str(val.value)],
                            AfterValidator(lambda x: enum_val(value_type(x))),
                        ]
                    )
                if col_type is None:
                    col_type = new_val
                else:
                    col_type = col_type | new_val
            return col_type
        elif self.is_geometry(col):
            from geoalchemy2 import Geometry

            return Geometry
        elif self.is_date(col):
            return date
        elif self.is_datetime(col):
            return DatetimeUTC | datetime
        elif self.is_text(col) or self.is_string(col):
            return str
        elif (
            self.is_integer(col_name=col) or self.is_numeric(col) or self.is_float(col)
        ):
            return int | float
        elif self.is_boolean(col):
            return bool
        elif self.is_json or self.is_jsonb(col):
            #! At the bottom, because everything is a subclass of the JSON type

            def validator_func(data):
                try:
                    return json.loads(data)
                except Exception:
                    return data

            return typing.Annotated[
                typing.Any,
                AfterValidator(validator_func),
            ]
        elif self.is_relation(col_name=col):
            raise Exception(
                f"Column '{col}' is a relation. Use 'get_relation_type' instead."
            )
        else:
            return typing.Any

    def get_type_name(self, col: str) -> str:
        """
        Get the name of the Python type corresponding to the specified column name.

        Args:
            col (str): The name of the column.

        Returns:
            str: The name of the Python type corresponding to the column.

        """
        cache_key = f"{self.obj.__name__}.{col}"
        if not self._cache_field.get(cache_key):
            try:
                # Check for geometry
                if self.is_geometry(col):
                    self._cache_field[cache_key] = "Geometry"
                elif self.is_enum(col):
                    self._cache_field[cache_key] = "Enum"
                elif self.is_hybrid_property(col):
                    self._cache_field[cache_key] = marshmallow_sqlalchemy.column2field(
                        Column(
                            col, getattr(self.obj, col).expression.type, nullable=True
                        )
                    ).__class__.__name__
                else:
                    self._cache_field[cache_key] = marshmallow_sqlalchemy.field_for(
                        self.obj, col
                    ).__class__.__name__
            except Exception:
                self._cache_field[cache_key] = "Unknown"
        return self._cache_field[cache_key]

    async def get_column_info(
        self,
        col: str,
        session: Session | AsyncSession,
        *,
        params: DBExecuteParams | None = None,
        description_columns: dict[str, str] | None = None,
        label_columns: dict[str, str] | None = None,
        dictionary_cache: dict[str, Any] | None = None,
        cache_key: str | None = None,
    ):
        """
        Get the information about a column in the model.

        Args:
            col (str): The name of the column.
            session (Session | AsyncSession): The SQLAlchemy session to use for the query.
            params (DBExecuteParams | None, optional): The parameters for the query. Defaults to None.
            description_columns (dict[str, str] | None, optional): Mapping of column names to their descriptions. Defaults to None.
            label_columns (dict[str, str] | None, optional): Mapping of column names to their labels. Defaults to None.
            dictionary_cache (dict[str, Any] | None, optional): Storage for cached values. Must be used together with `cache_key`. Defaults to None.
            cache_key (str | None, optional): Key for caching the result. Must be used together with `dictionary_cache`. Defaults to None.

        Returns:
            ColumnInfo | ColumnRelationInfo | ColumnEnumInfo: The information about the column.
        """
        # Return cached value if available
        if cache_key and dictionary_cache is not None:
            # Check if the cache_key is in the dictionary_cache
            if cache_key in dictionary_cache:
                return dictionary_cache[cache_key]

        params = params or DBExecuteParams(page=0)
        description_columns = description_columns or {}
        label_columns = label_columns or {}
        column_info = {
            "description": description_columns.get(col, ""),
            "label": label_columns.get(col, ""),
            "name": col,
            "required": not self.is_nullable(col),
            "unique": self.is_unique(col),
            "type": self.get_type_name(col),
        }

        if self.is_relation(col):
            related_interface = self.get_related_interface(col)
            query = QueryManager(related_interface)
            related_items = await smart_run(
                query.get_many,
                session,
                params,
            )
            count = await smart_run(
                query.count, session, filter_classes=params.get("filter_classes")
            )
            values = []
            for item in related_items:
                id, item = related_interface.convert_to_result(item)
                values.append({"id": id, "value": str(item)})
            column_info["count"] = count
            column_info["values"] = values
            return ColumnRelationInfo(**column_info)
        info_class = ColumnInfo

        if self.is_enum(col):
            info_class = ColumnEnumInfo
            column_info["values"] = self.get_enum_value(col)

        info = info_class(**column_info)

        # Cache the result if a cache key is provided
        if cache_key and dictionary_cache is not None:
            dictionary_cache[cache_key] = info

        return info

    def get_pk_attr(self) -> str:
        """
        Returns the name of the primary key attribute for the object.

        Returns:
            str: The name of the primary key attribute.
        """
        for key in self.list_columns.keys():
            if self.is_pk(key):
                return key

    def get_pk_attrs(self) -> List[str]:
        """
        Returns the names of the primary key attributes for the object.

        Returns:
            List[str]: The names of the primary key attributes.
        """
        return [key for key in self.list_columns.keys() if self.is_pk(key)]

    def _init_properties(self):
        """
        Initialize the properties of the object.

        This method initializes the properties of the object by creating a dictionary of the object's columns and their corresponding types.

        Returns:
            None
        """
        self._list_columns = dict()
        self._list_properties = dict()
        for prop in class_mapper(self.obj).iterate_properties:
            if type(prop) is not SynonymProperty:
                self._list_properties[prop.key] = prop
        for col_name in self.obj.__mapper__.columns.keys():
            if col_name in self._list_properties:
                self._list_columns[col_name] = self.obj.__mapper__.columns[col_name]

    def _init_filters(self):
        """
        Initializes the filters dictionary by iterating over the keys of the `list_properties` dictionary.
        For each key, it checks if the class has the corresponding attribute specified in the `conversion_table`
        of the `filter_converter` object. If the attribute exists, it adds the corresponding filters to the
        `_filters` dictionary.

        Parameters:
            None

        Returns:
            None
        """
        self._filters = collections.defaultdict(list)
        for col in self.list_properties.keys():
            for func_attr, filters in self.filter_converter.conversion_table:
                if getattr(self, func_attr)(col):
                    self._filters[col] = [f(self) for f in filters]
                    break

        for col in self.get_property_column_list():
            if self.is_hybrid_property(col):
                self.list_columns[col] = Column(
                    col, getattr(self.obj, col).expression.type, nullable=True
                )
                try:
                    for func_attr, filters in self.filter_converter.conversion_table:
                        if getattr(self, func_attr)(col):
                            self._filters[col] = [f(self) for f in filters]
                            break
                finally:
                    del self.list_columns[col]

    """
    ------------------------------
     FUNCTIONS FOR PROPERTIES
    ------------------------------
    """

    @property
    def id_schema(self):
        if not self._id_schema.get(self.obj.__name__):
            pk_type = int | float
            pk_attr = self.get_pk_attr()
            if self.is_pk_composite() or self.is_string(pk_attr):
                pk_type = str
            self._id_schema[self.obj.__name__] = pk_type
        return self._id_schema[self.obj.__name__]

    @id_schema.setter
    def id_schema(self, value: type):
        self._id_schema[self.obj.__name__] = value

    @property
    def schema(self) -> Type[BaseModel]:
        """
        The pydantic schema for the model. This is the standard schema. If the field is optional, it will be set to None as default.
        """
        if not self._schema:
            cols = self.get_column_list() + self.get_property_column_list()
            if not self.with_fk:
                cols = [
                    col
                    for col in cols
                    if not self.is_fk(col) and not self.is_relation(col)
                ]
            self._schema = self.generate_schema(cols)
        return self._schema

    @schema.setter
    def schema(self, value: Type[BaseModel]):
        self._schema = value

    @property
    def schema_optional(self) -> Type[BaseModel]:
        """
        The pydantic schema for the model. This is the standard schema, but all fields are optional. Useful for POST and PUT requests.
        """
        if not self._schema_optional:
            cols = self.get_column_list() + self.get_property_column_list()
            if not self.with_fk:
                cols = [
                    col
                    for col in cols
                    if not self.is_fk(col) and not self.is_relation(col)
                ]
            self._schema_optional = self.generate_schema(cols, optional=True)
        return self._schema_optional

    @schema_optional.setter
    def schema_optional(self, value: Type[BaseModel]):
        self._schema_optional = value

    @property
    def list_columns(self) -> dict[str, Column]:
        if not self._list_columns:
            self._init_properties()
        return self._list_columns

    @list_columns.setter
    def list_columns(self, value: dict[str, Column]):
        self._list_columns = value

    @property
    def list_properties(self) -> dict[str, Column]:
        if not self._list_properties:
            self._init_properties()
        return self._list_properties

    @list_properties.setter
    def list_properties(self, value: dict[str, Column]):
        self._list_properties = value

    @property
    def filters(self) -> collections.defaultdict[str, list[BaseFilter]]:
        if not self._filters:
            self._init_filters()
        return self._filters

    @filters.setter
    def filters(self, value: collections.defaultdict[str, list[BaseFilter]]):
        self._filters = value

    @property
    def exclude_filters(self):
        """
        List of filters that should be excluded when using `QueryManager` to handle the filters.

        Returns:
            collections.defaultdict[str, list[str]]: A dictionary where the keys are column names and the values are lists of filters or strings.
        """
        if self._exclude_filters is None:
            self._exclude_filters = collections.defaultdict(list)
        return self._exclude_filters

    @exclude_filters.setter
    def exclude_filters(self, value: collections.defaultdict[str, list[str]]):
        self._exclude_filters = value

    """
    -----------------------------------------
            CONVERSION FUNCTIONS
    -----------------------------------------
    """

    @overload
    def convert_to_result(self, data: Model) -> Tuple[PRIMARY_KEY, Model]: ...
    @overload
    def convert_to_result(
        self, data: List[Model]
    ) -> Tuple[List[PRIMARY_KEY], List[Model]]: ...
    def convert_to_result(self, data: Model | List[Model]):
        """
        Converts the given data to a result tuple.

        Args:
            data (Model | List[Model]): The data to be converted.

        Returns:
            tuple: A tuple containing the primary key(s) and the converted data.

        """
        if isinstance(data, list):
            pks: PRIMARY_KEY = (
                [getattr(item, self.get_pk_attr()) for item in data]
                if not self.is_pk_composite()
                else [
                    [str(getattr(item, key)) for key in self.get_pk_attrs()]
                    for item in data
                ]
            )
        else:
            pks: PRIMARY_KEY = (
                getattr(data, self.get_pk_attr())
                if not self.is_pk_composite()
                else [str(getattr(data, key)) for key in self.get_pk_attrs()]
            )

        return (pks, data)

    """
    ------------------------------
     FUNCTIONS FOR RELATED MODELS
    ------------------------------
    """

    def get_col_default(self, col_name: str) -> Any:
        default = getattr(self.list_columns[col_name], "default", None)
        if default is None:
            return None

        value = getattr(default, "arg", None)
        if value is None:
            return None

        if getattr(default, "is_callable", False):
            return lambda: default.arg(None)

        if not getattr(default, "is_scalar", True):
            return None

        return value

    def get_related_model(self, col_name: str) -> Type[Model]:
        return self.list_properties[col_name].mapper.class_

    def get_related_interface(self, col_name: str, with_fk: bool | None = None):
        return self.__class__(self.get_related_model(col_name), with_fk)

    def get_related_fk(self, model: Type[Model]) -> Optional[str]:
        for col_name in self.list_properties.keys():
            if self.is_relation(col_name):
                if model == self.get_related_model(col_name):
                    return col_name
        return None

    def get_related_fks(self) -> List[str]:
        return [
            self.get_related_fk(model)
            for model in self.list_properties.values()
            if self.is_relation(model)
        ]

    def get_fk_column(self, relationship_name: str) -> str:
        """
        Get the foreign key column for the specified relationship.

        Args:
            relationship_name (str): The name of the relationship.

        Raises:
            Exception: If no foreign key is found for the specified relationship.

        Returns:
            str: The name of the foreign key column.
        """
        # Get the relationship property from the model's mapper
        relationship_prop = class_mapper(self.obj).relationships[relationship_name]

        # Iterate through the columns involved in the relationship
        for local_column, _ in relationship_prop.local_remote_pairs:
            # Check if the local column is the foreign key
            if local_column.foreign_keys:
                return local_column.name

        raise Exception(
            f"No foreign key found for relationship '{relationship_name}' in model '{self.obj.__name__}'."
        )

    def get_info(self, col_name: str):
        if col_name in self.list_properties:
            return self.list_properties[col_name].info
        return {}

    def get_columns_from_related_col(self, col: str, depth=1, prefix=""):
        prefix += f"{col}."
        interface = self.get_related_interface(col)
        columns = (
            interface.get_user_column_list() + interface.get_property_column_list()
        )
        columns = [f"{prefix}{sub_col}" for sub_col in columns]
        if depth > 1:
            related_cols = [
                x for x in interface.get_user_column_list() if interface.is_relation(x)
            ]
            for col in related_cols:
                columns += interface.get_columns_from_related_col(
                    col, depth - 1, prefix
                )
        return columns

    """
    -------------
     GET METHODS
    -------------
    """

    def get_column_list(self) -> List[str]:
        """
        Returns all model's columns on SQLA properties
        """
        return list(self.list_properties.keys())

    def get_user_column_list(self) -> List[str]:
        """
        Returns all model's columns except pk or fk
        """
        return [
            col_name
            for col_name in self.get_column_list()
            if (not self.is_pk(col_name)) and (not self.is_fk(col_name))
        ]

    def get_property_column_list(self) -> List[str]:
        """
        Returns all model's columns that have @property decorator and is public
        """
        self_dict = vars(self.obj)
        return [
            key
            for key in self_dict.keys()
            if self.is_property(key) and not key.startswith("_")
        ]

    def get_search_column_list(self) -> List[str]:
        ret_lst = []
        for col_name in self.get_column_list() + list(
            filter(
                lambda x: self.is_hybrid_property(x), self.get_property_column_list()
            )
        ):
            if not self.is_relation(col_name) and not self.is_hybrid_property(col_name):
                tmp_prop = self.get_property_first_col(col_name).name
                if (
                    (not self.is_pk(tmp_prop))
                    and (not self.is_fk(tmp_prop))
                    and (not self.is_image(col_name))
                    and (not self.is_file(col_name))
                ):
                    ret_lst.append(col_name)
            else:
                ret_lst.append(col_name)
        return ret_lst

    def get_order_column_list(self, list_columns: List[str], *, depth=0, max_depth=-1):
        """
        Get all columns that can be used for ordering

        Args:
            list_columns (List[str]): Columns to be used for ordering.
            depth (int, optional): Depth of the relation. Defaults to 0. Used for recursive calls.
            max_depth (int, optional): Maximum depth of the relation. When set to -1, it will be ignored. Defaults to -1.

        Returns:
            List[str]: List of columns that can be used for ordering
        """
        unique_order_columns: set[str] = set()
        for col_name in list_columns:
            if "." in col_name:
                col_name, sub_col_name = col_name.split(".", 1)
            else:
                sub_col_name = ""
            if self.is_relation(col_name):
                unique_order_columns.add(col_name)
                if (
                    (max_depth != -1 and depth >= max_depth)
                    or self.is_relation_one_to_many(col_name)
                    or self.is_relation_many_to_many(col_name)
                ):
                    continue
                related_interface = self.get_related_interface(col_name)
                sub_order_columns = related_interface.get_order_column_list(
                    [sub_col_name], depth=depth + 1, max_depth=max_depth
                )
                if sub_col_name:
                    sub_order_columns = [
                        x for x in sub_order_columns if x == sub_col_name
                    ]

                unique_order_columns.update(
                    [f"{col_name}.{sub_col}" for sub_col in sub_order_columns]
                )
                continue

            if self.is_hybrid_property(col_name):
                unique_order_columns.add(col_name)
                continue

            if self.is_property(col_name):
                continue

            if hasattr(self.obj, col_name):
                attribute = getattr(self.obj, col_name)
                if not callable(attribute) or hasattr(attribute, "_col_name"):
                    unique_order_columns.add(col_name)
            else:
                unique_order_columns.add(col_name)

        # Only take the columns that are in the list_columns
        result = [x for x in unique_order_columns if x in list_columns]

        # Order our result by the order of the list_columns
        return sorted(result, key=lambda x: list_columns.index(x))

    def get_file_column_list(self) -> List[str]:
        return [
            i.name
            for i in self.obj.__mapper__.columns
            if isinstance(i.type, FileColumn)
        ]

    def get_image_column_list(self) -> List[str]:
        return [
            i.name
            for i in self.obj.__mapper__.columns
            if isinstance(i.type, ImageColumn)
        ]

    def get_enum_value(self, col_name: str) -> enum.EnumType | list[str]:
        col_type = self.list_columns[col_name].type
        if isinstance(col_type.python_type, enum.EnumType):
            return col_type.python_type
        return col_type.enums

    def get_property_first_col(self, col_name: str) -> ColumnProperty:
        # support for only one col for pk and fk
        return self.list_properties[col_name].columns[0]

    def get_relation_fk(self, col_name: str) -> Column:
        # support for only one col for pk and fk
        return list(self.list_properties[col_name].local_columns)[0]

    """
    -----------------------------------------
         FUNCTIONS for Testing TYPES
    -----------------------------------------
    """

    def is_image(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, ImageColumn)
        except KeyError:
            return False

    def is_file(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, FileColumn)
        except KeyError:
            return False

    def is_string(self, col_name: str) -> bool:
        try:
            return is_sqla_type(
                self.list_columns[col_name].type, sa_types.String
            ) or is_sqla_type(self.list_columns[col_name].type, sa_types.UUID)
        except KeyError:
            return False

    def is_text(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Text)
        except KeyError:
            return False

    def is_binary(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.LargeBinary)
        except KeyError:
            return False

    def is_integer(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Integer)
        except KeyError:
            return False

    def is_numeric(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Numeric)
        except KeyError:
            return False

    def is_float(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Float)
        except KeyError:
            return False

    def is_boolean(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Boolean)
        except KeyError:
            return False

    def is_date(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Date)
        except KeyError:
            return False

    def is_datetime(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.DateTime)
        except KeyError:
            return False

    def is_enum(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.Enum)
        except KeyError:
            return False

    def is_json(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, sa_types.JSON)
        except KeyError:
            return False

    def is_jsonb(self, col_name: str) -> bool:
        try:
            return is_sqla_type(self.list_columns[col_name].type, postgresql.JSONB)
        except KeyError:
            return False

    def is_geometry(self, col_name: str) -> bool:
        try:
            from geoalchemy2 import Geometry

            return is_sqla_type(self.list_columns[col_name].type, Geometry)
        except KeyError:
            return False
        except ImportError:
            return False

    def is_relation(self, col_name: str) -> bool:
        try:
            return isinstance(self.list_properties[col_name], RelationshipProperty)
        except KeyError:
            return False

    def is_relation_many_to_one(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                return self.list_properties[col_name].direction.name == "MANYTOONE"
            return False
        except KeyError:
            return False

    def is_relation_many_to_many(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return relation.direction.name == "MANYTOMANY"
            return False
        except KeyError:
            return False

    def is_relation_many_to_many_special(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return relation.direction.name == "ONETOONE" and relation.uselist
            return False
        except KeyError:
            return False

    def is_relation_one_to_one(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return self.list_properties[col_name].direction.name == "ONETOONE" or (
                    relation.direction.name == "ONETOMANY" and relation.uselist is False
                )
            return False
        except KeyError:
            return False

    def is_relation_one_to_many(self, col_name: str) -> bool:
        try:
            if self.is_relation(col_name):
                relation = self.list_properties[col_name]
                return relation.direction.name == "ONETOMANY" and relation.uselist
            return False
        except KeyError:
            return False

    def is_nullable(self, col_name: str) -> bool:
        if self.is_relation_many_to_one(col_name):
            col = self.get_relation_fk(col_name)
            return col.nullable
        elif self.is_relation_many_to_many(col_name) or self.is_relation_one_to_many(
            col_name
        ):
            return True
        try:
            return self.list_columns[col_name].nullable
        except KeyError:
            return False

    def is_unique(self, col_name: str) -> bool:
        try:
            return self.list_columns[col_name].unique is True
        except KeyError:
            return False

    def is_pk(self, col_name: str) -> bool:
        try:
            return self.list_columns[col_name].primary_key
        except KeyError:
            return False

    def is_pk_composite(self) -> bool:
        return len(self.obj.__mapper__.primary_key) > 1

    def is_fk(self, col_name: str) -> bool:
        try:
            return self.list_columns[col_name].foreign_keys
        except KeyError:
            return False

    def is_property(self, col_name: str) -> bool:
        return hasattr(getattr(self.obj, col_name, None), "fget")

    def is_hybrid_property(self, col_name: str) -> bool:
        try:
            attr = getattr(self.obj, col_name)
            descriptor = getattr(attr, "descriptor")
            return isinstance(descriptor, hybrid_property)
        except AttributeError:
            return False

    def is_function(self, col_name: str) -> bool:
        return hasattr(getattr(self.obj, col_name, None), "__call__")

    def get_max_length(self, col_name: str) -> int:
        try:
            if self.is_enum(col_name):
                return -1
            col = self.list_columns[col_name]
            if col.type.length:
                return col.type.length
            else:
                return -1
        except Exception:
            return -1

    def _generate_schema_from_dict(self, schema_dict: dict[str, Any]):
        """
        Recursively generate a pydantic schema for the model from a dictionary created by `_generate_schema_from_columns`.

        Args:
            schema_dict (dict[str, Any]): The dictionary created by `_generate_schema_from_columns`.

        Returns:
            type[BaseModel]: The Pydantic schema for the model.
        """
        async_columns = schema_dict.pop("__async_columns__")
        model_name = schema_dict.pop("__name__", "")
        columns = schema_dict.pop("__columns__", None)
        with_name_ = schema_dict.pop("__with_name__", True)
        with_id_ = schema_dict.pop("__with_id__", True)
        optional = schema_dict.pop("__optional__", False)
        hide_sensitive_columns = schema_dict.pop("__hide_sensitive_columns__", True)
        with_fk = schema_dict.pop("__with_fk__", True)

        if not model_name:
            model_name = f"{self.obj.__name__}-Schema"
            if columns:
                model_name += f"-{'-'.join(columns)}"
            if with_name_:
                model_name += "-WithName"
            if with_id_:
                model_name += "-WithID"
            if optional:
                model_name += "-Optional"
            if hide_sensitive_columns:
                model_name += "-HideSensitive"
            if with_fk:
                model_name += "-WithFK"

        if async_columns:
            AsyncColumnHandler.add_async_validators(schema_dict, async_columns)

        if self.is_pk_composite():
            self.id_schema = str

        # Convert relationship schema to BaseModel
        for key, value in schema_dict.items():
            if key.startswith("__"):
                continue
            if isinstance(value, dict):
                sub_interface = self.get_related_interface(
                    key, bool(value.pop("__with_fk__", True))
                )
                params = {}
                type = sub_interface._generate_schema_from_dict(value) | None
                if self.is_relation_one_to_many(key) or self.is_relation_many_to_many(
                    key
                ):
                    type = list[type]
                if self.is_nullable(key) or optional:
                    params["default"] = None
                    type = type | None
                if self.get_max_length(key) != -1:
                    params["max_length"] = self.get_max_length(key)
                schema_dict[key] = (type, Field(**params))

        self._cache_schema[model_name] = create_model(model_name, **schema_dict)
        return self._cache_schema[model_name]

    def _generate_schema_from_columns(
        self,
        columns: List[str] | None = None,
        with_name_=True,
        with_id_=True,
        optional=False,
        name="",
        hide_sensitive_columns=True,
    ):
        """
        Recursively generate a pydantic schema for the model with the specified columns and options. If a column is a relation, the schema for the related model is generated as well.

        Args:
            columns (List[str] | None, optional): The list of columns to include in the schema. Defaults to None.
            with_name_ (bool, optional): Whether to include the name_ column. Defaults to True.
            with_id_ (bool, optional): Whether to include the id_ column. Defaults to True.
            optional (bool, optional): Whether the columns should be optional. Defaults to False.
            name (str, optional): The name of the schema. If not specified, the name is generated based on the object's name and the specified options. Defaults to ''.
            hide_sensitive_columns (bool, optional): Whether to hide sensitive columns such as `password`. Defaults to True.

        Returns:
            dict: The generated schema.
        """
        current_schema = {
            "__config__": ConfigDict(from_attributes=True),
            "__async_columns__": [],
            "__columns__": columns,
            "__with_name__": with_name_,
            "__with_id__": with_id_,
            "__optional__": optional,
            "__hide_sensitive_columns__": hide_sensitive_columns,
            "__with_fk__": self.with_fk,
        }
        if name:
            current_schema["__name__"] = name

        if with_name_:
            current_schema["name_"] = (str, Field())
        if with_id_:
            current_schema["id_"] = (PRIMARY_KEY, Field())

        if hide_sensitive_columns:
            sensitive_columns = g.sensitive_data.get(self.obj.__name__, [])
            columns = [col for col in columns if col not in sensitive_columns]

        prop_dict = self.list_properties if self.with_fk else self.list_columns
        for col in columns:
            sub_col = ""
            if "." in col:
                col, sub_col = col.split(".", 1)

            if self.is_relation(col):
                current_schema[col] = current_schema.get(
                    col,
                    {
                        "__config__": ConfigDict(from_attributes=True),
                        "__async_columns__": [],
                    },
                )

                sub_interface = self.get_related_interface(col, bool(sub_col))
                sub_with_name_ = current_schema[col].get("name_", not bool(sub_col))
                sub_with_id_ = current_schema[col].get("id_", not bool(sub_col))
                sub_columns = (
                    [
                        x
                        for x in sub_interface.get_column_list()
                        + sub_interface.get_property_column_list()
                        if not sub_interface.is_relation(x)
                        and not sub_interface.is_fk(x)
                    ]
                    if not sub_col
                    else [sub_col]
                )

                deep_merge(
                    current_schema[col],
                    sub_interface._generate_schema_from_columns(
                        sub_columns,
                        sub_with_name_,
                        sub_with_id_,
                        optional,
                        hide_sensitive_columns=hide_sensitive_columns,
                    ),
                )
            else:
                # Get column from properties
                column = prop_dict.get(col, None)
                # If column is not found, check if it is a property
                if column is None:
                    if self.is_property(col):
                        current_schema[col] = (typing.Any, Field(default=None))
                        if inspect.iscoroutinefunction(
                            getattr(getattr(self.obj, col), "fget")
                        ):
                            current_schema["__async_columns__"].append(col)
                    continue

                params = {}
                type = self.get_type(col)

                # Check if it is 'Geometry' type
                try:
                    from geoalchemy2 import Geometry

                    if type == Geometry:
                        geo_col = self.list_columns[col]
                        type = Annotated[
                            dict[str, typing.Any] | str,
                            BeforeValidator(
                                g.geometry_converter.two_way_converter_generator(
                                    geo_col.type.geometry_type
                                )
                            ),
                        ]
                except ImportError:
                    pass

                if hasattr(column, "primary_key") and column.primary_key:
                    self.id_schema = type
                if self.is_nullable(col) or optional:
                    params["default"] = None
                    type = type | None
                # if self.get_max_length(col) != -1:
                #     params["max_length"] = self.get_max_length(col)
                current_schema[col] = (type, Field(**params))

        return current_schema
