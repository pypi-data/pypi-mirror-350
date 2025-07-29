import csv
import enum
import inspect
import json
import os
import re
import secrets
import sys
import typing
import unicodedata
import uuid
from datetime import datetime, timezone
from types import FunctionType
from typing import Any, Awaitable, Callable, Coroutine, Dict, NotRequired, Type, Union

import pydantic
import sqlalchemy.types as sa_types
from fastapi import Depends, UploadFile
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field, create_model
from sqlalchemy import Column
from starlette.concurrency import P, T

from .types import ExportMode

__all__ = [
    "ExtenderMixin",
    "SelfDepends",
    "SelfType",
    "CSVJSONConverter",
    "Line",
    "merge_schema",
    "update_signature",
    "uuid_namegen",
    "secure_filename",
    "ensure_tz_info",
    "validate_utc",
    "smart_run",
    "safe_call",
    "ImportStringError",
    "import_string",
    "is_sqla_type",
    "generate_schema_from_typed_dict",
    "prettify_dict",
    "call_with_valid_kwargs",
    "deep_merge",
    "use_default_when_none",
]

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(10)),
    *(f"LPT{i}" for i in range(10)),
}


class ExtenderMixin:
    """
    A utility class that can be used to extend the attributes of the parent classes.

    When a class inherits from this class, it will take all the non-private attributes of the child class and add them to the parent classes.

    Can also be combined with a class that is a subclass of `Model` from `fastapi_rtk.model` to add new columns when modifying the actual class is not possible.

    ### Example:

    ```python
    class Parent:
        parent_attr = "parent"

    class Child(ExtendingModel, Parent):
        child_attr = "child"

    print(Parent.parent_attr)  # Output: "parent"
    print(Parent.child_attr)  # Output: "child"
    ```
    """

    def __init_subclass__(cls) -> None:
        if ExtenderMixin in cls.__bases__:
            copy_vars = {
                k: v
                for k, v in vars(cls).items()
                if not k == "__module__" and not k == "__doc__"
            }
            cls._extend_parents(**copy_vars)
        return super().__init_subclass__()

    @classmethod
    def _extend_parents(cls, **kwargs):
        for base in cls.__bases__:
            if base is ExtenderMixin:
                continue
            for k, v in kwargs.items():
                setattr(base, k, v)
            if hasattr(base, "_extend_parents"):
                base._extend_parents(**kwargs)


class BaseSelf:
    attr: str | None = None
    ignored_keys: list[str] = None

    def __init__(self) -> None:
        self.ignored_keys = ["attr", "__class__"]

    def __getattribute__(self, name: str) -> Any:
        # Special handling for when name is "ignored_keys" or in self.ignored_keys
        if name == "ignored_keys" or name in self.ignored_keys:
            return super().__getattribute__(name)

        # If attr is not set, set attr to the attribute name
        curr_attr = self.attr
        if curr_attr is None:
            curr_attr = ""
        curr_attr += f".{name}" if curr_attr else name
        self.attr = curr_attr

        return self

    def __call__(self, cls) -> Any:
        split = self.attr.split(".")
        result = None
        for attr in split:
            result = getattr(result or cls, attr)
        return result


class SelfDepends(BaseSelf):
    """
    A class that can be used to create a dependency that depends on the class instance.

    Sometimes you need to create a dependency that requires the class instance to be passed as a parameter when using Depends() from FastAPI. This class can be used to create such dependencies.

    ### Example:

    ```python
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, permissions: List[str] = SelfDepends().get_current_permissions):
                # Do something
                pass

            def get_current_permissions(self):
                # Do something that requires the class instance, and should returns a function that can be used as a dependency
                pass
    ```

    is equivalent to:

    ```python
        # self. is actually not possible here, that's why we use the string representation of the attribute
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, permissions: List[str] = Depends(self.get_current_permissions)):
                # Do something
                pass

            def get_current_permissions(self):
                # Do something that requires the class instance, and should returns a function that can be used as a dependency
                pass
    ```
    """

    args = None
    kwargs = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.ignored_keys.append("args")
        self.ignored_keys.append("kwargs")
        self.args = args or ()
        self.kwargs = kwargs or {}

    def __call__(self, cls) -> Any:
        result = super().__call__(cls)
        return Depends(result(*self.args, **self.kwargs))


