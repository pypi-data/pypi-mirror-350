import typing

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    create_model,
    model_validator,
)

from ..utils import T
from .exceptions import ColumnInvalidTypeException, GenericColumnException

if typing.TYPE_CHECKING:
    from .model import GenericModel

__all__ = ["GenericColumn"]


class ColumnPlaceholder:
    def __repr__(self) -> str:
        return str(None)


class PKAutoIncrement(ColumnPlaceholder): ...


class NoDefault(ColumnPlaceholder): ...


class GenericProperty(typing.Generic[T]):
    col_type: typing.Type[T]
    primary_key: bool
    auto_increment: bool
    unique: bool
    nullable: bool
    default: T | NoDefault


class PydanticGenericColumn(BaseModel, GenericProperty[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    col_type: T
    primary_key: bool
    auto_increment: bool
    unique: bool
    nullable: bool
    default: T | NoDefault

    @model_validator(mode="after")
    def check_column(self) -> typing.Self:
        if self.primary_key and not isinstance(self.default, NoDefault):
            raise GenericColumnException(
                self, "Primary key columns cannot have a default value"
            )

        if not self.primary_key and self.auto_increment:
            raise GenericColumnException(
                self, "Auto increment can only be set on primary key columns"
            )

        if self.auto_increment and self.col_type is not int:
            raise GenericColumnException(
                self, "Primary key with auto increment must be of type int"
            )

        if self.primary_key:
            self.unique = True
            self.nullable = False

        return self


class GenericColumn(GenericProperty[T]):
    """
    A generic column for `GenericModel`. This works similar to a SQLAlchemy column.

    Args:
        col_type (Type[T]): The type of the column.
        primary_key (bool, optional): Whether the column is a primary key. Defaults to False.
        auto_increment (bool, optional): Whether the column is auto incremented. Only works if the column is a primary key. Defaults to False.
        unique (bool, optional): Whether the column is unique. Defaults to False.
        nullable (bool, optional): Whether the column is nullable. Defaults to True.
        default (T | NoDefault, optional): The default value of the column. Will be used if the column is not set by the user. Defaults to NoDefault (no default value).
    """

    validation_model: BaseModel = None
    _col_name: str = None

    def __init__(
        self,
        col_type: typing.Type[T],
        *,
        primary_key: bool = False,
        auto_increment: bool = False,
        unique: bool = False,
        nullable: bool = True,
        default: T | NoDefault = NoDefault(),
    ):
        model = PydanticGenericColumn(
            col_type=col_type,
            primary_key=primary_key,
            auto_increment=auto_increment,
            unique=unique,
            nullable=nullable,
            default=default,
        )
        self.col_type = model.col_type
        self.primary_key = model.primary_key
        self.auto_increment = model.auto_increment
        self.unique = model.unique
        self.nullable = model.nullable
        self.default = model.default
        # TODO: Handle self.unique

    @typing.overload
    def __get__(
        self, instance: None, owner: typing.Type["GenericModel"]
    ) -> "GenericColumn": ...
    @typing.overload
    def __get__(
        self, instance: "GenericModel", owner: typing.Type["GenericModel"]
    ) -> T | None: ...
    def __get__(
        self,
        instance: typing.Optional["GenericModel"],
        owner: typing.Type["GenericModel"],
    ):
        if not instance:
            return self

        value: T | NoDefault = instance.__dict__.get(f"_{self._col_name}", NoDefault())
        if not isinstance(value, NoDefault):
            return value
        if self.nullable:
            return None
        if self.primary_key and self.auto_increment:
            return PKAutoIncrement()
        return self.default

    def __set__(self, instance: "GenericModel", value: T | NoDefault) -> None:
        try:
            validated = self.validation_model.model_validate({self._col_name: value})
        except ValidationError as e:
            raise ColumnInvalidTypeException(
                instance, f"Invalid type for column {self._col_name}, {str(e)}"
            )
        instance.__dict__[f"_{self._col_name}"] = getattr(validated, self._col_name)

    def __set_name__(self, owner: typing.Type["GenericModel"], name: str) -> None:
        self._col_name = name

        # Create pydantic model for validation
        validation_type = self.col_type
        if self.nullable:
            validation_type = validation_type | None
        if not isinstance(self.default, NoDefault):
            validation_type = validation_type | type(self.default)
            validation_field = Field(default=self.default)
        else:
            validation_field = Field

        self.validation_model = create_model(
            owner.__name__,
            **{name: (validation_type, validation_field)},
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"GenericColumn({self.col_type.__name__}, primary_key={self.primary_key}, auto_increment={self.auto_increment}, unique={self.unique}, nullable={self.nullable}, default={self.default})"
