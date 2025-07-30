import typing
from datetime import date, datetime

from ..filters import BaseFilter
from .session import GenericSession

if typing.TYPE_CHECKING:
    from .db import GenericQueryManager
    from .interface import GenericInterface

__all__ = [
    "GenericBaseFilter",
    "GenericFilterTextContains",
    "GenericFilterStartsWith",
    "GenericFilterNotStartsWith",
    "GenericFilterEndsWith",
    "GenericFilterNotEndsWith",
    "GenericFilterContains",
    "GenericFilterIContains",
    "GenericFilterNotContains",
    "GenericFilterEqual",
    "GenericFilterNotEqual",
    "GenericFilterGreater",
    "GenericFilterSmaller",
    "GenericFilterGreaterEqual",
    "GenericFilterSmallerEqual",
    "GenericFilterIn",
    "GenericFilterConverter",
]


class GenericBaseFilter(BaseFilter):
    datamodel: "GenericInterface" = None
    query: "GenericQueryManager" = None

    def apply(self, session: GenericSession, col: str, value) -> GenericSession:
        value = self._cast_value(col, value)
        return super().apply(session, col, value)


class GenericFilterTextContains(GenericBaseFilter):
    name = "Text contains"
    arg_name = "tc"

    def apply(self, session, col, value):
        value = self._cast_value(col, value)
        return session.text_contains(col, value)


class GenericFilterStartsWith(GenericBaseFilter):
    name = "Starts with"
    arg_name = "sw"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.starts_with(col, value)


class GenericFilterNotStartsWith(GenericBaseFilter):
    name = "Not Starts with"
    arg_name = "nsw"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.not_starts_with(col, value)


class GenericFilterEndsWith(GenericBaseFilter):
    name = "Ends with"
    arg_name = "ew"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.ends_with(col, value)


class GenericFilterNotEndsWith(GenericBaseFilter):
    name = "Not Ends with"
    arg_name = "new"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.not_ends_with(col, value)


class GenericFilterContains(GenericBaseFilter):
    name = "Contains"
    arg_name = "ct"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.like(col, value)


class GenericFilterIContains(GenericBaseFilter):
    name = "Contains (insensitive)"
    arg_name = "ict"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.ilike(col, value)


class GenericFilterNotContains(GenericBaseFilter):
    name = "Not Contains"
    arg_name = "nct"

    def apply(self, session, col: str, value):
        value = self._cast_value(col, value)
        return session.not_like(col, value)


class GenericFilterEqual(GenericBaseFilter):
    name = "Equal to"
    arg_name = "eq"

    def apply(
        self,
        session,
        col: str,
        value: str | bool | int | date | datetime,
    ):
        value = self._cast_value(col, value)
        return session.equal(col, value)


class GenericFilterNotEqual(GenericBaseFilter):
    name = "Not Equal to"
    arg_name = "neq"

    def apply(
        self,
        session,
        col: str,
        value: str | bool | int | date | datetime,
    ):
        value = self._cast_value(col, value)
        return session.not_equal(col, value)


class GenericFilterGreater(GenericBaseFilter):
    name = "Greater than"
    arg_name = "gt"

    def apply(self, session, col: str, value: int | date | datetime):
        value = self._cast_value(col, value)
        return session.greater(col, value)


class GenericFilterSmaller(GenericBaseFilter):
    name = "Smaller than"
    arg_name = "lt"

    def apply(self, session, col: str, value: int | date | datetime):
        value = self._cast_value(col, value)
        return session.smaller(col, value)


class GenericFilterGreaterEqual(GenericBaseFilter):
    name = "Greater equal"
    arg_name = "ge"

    def apply(self, session, col: str, value: int | date | datetime):
        value = self._cast_value(col, value)
        return session.greater_equal(col, value)


class GenericFilterSmallerEqual(GenericBaseFilter):
    name = "Smaller equal"
    arg_name = "le"

    def apply(self, session, col: str, value: int | date | datetime):
        value = self._cast_value(col, value)
        return session.smaller_equal(col, value)


class GenericFilterIn(GenericBaseFilter):
    name = "One of"
    arg_name = "in"

    def apply(self, session, col: str, value: list[str | bool | int]):
        value = self._cast_value(col, value)
        return session.in_(col, value)


class GenericFilterConverter:
    """
    Helper class to get available filters for a generic column type.
    """

    conversion_table = (
        (
            "is_enum",
            [
                GenericFilterTextContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_boolean",
            [GenericFilterEqual, GenericFilterNotEqual, GenericFilterTextContains],
        ),
        (
            "is_text",
            [
                GenericFilterTextContains,
                GenericFilterStartsWith,
                GenericFilterNotStartsWith,
                GenericFilterEndsWith,
                GenericFilterNotEndsWith,
                GenericFilterContains,
                GenericFilterIContains,
                GenericFilterNotContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_string",
            [
                GenericFilterTextContains,
                GenericFilterStartsWith,
                GenericFilterNotStartsWith,
                GenericFilterEndsWith,
                GenericFilterNotEndsWith,
                GenericFilterContains,
                GenericFilterIContains,
                GenericFilterNotContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_integer",
            [
                GenericFilterTextContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterGreater,
                GenericFilterSmaller,
                GenericFilterGreaterEqual,
                GenericFilterSmallerEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_date",
            [
                GenericFilterTextContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterGreater,
                GenericFilterSmaller,
                GenericFilterGreaterEqual,
                GenericFilterSmallerEqual,
                GenericFilterIn,
            ],
        ),
        (
            "is_datetime",
            [
                GenericFilterTextContains,
                GenericFilterEqual,
                GenericFilterNotEqual,
                GenericFilterGreater,
                GenericFilterSmaller,
                GenericFilterGreaterEqual,
                GenericFilterSmallerEqual,
                GenericFilterIn,
            ],
        ),
    )