class SelfType(BaseSelf):
    """
    A class that can be used to create a dependency that depends on the class instance.

    Sometimes you need to create a type that depends on the class instance. This class can be used to create such types.

    ### Example:

    ```python
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, schema: BaseModel = SelfType().datamodel.obj.schema):
                # Do something
                pass

            @expose("/my_other_endpoint")
            def my_other_endpoint(self, schema: BaseModel = SelfType.with_depends().datamodel.obj.schema):
                # Do something
                pass
    ```

    is equivalent to:

    ```python
        # self. is actually not possible here, that's why we use the string representation of the attribute
        class MyApi:
            @expose("/my_endpoint")
            def my_endpoint(self, schema: self.datamodel.obj.schema):
                # Do something
                pass

            @expose("/my_other_endpoint")
            def my_other_endpoint(self, schema: self.datamodel.obj.schema = Depends()):
                # Do something
                pass
    ```
    """

    depends = False

    def __init__(self, depends: bool = False) -> None:
        super().__init__()
        self.ignored_keys.append("depends")
        self.depends = depends
        self.attr = None

    @classmethod
    def with_depends(cls):
        return cls(depends=True)


class CSVJSONConverter:
    """
    A utility class for converting CSV data to JSON format and vice versa.
    """

    @classmethod
    def csv_to_json(
        cls,
        csv_data: str | bytes,
        *,
        delimiter=",",
        quotechar: str | None = None,
    ):
        """
        Converts CSV data to JSON format.

        Args:
            csv_data (str, bytes): The CSV data.
            delimiter (str, optional): The delimiter to use in the CSV. Defaults to ",".
            quotechar (str | None, optional): Quote character for the CSV file. If not given, it will not be used. Defaults to None.

        Returns:
            list[dict[str, Any]]: The JSON data as a list of dictionaries.
        """
        if isinstance(csv_data, bytes):
            csv_data = csv_data.decode("utf-8")

        lines = csv_data.splitlines()
        reader = csv.DictReader(lines, delimiter=delimiter, quotechar=quotechar)
        return [
            cls._convert_nested_col_into_dict(
                row, list_delimiter=";" if delimiter != ";" else ","
            )
            for row in reader
        ]

    @classmethod
    def json_to_csv(
        cls,
        data: dict[str, typing.Any] | list[dict[str, typing.Any]],
        /,
        *,
        list_columns: list[str],
        label_columns: dict[str, str],
        with_header=True,
        delimiter=",",
        quotechar: str | None = None,
        relation_separator: str = ".",
        export_mode: ExportMode = "simplified",
    ):
        """
        Converts JSON data to CSV format.

        Args:
            data (dict[str, Any] | list[dict[str, Any]]): The JSON data to be converted.
            list_columns (list[str]): The list of columns to be included in the CSV.
            label_columns (dict[str, str]): The mapping of column names to labels.
            with_header (bool, optional): Whether to include the header in the CSV. Defaults to True.
            delimiter (str, optional): The delimiter to use in the CSV. Defaults to ",".
            quotechar (str | None, optional): Quote character for the CSV file. If not given, it will not be used. Defaults to None.
            relation_separator (str, optional): The separator to use for nested keys. Defaults to ".".
            export_mode (ExportMode, optional): Export mode (simplified or detailed). Defaults to "simplified".

        Returns:
            str: The CSV data as a string.
        """
        csv_data = ""
        line = Line()
        writer = csv.writer(line, delimiter=delimiter, quotechar=quotechar)

        if with_header:
            header = [label_columns[col] for col in list_columns]
            writer.writerow(header)
            csv_data = line.read()

        if isinstance(data, dict):
            data = [data]

        for item in data:
            row = cls._json_to_csv(
                item,
                list_columns=list_columns,
                delimiter=delimiter,
                relation_separator=relation_separator,
                export_mode=export_mode,
            )
            writer.writerow(row)
            csv_data += line.read()

        return csv_data.strip()

    @classmethod
    def _json_to_csv(
        self,
        data: dict[str, Any],
        /,
        *,
        list_columns: list[str],
        delimiter=",",
        relation_separator=".",
        export_mode: ExportMode = "simplified",
    ):
        """
        Converts single JSON object to CSV format.

        Args:
            data (dict[str, Any]): The JSON data to be converted.
            list_columns (list[str]): The list of columns to be included in the CSV.
            delimiter (str, optional): The delimiter to use in the CSV. Defaults to ",".
            relation_separator (str, optional): The separator to use for nested keys. Defaults to ".".
            export_mode (ExportMode, optional): Export mode (simplified or detailed). Defaults to "simplified".

        Returns:
            str: The CSV data as a string.
        """
        csv_data: list[str] = []

        for col in list_columns:
            sub_col = []
            if relation_separator in col:
                col, *sub_col = col.split(relation_separator)
            curr_val = data.get(col, "")
            for sub in sub_col:
                if isinstance(curr_val, dict):
                    curr_val = curr_val.get(sub, "")
                else:
                    curr_val = ""

            if isinstance(curr_val, dict):
                curr_val = curr_val.get("name_", curr_val)
            elif isinstance(curr_val, list):
                curr_val = [
                    curr_val.get(
                        "id_" if export_mode == "detailed" else "name_", curr_val
                    )
                    for curr_val in curr_val
                ]
                array_separator = "," if delimiter == ";" else ";"
                curr_val = array_separator.join(curr_val)
            elif isinstance(curr_val, enum.Enum):
                curr_val = curr_val.value
            if curr_val is not None:
                if isinstance(curr_val, dict):
                    curr_val = json.dumps(curr_val)
                else:
                    curr_val = str(curr_val)
            else:
                curr_val = ""
            csv_data.append(curr_val)

        return csv_data

    @classmethod
    def _convert_nested_col_into_dict(
        cls, data: dict[str, Any], /, *, separator: str = ".", list_delimiter: str = ";"
    ):
        """
        Converts nested columns in a dictionary into a nested dictionary.

        Args:
            data (dict[str, Any]): The dictionary to be converted.
            separator (str, optional): Separator used to split the keys into nested dictionaries. Defaults to ".".
            list_delimiter (str, optional): Delimiter used to join list values. Defaults to ";"

        Returns:
            dict[str, Any]: The converted dictionary with nested keys.

        Example:
        ```python
            data = {
                "name": "Alice",
                "age": 30,
                "address.city": "New York",
                "address.state": "NY",
            }
            result = CSVJSONConverter._convert_nested_col_into_dict(data)
            # result = {
            #     "name": "Alice",
            #     "age": 30,
            #     "address": {
            #         "city": "New York",
            #         "state": "NY"
            #     }
            # }
        ```
        """
        result: dict[str, typing.Any] = {}
        for key, value in data.items():
            parts = key.strip().split(separator)
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value

            if list_delimiter in value:
                value = value.split(list_delimiter)
                current[parts[-1]] = [item.strip() for item in value if item.strip()]
        return result


