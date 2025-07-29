import datetime
import typing
from enum import Enum
from typing import List

from pydantic import EmailStr

from ..api import SQLAInterface
from .filters import GenericBaseFilter, GenericFilterConverter
from .model import GenericColumn, GenericModel
from .session import GenericSession

__all__ = ["GenericInterface"]


class GenericInterface(SQLAInterface):
    """
    Represents an interface for a Generic model (Based on pydantic).
    """

    # Overloaded attributes
    obj: typing.Type[GenericModel]
    filter_converter: GenericFilterConverter = GenericFilterConverter()
    with_fk: bool = True
    list_columns: dict[str, GenericColumn]
    list_properties: dict[str, GenericColumn]
    _filters: dict[str, list[GenericBaseFilter]] = None

    # Generic attributes
    session: typing.Type[GenericSession] = None

    def __init__(
        self, obj: typing.Type[GenericModel], session: typing.Type[GenericSession]
    ):
        if not isinstance(session, type):
            raise ValueError("session must be a class, do not instantiate it")
        self.session = session
        super().__init__(obj)

    def get_type(self, col: str):
        return self.obj.properties[col].col_type

    def get_type_name(self, col: str) -> str:
        if self.is_string(col):
            return "String"
        if self.is_integer(col):
            return "Integer"
        if self.is_boolean(col):
            return "Boolean"
        if self.is_date(col):
            return "DateTime"
        return "Raw"

    def _init_properties(self):
        self._list_columns = self.obj.properties
        self._list_properties = self.obj.properties

    """
    ------------------------------
     FUNCTIONS FOR RELATED MODELS
    ------------------------------
    """

    def get_related_model(self, col_name: str) -> typing.Type[GenericModel]:
        if self.is_relation(col_name):
            return self.list_properties[col_name].__class__

        raise ValueError(f"{col_name} is not a relation")

    """
    -------------
     GET METHODS
    -------------
    """

    def get_search_column_list(self) -> List[str]:
        return [x for x in self.obj.columns if not self.is_pk(x)]

    def get_file_column_list(self) -> List[str]:
        return []

    def get_image_column_list(self) -> List[str]:
        return []

    """
    -----------------------------------------
         FUNCTIONS for Testing TYPES
    -----------------------------------------
    """

    def is_image(self, col_name: str) -> bool:
        return False

    def is_file(self, col_name: str) -> bool:
        return False

    def is_string(self, col_name: str) -> bool:
        return (
            self.obj.properties[col_name].col_type is str
            or self.obj.properties[col_name].col_type == EmailStr
        )

    def is_text(self, col_name: str) -> bool:
        return self.is_string(col_name)

    def is_binary(self, col_name: str) -> bool:
        return False

    def is_integer(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type is int

    def is_numeric(self, col_name: str) -> bool:
        return self.is_integer(col_name)

    def is_float(self, col_name: str) -> bool:
        return self.is_integer(col_name)

    def is_boolean(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type is bool

    def is_date(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == datetime.date

    def is_datetime(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == datetime.datetime

    def is_enum(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == Enum

    def is_json(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type is dict

    def is_jsonb(self, col_name):
        return self.is_json(col_name)

    def is_relation(self, col_name: str) -> bool:
        return self.is_relation_one_to_one(col_name) or self.is_relation_one_to_many(
            col_name
        )

    def is_relation_many_to_one(self, col_name: str) -> bool:
        # TODO: AS OF NOW, cant detect
        return False

    def is_relation_many_to_many(self, col_name: str) -> bool:
        # TODO: AS OF NOW, cant detect
        return False

    def is_relation_many_to_many_special(self, col_name: str) -> bool:
        return False

    def is_relation_one_to_one(self, col_name: str) -> bool:
        return isinstance(self.list_properties[col_name], GenericModel)

    def is_relation_one_to_many(self, col_name: str) -> bool:
        if not isinstance(self.list_properties[col_name], list):
            return False
        for prop in self.list_properties[col_name]:
            if not isinstance(prop, GenericModel):
                return False

        return True

    def is_pk_composite(self) -> bool:
        return False

    def is_fk(self, col_name: str) -> bool:
        return False

    def get_max_length(self, col_name: str) -> int:
        return -1