class Line:
    _line = ""

    def write(self, line: str):
        self._line = line

    def read(self):
        return self._line


def merge_schema(
    schema: BaseModel,
    fields: Dict[str, tuple[type, pydantic.fields.FieldInfo]],
    only_update=False,
    name: str | None = None,
) -> Type[BaseModel]:
    """
    Replace or add fields to the given schema.

    Args:
        schema (BaseModel): The schema to be updated.
        fields (Dict[str, tuple[type, Field]]): The fields to be added or updated.
        only_update (bool): If True, only update the fields with the same name. Otherwise, add new fields.
        name (str, optional): The name of the new schema. If not given, the schema name will be suffixed with a random hex string. Defaults to None.

    Returns:
        BaseModel: The updated schema.
    """
    name = name or f"{schema.__name__}-{secrets.token_hex(3)}"
    new_fields = dict()
    if only_update:
        for key, value in schema.model_fields.items():
            if key in fields:
                val = fields[key]
                if isinstance(val, tuple):
                    new_fields[key] = val
                else:
                    new_fields[key] = (value.annotation, val)
    else:
        new_fields = fields

    return create_model(
        name,
        **new_fields,
        __base__=schema,
    )


def copy_function(f):
    """Copy a function."""
    return FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__,
    )


def update_signature(cls, f):
    """
    Copy a function and update its signature to include the class instance as the first parameter instead of string "self" for FastAPI Route Dependencies.

    It also replaces SelfDepends and SelfType with the actual value.

    Args:
        f (Callable): The function to be updated.
    Returns:
        Callable: The updated function.
    """
    # Get the function's parameters
    old_signature = inspect.signature(f)
    old_parameters = list(old_signature.parameters.values())
    if not old_parameters:
        return f
    old_first_parameter, *old_parameters = old_parameters

    # If the first parameter is self, replace it
    if old_first_parameter.name == "self":
        new_first_parameter = old_first_parameter.replace(default=Depends(lambda: cls))

        new_parameters = [new_first_parameter]
        for parameter in old_parameters:
            parameter = parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
            if isinstance(parameter.default, SelfDepends):
                parameter = parameter.replace(default=parameter.default(cls))
            elif isinstance(parameter.default, SelfType):
                parameter = parameter.replace(
                    annotation=parameter.default(cls),
                    default=(
                        Depends()
                        if parameter.default.depends
                        else inspect.Parameter.empty
                    ),
                )
            new_parameters.append(parameter)

        new_signature = old_signature.replace(parameters=new_parameters)

        # Copy the function to avoid modifying the original
        f = copy_function(f)

        setattr(
            f, "__signature__", new_signature
        )  # Set the new signature to the function

    return f


def uuid_namegen(file_data: UploadFile) -> str:
    """
    Generates a unique filename by combining a UUID and the original filename.

    Args:
        file_data (File): The file data object.

    Returns:
        str: The generated unique filename.
    """
    return str(uuid.uuid1()) + "_sep_" + file_data.filename


def secure_filename(filename: str) -> str:
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.

    .. versionadded:: 0.5

    :param filename: the filename to secure
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename


def ensure_tz_info(dt: datetime | str) -> datetime:
    """Ensure that the datetime has a timezone info."""
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def validate_utc(dt: datetime) -> datetime:
    """Validate that the datetime is in UTC."""
    if dt.tzinfo.utcoffset(dt) != timezone.utc.utcoffset(dt):
        raise ValueError("Timezone must be UTC")
    return dt


async def smart_run(
    func: Callable[P, Union[T, Awaitable[T]]], *args: P.args, **kwargs: P.kwargs
) -> T:
    """
    A utility function that can run a function either as a coroutine or in a threadpool.

    Args:
        func: The function to be executed.
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Returns:
        The result of the function execution.

    Raises:
        Any exceptions raised by the function.

    """
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return await run_in_threadpool(func, *args, **kwargs)


async def safe_call(coro: Coroutine[Any, Any, T] | T) -> T:
    """
    A utility function that can await a coroutine or return a non-coroutine object.

    Args:
        coro (Any): The function call or coroutine to be awaited.

    Returns:
        The result of the function call or coroutine.
    """
    if isinstance(coro, Coroutine):
        return await coro
    return coro


class ImportStringError(ImportError):
    """
    COPIED FROM WERKZEUG LIBRARY

    Provides information about a failed :func:`import_string` attempt.
    """

    #: String in dotted notation that failed to be imported.
    import_name: str
    #: Wrapped exception.
    exception: BaseException

    def __init__(self, import_name: str, exception: BaseException) -> None:
        self.import_name = import_name
        self.exception = exception
        msg = import_name
        name = ""
        tracked = []
        for part in import_name.replace(":", ".").split("."):
            name = f"{name}.{part}" if name else part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, "__file__", None)))
            else:
                track = [f"- {n!r} found in {i!r}." for n, i in tracked]
                track.append(f"- {name!r} not found.")
                track_str = "\n".join(track)
                msg = (
                    f"import_string() failed for {import_name!r}. Possible reasons"
                    f" are:\n\n"
                    "- missing __init__.py in a package;\n"
                    "- package or module path not included in sys.path;\n"
                    "- duplicated package or module name taking precedence in"
                    " sys.path;\n"
                    "- missing module, class, function or variable;\n\n"
                    f"Debugged import:\n\n{track_str}\n\n"
                    f"Original exception:\n\n{type(exception).__name__}: {exception}"
                )
                break

        super().__init__(msg)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}({self.import_name!r}, {self.exception!r})>"


def import_string(import_name: str, silent: bool = False) -> Any:
    """
    COPIED FROM WERKZEUG LIBRARY

    Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    import_name = import_name.replace(":", ".")
    try:
        try:
            __import__(import_name)
        except ImportError:
            if "." not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit(".", 1)
        module = __import__(module_name, globals(), locals(), [obj_name])
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e) from None

    except ImportError as e:
        if not silent:
            raise ImportStringError(import_name, e).with_traceback(
                sys.exc_info()[2]
            ) from None

    return None


def is_sqla_type(col: Column, sa_type: Type[sa_types.TypeEngine]) -> bool:
    """
    Check if the column is an instance of the given SQLAlchemy type.

    Args:
        col (Column): The SQLAlchemy Column to check.
        sa_type (Type[sa_types.TypeEngine]): The SQLAlchemy type to check against.

    Returns:
        bool: True if the column is an instance of the given SQLAlchemy type, False otherwise.
    """
    return (
        isinstance(col, sa_type)
        or isinstance(col, sa_types.TypeDecorator)
        and isinstance(col.impl, sa_type)
    )


def generate_schema_from_typed_dict(typed_dict: type):
    """
    Generate a Pydantic model schema from a TypedDict.
    Args:
        typed_dict (type): A type that is a subclass of dict, typically a TypedDict.
    Returns:
        BaseModel: A Pydantic model generated from the TypedDict.
    Raises:
        TypeError: If the provided typed_dict is not a type or not a subclass of dict.
    """
    if not isinstance(typed_dict, type) or not issubclass(typed_dict, dict):
        raise TypeError("typed_dict must be a type that is a subclass of dict")

    fields = {}
    for key, val in typed_dict.__annotations__.items():
        if getattr(val, "__origin__", None) is NotRequired:
            fields[key] = (val.__args__[0], Field(None))
        else:
            fields[key] = (val, Field(...))
    return create_model(typed_dict.__name__, **fields)


def prettify_dict(d: Dict[str, Any], indent: int = 0) -> str:
    """
    Prettify a dictionary to a string.

    Args:
        d (Dict[str, Any]): The dictionary to be prettified.
        indent (int, optional): The number of spaces to indent each level. Defaults to 0.

    Returns:
        str: The prettified dictionary as a string.
    """
    result = ""
    for key, value in d.items():
        result += " " * indent + f"{key}: "
        if isinstance(value, dict):
            result += "\n" + prettify_dict(value, indent + 2)
        else:
            result += f"{value}\n"
    return result


def call_with_valid_kwargs(func: Callable[..., T], params: Dict[str, Any]):
    """
    Call a function with valid keyword arguments. If a required parameter is missing, raise an error.

    Args:
        func (Callable[..., T]): The function to be called.
        params (Dict[str, Any]): The parameters to be passed to the function as keyword arguments.

    Raises:
        ValueError: If a required parameter is missing. The error message will contain the missing parameter and the given parameters.

    Returns:
        T: The result of the function call.
    """
    valid_kwargs: Dict[str, Any] = {}
    for [parameter_name, parameter_info] in inspect.signature(func).parameters.items():
        if parameter_name in params:
            valid_kwargs[parameter_name] = params[parameter_name]
        else:
            # Throw error if required parameter is missing
            if parameter_info.default == inspect.Parameter.empty:
                raise ValueError(
                    f"Parameter `{parameter_name}` does not exist in given parameters! Given parameters are:\n{prettify_dict(params, 2)}"
                )
    return func(**valid_kwargs)


def deep_merge(
    base_data: typing.Dict[str, typing.Any],
    additional_data: typing.Dict[str, typing.Any],
    rules: typing.Dict[str, typing.Callable[[typing.Any, typing.Any], bool]]
    | None = None,
):
    """
    Recursively merges the contents of `additional_data` into `base_data`.

    If a key in `additional_data` corresponds to a dictionary in both `base_data` and `additional_data`,
    the function will recursively merge the dictionaries. If the key corresponds to a list in both,
    the lists will be concatenated. For all other types, the value from `additional_data` will overwrite
    the value in `base_data`.

    Args:
        base_data (typing.Dict[str, typing.Any]): The dictionary to be updated.
        additional_data (typing.Dict[str, typing.Any]): The dictionary whose contents will be merged into `base_data`.
        rules (typing.Dict[str, typing.Callable[[typing.Any, typing.Any], bool]] | None, optional): A dictionary of rules to apply when merging values. If a key in `additional_data` corresponds to a key in `rules`, the rule will be applied to determine if the value should be overwritten. Defaults to None.

    Returns:
        None: The function modifies `base_data` in place.
    """
    for key, value in additional_data.items():
        if isinstance(value, dict):
            if key not in base_data:
                base_data[key] = value
            else:
                deep_merge(base_data[key], value, rules)
        elif isinstance(value, list):
            if key not in base_data:
                base_data[key] = value
            else:
                base_data[key] += value
                base_data[key] = list(set(base_data[key]))
        else:
            if rules and key in rules:
                if rules[key](base_data[key], value):
                    base_data[key] = value
            else:
                base_data[key] = value


def use_default_when_none(value: T, default: T) -> T:
    """
    Returns the value if it is not None, otherwise returns the default value.

    Args:
        value (T): The value to check.
        default (T): The default value to return if `value` is None.

    Returns:
        T: The original value or the default value.
    """
    return value if value is not None else default
