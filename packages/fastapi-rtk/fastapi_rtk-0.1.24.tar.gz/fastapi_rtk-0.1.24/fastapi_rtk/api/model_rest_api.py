import asyncio
import csv
import enum
import re
import types
import typing
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Tuple, Type

import pydantic
from fastapi import Body, Depends, HTTPException, Response, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, create_model
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import Session, scoped_session

from ..async_column_handler import AsyncColumnHandler
from ..const import EXCLUDE_ROUTES, PERMISSION_PREFIX, logger
from ..db import QueryManager, get_session
from ..decorators import expose, permission_name, priority
from ..dependencies import current_permissions, get_query_manager, has_access_dependency
from ..filters import BaseFilter
from ..globals import g
from ..models import Model
from ..schemas import (
    BaseResponseMany,
    BaseResponseSingle,
    ColumnEnumInfo,
    ColumnInfo,
    ColumnRelationInfo,
    GeneralResponse,
    InfoResponse,
    QueryBody,
    QuerySchema,
    RelInfo,
)
from ..setting import Setting
from ..types import ExportMode
from ..utils import (
    CSVJSONConverter,
    Line,
    SelfDepends,
    SelfType,
    deep_merge,
    merge_schema,
    safe_call,
    smart_run,
    use_default_when_none,
)
from .base_api import BaseApi
from .interface import (
    PARAM_BODY_QUERY_SESSION,
    PARAM_ID_QUERY_SESSION,
    PARAM_ID_QUERY_SESSION_ITEM,
    PARAM_IDS_Q_QUERY_SESSION_ITEMS,
    SQLAInterface,
)

__all__ = ["ModelRestApi"]


class ModelRestApi(BaseApi):
    """
    Base Class for FastAPI APIs that use a SQLAlchemy model.

    Usage:
    ```python
    from fastapi_rtk.api import ModelRestApi
    from fastapi_rtk.filters import FilterEqual
    from app.models import User
    from app.schemas import UserSchema

    class UserApi(ModelRestApi):
        datamodel = SQLAInterface(User)
        search_columns = ["username"]
        search_exclude_columns = ["password"]
        search_query_rel_fields = {
            "user": [
                ["username", FilterEqual, "admin"],
            ],
        }
        filter_options = {
            "odd_numbers": [1, 3, 5, 7, 9],
        }
    """

    """
    -------------
     GENERAL
    -------------
    """

    datamodel: SQLAInterface
    """
    The SQLAlchemy interface object.

    Usage:
    ```python
    datamodel = SQLAInterface(User)
    ```
    """

    max_page_size: int | None = None
    """
    The maximum page size for the related fields in add_columns, edit_columns, and search_columns properties.
    """

    exclude_routes: List[EXCLUDE_ROUTES] = None
    """
    The list of routes to exclude. available routes: `info`, `download`, `upload`, `bulk`, `get_list`, `get`, `post`, `put`, `delete`.
    """

    base_order: Tuple[str, Literal["asc", "desc"]] | None = None
    """
    The default order for the list endpoint. Set this to set the default order for the list endpoint.

    Example:
    ```python
    base_order = ("name", "asc")
    ```
    """

    base_filters: List[Tuple[str, Type[BaseFilter], Any]] | None = None
    """
    The default filters for the list endpoint. Set this to set the default filters for the list endpoint. Defaults to None.

    Example:
    ```python
    base_filters = [
        ["status", FilterEqual, "active"],
    ]
    ```
    """

    show_base_filters: List[Tuple[str, Type[BaseFilter], Any]] | None = None
    """
    The default filters for the show endpoint. Set this to set the default filters for the show endpoint. Defaults to None.

    Example:
    ```python
    show_base_filters = [
        ["status", FilterEqual, "active"],
    ]
    ```
    """

    download_base_filters: List[Tuple[str, Type[BaseFilter], Any]] | None = None
    """
    The default filters for the download endpoint. Set this to set the default filters for the download endpoint. Defaults to None.

    Example:
    ```python
    download_base_filters = [
        ["status", FilterEqual, "active"],
    ]
    ```
    """

    description_columns: Dict[str, str] = None
    """
    The description for each column in the add columns, edit columns, and search columns properties.

    Example:
    ```python
    description_columns = {
        "name": "Name of the item",
        "description": "Description of the item",
    }
    ```
    """
    order_rel_fields: Dict[str, Tuple[str, Literal["asc", "desc"]]] = None
    """
    Order the related fields in the add columns, edit columns, and search columns properties.

    Example:
    ```python
    order_rel_fields = {
        "user": ("username", "asc"),
    }
    ```
    """
    filter_options: Dict[str, Any] = None
    """
    Additional filter options from the user for the info endpoint.

    Example:
    ```python
    filter_options = {
        "odd_numbers": [1, 3, 5, 7, 9],
    }
    ```
    """
    query_schema: Type[QuerySchema] = None
    """
    The query schema for the list endpoint.
    
    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    download_body_schema: Type[QueryBody] = None
    """
    The body schema for the download endpoint.
    
    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """

    """
    -------------
     INFO
    -------------
    """

    info_return_schema: Type[InfoResponse] = None
    """
    The response schema for the info endpoint. 

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """

    """
    -------------
     SEARCH
    -------------
    """

    search_columns: List[str] = None
    """
    The list of columns that are allowed to be filtered in the list endpoint. If not provided, all columns will be allowed.
    """
    search_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the search columns.
    """
    search_filters: Dict[str, List[Type[BaseFilter]]] = None
    """
    Add additional filters to the search columns.

    Example:
    ```python
    search_filters = {
        "name": [FilterNameStartsWithA],
    }
    ```
    """
    search_exclude_filters: Dict[str, List[Type[BaseFilter] | str]] = None
    """
    Exclude filters from the search columns.

    Can be a list of filter classes or a list of strings with the filter names.

    Example:
    ```python
    search_exclude_filters = {
        "name": ['eq', 'in', FilterNotEqual, FilterStartsWith],
    }
    ```
    """
    search_query_rel_fields: Dict[str, List[Tuple[str, Type[BaseFilter], Any]]] = None
    """
    The query fields for the related fields in the filters.

    Example:
    ```python
    search_query_rel_fields = {
        "user": [
            ["username", FilterEqual, "admin"],
        ],
    }
    ```
    """

    """
    -------------
     LIST
    -------------
    """

    list_title: str = None
    """
    The title for the list endpoint. If not provided, Defaults to "List {ModelName}".
    """
    list_columns: List[str] = None
    """
    The list of columns to display in the list endpoint. If not provided, all columns will be displayed.
    """
    list_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the list endpoint.
    """
    extra_list_fetch_columns: List[str] = None
    """
    The list of columns to be fetch from the database alongside the `list_columns`. Useful if you don't want some columns to be shown but still want to fetch them.
    """
    list_select_columns: List[str] = None
    """
    The list of columns to be selected from the database and as a result of the list endpoint. If not provided, `list_columns` + `extra_list_fetch_columns` will be used.

    Useful if you need to modify which columns to be returned while keeping everything else the same.
    """
    list_obj_schema: Type[BaseModel] = None
    """
    The schema for the object in the list endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    list_return_schema: Type[BaseResponseMany] = None
    """
    The response schema for the list endpoint.
    
    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    label_columns: Dict[str, str] = None
    """
    The label for each column in the list columns and show columns properties.

    Example:
    ```python
    label_columns = {
        "name": "Name",
        "description": "Description",
    }
    ```
    """
    order_columns: List[str] = None
    """
    The list of columns that can be ordered in the list endpoint. If not provided, all columns will be allowed.
    """

    """
    -------------
     SHOW
    -------------
    """

    show_title: str = None
    """
    The title for the show endpoint. If not provided, Defaults to "Show {ModelName}".
    """
    show_columns: List[str] = None
    """
    The list of columns to display in the show endpoint and for the result of the add and edit endpoint. If not provided, all columns will be displayed.
    """
    show_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the show endpoint.
    """
    extra_show_fetch_columns: List[str] = None
    """
    The list of columns to be fetch from the database alongside the `show_columns`. Useful if you don't want some columns to be shown but still want to fetch them.
    """
    show_select_columns: List[str] = None
    """
    The list of columns to be selected from the database and as a result of the show endpoint. If not provided, `show_columns` + `extra_show_fetch_columns` will be used.

    Useful if you need to modify which columns to be returned while keeping everything else the same.
    """
    show_obj_schema: Type[BaseModel] = None
    """
    The schema for the object in the show endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    show_return_schema: Type[BaseResponseSingle] = None
    """
    The response schema for the show endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """

    """
    -------------
     ADD
    -------------
    """

    add_title: str = None
    """
    The title for the add endpoint. If not provided, Defaults to "Add {ModelName}".
    """
    add_columns: List[str] = None
    """
    The list of columns to display in the add endpoint. If not provided, all columns will be displayed.
    """
    add_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the add endpoint.
    """
    add_jsonforms_schema: Dict[str, Any] | None = None
    """
    The `JSONForms` schema for the add endpoint. If not provided, Defaults to the schema generated from the `add_columns` property.
    """
    add_jsonforms_uischema: Dict[str, Any] | None = None
    """
    The `JSONForms` uischema for the add endpoint. If not provided, it will let `JSONForms` generate the uischema.
    """
    add_schema: Type[BaseModel] = None
    """
    The schema for the add endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    add_schema_extra_fields: (
        dict[str, type | tuple[type, pydantic.fields.FieldInfo]] | None
    ) = None
    """
    Extra fields to add to the add schema. Useful when you want to add extra fields in the body of the add endpoint for your custom logic.

    Example:
    ```python
    add_schema_extra_fields = {
        "extra_field": str,
        "extra_field_with_field_info": (str, Field(default="default_value")),
    }
    ```
    """
    add_obj_schema: Type[BaseModel] = None
    """
    The schema for the object in the add endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    add_return_schema: Type[BaseResponseSingle] = None
    """
    The response schema for the add endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    add_query_rel_fields: Dict[str, List[Tuple[str, Type[BaseFilter], Any]]] = None
    """
    The query fields for the related fields in the add_columns property.

    Example:
    ```python
    add_query_rel_fields = {
        "user": [
            ["username", FilterEqual, "admin"],
        ],
    }
    ```
    """

    """
    -------------
     EDIT
    -------------
    """

    edit_title: str = None
    """
    The title for the edit endpoint. If not provided, Defaults to "Edit {ModelName}".
    """
    edit_columns: List[str] = None
    """
    The list of columns to display in the edit endpoint. If not provided, all columns will be displayed.
    """
    edit_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the edit endpoint.
    """
    edit_jsonforms_schema: Dict[str, Any] | None = None
    """
    The `JSONForms` schema for the edit endpoint. If not provided, Defaults to the schema generated from the `edit_columns` property.
    """
    edit_jsonforms_uischema: Dict[str, Any] | None = None
    """
    The `JSONForms` uischema for the edit endpoint. If not provided, it will let `JSONForms` generate the uischema.
    """
    edit_schema: Type[BaseModel] = None
    """
    The schema for the edit endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    edit_schema_extra_fields: (
        dict[str, type | tuple[type, pydantic.fields.FieldInfo]] | None
    ) = None
    """
    Extra fields to add to the edit schema. Useful when you want to add extra fields in the body of the edit endpoint for your custom logic.

    Example:
    ```python
    edit_schema_extra_fields = {
        "extra_field": str,
        "extra_field_with_field_info": (str, Field(default="default_value")),
    }
    ```
    """
    edit_obj_schema: Type[BaseModel] = None
    """
    The schema for the object in the edit endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    edit_return_schema: Type[BaseResponseSingle] = None
    """
    The response schema for the edit endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    edit_query_rel_fields: Dict[str, List[Tuple[str, Type[BaseFilter], Any]]] = None
    """
    The query fields for the related fields in the edit_columns property.

    Example:
    ```python
    edit_query_rel_fields = {
        "user": [
            ["username", FilterEqual, "admin"],
        ],
    }
    ```
    """

    """
    -------------
     PRIVATE
    -------------
    """

    _default_info_schema: bool = False
    """
    A flag to indicate if the default info schema is used.

    DO NOT MODIFY.
    """

    def __init__(self):
        if not self.datamodel:
            raise Exception(f"Missing datamodel in {self.__class__.__name__} API.")
        self.resource_name = self.resource_name or self.datamodel.obj.__name__.lower()
        self.max_page_size = self.max_page_size or Setting.API_MAX_PAGE_SIZE
        self._init_titles()
        self._init_properties()
        self.post_properties()
        self._init_schema()
        self.post_schema()
        self._init_routes()
        super().__init__()

    def post_properties(self):
        """
        Post properties to be called after the init_properties method.
        """
        pass

    def post_schema(self):
        """
        Post schema to be called after the init_schema method.
        """
        pass

    """
    -----------------------------------------
         INIT FUNCTIONS
    -----------------------------------------
    """

    def _init_titles(self) -> None:
        """
        Init Titles if not defined
        """
        class_name = self.datamodel.obj.__name__
        if not self.list_title:
            self.list_title = "List " + self._prettify_name(class_name)
        if not self.add_title:
            self.add_title = "Add " + self._prettify_name(class_name)
        if not self.edit_title:
            self.edit_title = "Edit " + self._prettify_name(class_name)
        if not self.show_title:
            self.show_title = "Show " + self._prettify_name(class_name)
        self.title = self.list_title

    def _init_properties(self) -> None:
        """
        Init properties if not defined
        """
        list_cols = self.datamodel.get_user_column_list()
        property_cols = self.datamodel.get_property_column_list()

        self.search_filters = self.search_filters or {}
        for key, value in self.search_filters.items():
            datamodel, _ = self._get_datamodel_and_column(key)
            self.datamodel.filters[key].extend([v(datamodel) for v in value])
        self.search_exclude_filters = self.search_exclude_filters or {}
        for key, value in self.search_exclude_filters.items():
            value = [v.arg_name if isinstance(v, BaseFilter) else v for v in value]
            self.datamodel.exclude_filters[key].extend(value)
            self.datamodel.filters[key] = [
                x for x in self.datamodel.filters[key] if x.arg_name not in value
            ]

        self.exclude_routes = self.exclude_routes or []
        self.exclude_routes = [x.lower() for x in self.exclude_routes]
        self.description_columns = self.description_columns or {}
        self.filter_options = self.filter_options or {}

        self.list_exclude_columns = self.list_exclude_columns or []
        self.show_exclude_columns = self.show_exclude_columns or []
        self.add_exclude_columns = self.add_exclude_columns or []
        self.edit_exclude_columns = self.edit_exclude_columns or []
        self.search_exclude_columns = self.search_exclude_columns or []
        self.label_columns = self.label_columns or {}

        self.extra_list_fetch_columns = self.extra_list_fetch_columns or []
        self.extra_show_fetch_columns = self.extra_show_fetch_columns or []

        self.list_columns = use_default_when_none(
            self.list_columns,
            [
                x
                for x in list_cols + property_cols
                if x not in self.list_exclude_columns
            ],
        )
        self.show_columns = use_default_when_none(
            self.show_columns,
            [
                x
                for x in list_cols + property_cols
                if x not in self.show_exclude_columns
            ],
        )
        self.add_columns = use_default_when_none(
            self.add_columns,
            [x for x in list_cols if x not in self.add_exclude_columns],
        )
        self.edit_columns = use_default_when_none(
            self.edit_columns,
            [x for x in list_cols if x not in self.edit_exclude_columns],
        )
        self.search_columns = use_default_when_none(
            self.search_columns,
            [
                x
                for x in self.list_columns
                if x not in self.search_exclude_columns
                and x.count(".") < 2  #! Currently only supports 1 level of relation
            ],
        )

        self.list_select_columns = use_default_when_none(
            self.list_select_columns,
            self.list_columns + self.extra_list_fetch_columns,
        )
        self.show_select_columns = use_default_when_none(
            self.show_select_columns,
            self.show_columns + self.extra_show_fetch_columns,
        )

        # Check for 2nd level relations in search columns
        not_supported_search_columns = [
            x for x in self.search_columns if x.count(".") > 1
        ]
        if not_supported_search_columns:
            raise Exception(
                f"Search columns with 2nd level relations are not supported: {not_supported_search_columns}"
            )

        self.order_columns = use_default_when_none(
            self.order_columns,
            self.datamodel.get_order_column_list(list_columns=self.list_columns),
        )

        self._gen_labels_columns(self.list_columns)
        self._gen_labels_columns(self.show_columns)
        self._gen_labels_columns(self.search_columns)

        self.order_rel_fields = self.order_rel_fields or dict()
        self.add_query_rel_fields = self.add_query_rel_fields or dict()
        self.edit_query_rel_fields = self.edit_query_rel_fields or dict()
        self.search_query_rel_fields = self.search_query_rel_fields or dict()

        # Instantiate all the filters
        filter_keys = ["base_filters", "show_base_filters", "download_base_filters"]
        for key in filter_keys:
            filters = getattr(self, key)
            if not filters:
                continue
            setattr(
                self,
                key,
                self._init_filter(self.datamodel, filters),
            )

        field_keys = [
            "add_query_rel_fields",
            "edit_query_rel_fields",
            "search_query_rel_fields",
        ]
        for key in field_keys:
            filter_dict = getattr(self, key)
            for field, filters in filter_dict.items():
                filter_dict[field] = self._init_filter(
                    self.datamodel.get_related_interface(field), filters
                )

    def _init_schema(self) -> None:
        """
        Initializes the schema for the API.

        This method creates schema models for info, list, get, add, and edit endpoints based on the datamodel's table columns.

        Returns:
            None
        """
        if not self.info_return_schema:
            self.info_return_schema = merge_schema(
                InfoResponse,
                {
                    "add_title": (str, Field(default=self.add_title)),
                    "edit_title": (str, Field(default=self.edit_title)),
                    "filter_options": (dict, Field(default={})),
                },
                name=f"{self.__class__.__name__}-InfoResponse",
            )
            self._default_info_schema = True

        order_column_enum = Enum(
            f"{self.__class__.__name__}-OrderColumnEnum",
            {col: col for col in self.order_columns},
            type=str,
        )

        self.query_schema = self.query_schema or merge_schema(
            QuerySchema,
            {
                "order_column": (order_column_enum | None, Field(default=None)),
            },
            True,
            f"{self.__class__.__name__}-QuerySchema",
        )

        self.download_body_schema = self.download_body_schema or merge_schema(
            QueryBody,
            {
                "order_column": (order_column_enum | None, Field(default=None)),
            },
            True,
            f"{self.__class__.__name__}-DownloadBodySchema",
        )

        self.list_obj_schema = self.list_obj_schema or self.datamodel.generate_schema(
            self.list_select_columns,
            False,
            False,
            name=f"{self.__class__.__name__}-ListObjSchema",
        )
        self.show_obj_schema = self.show_obj_schema or self.datamodel.generate_schema(
            self.show_select_columns,
            False,
            False,
            name=f"{self.__class__.__name__}-ShowObjSchema",
        )
        self.add_obj_schema = self.add_obj_schema or self.datamodel.generate_schema(
            self.add_columns,
            False,
            False,
            name=f"{self.__class__.__name__}-AddObjSchema",
            hide_sensitive_columns=False,
        )
        self.edit_obj_schema = self.edit_obj_schema or self.datamodel.generate_schema(
            self.edit_columns,
            False,
            False,
            optional=True,
            name=f"{self.__class__.__name__}-EditObjSchema",
            hide_sensitive_columns=False,
        )

        self.list_return_schema = self.list_return_schema or merge_schema(
            BaseResponseMany,
            {
                **vars(self),
                "result": (List[self.list_obj_schema], ...),
            },
            True,
            f"{self.__class__.__name__}-ListResponse",
        )
        self.show_return_schema = self.show_return_schema or merge_schema(
            BaseResponseSingle,
            {
                **vars(self),
                "result": (self.show_obj_schema, ...),
            },
            True,
            f"{self.__class__.__name__}-ShowResponse",
        )
        self.add_return_schema = self.add_return_schema or merge_schema(
            self.show_return_schema,
            {},
            name=f"{self.__class__.__name__}-AddResponse",
        )
        self.edit_return_schema = self.edit_return_schema or merge_schema(
            self.show_return_schema,
            {},
            name=f"{self.__class__.__name__}-EditResponse",
        )

        merged_schema = self.add_obj_schema
        if self.add_schema_extra_fields:
            extra_fields = self._handle_schema_extra_fields(
                self.add_schema_extra_fields
            )
            merged_schema = merge_schema(
                merged_schema,
                extra_fields,
                name=f"{self.__class__.__name__}-AddObjSchema-Merged",
            )
        self.add_schema = self.add_schema or self._create_request_schema(
            merged_schema, name=f"{self.__class__.__name__}-AddSchema"
        )

        merged_schema = self.edit_obj_schema
        if self.edit_schema_extra_fields:
            extra_fields = self._handle_schema_extra_fields(
                self.edit_schema_extra_fields
            )
            merged_schema = merge_schema(
                merged_schema,
                extra_fields,
                name=f"{self.__class__.__name__}-EditObjSchema-Merged",
            )
        self.edit_schema = self.edit_schema or self._create_request_schema(
            merged_schema,
            optional=True,
            name=f"{self.__class__.__name__}-EditSchema",
        )

    def _init_routes(self):
        """
        Init routes for the API.
        """
        routes = [
            "info",
            "download",
            "upload",
            "bulk",
            "get_list",
            "get",
            "post",
            "put",
            "delete",
        ]
        routes = [x for x in routes if x not in self.exclude_routes]
        for route in routes:
            getattr(self, route)()

    """
    -------------
     DEPENDENCIES
    -------------
    """

    def get_query_manager(self, select_property=""):
        """
        Returns the query manager dependency.

        Returns:
            Callable[..., QueryManager]: The query manager dependency.
        """
        if select_property:
            #! DEPRECATED
            logger.warning(
                "get_query_manager with `select_property` is deprecated and will be removed in the future."
            )
        return get_query_manager(self.datamodel)

    def get_current_permissions(self):
        """
        Returns the current permissions dependency.

        Returns:
            Callable[..., Coroutine[Any, Any, Any | list]]: The current permissions that the user has for the API dependency.
        """
        return current_permissions(self)

    def get_api_session(self):
        """
        Returns the database dependency.

        Returns:
            Callable[..., AsyncSession | Session]: The database dependency.
        """
        # TODO: Still using normal get session, scoped session still broken
        return get_session(getattr(self.datamodel.obj, "__bind_key__", None))

    def info(self):
        """
        Info endpoint for the API.
        """
        priority(9)(self.info_headless)
        permission_name("info")(self.info_headless)
        expose(
            "/_info",
            methods=["GET"],
            name="Get Info",
            description="Get the info for this API's Model.",
            response_model=self.info_return_schema,
            dependencies=[Depends(has_access_dependency(self, "info"))],
        )(self.info_headless)

    async def info_headless(
        self,
        permissions: List[str] = SelfDepends().get_current_permissions,
        session: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Retrieves information in a headless mode.

        Args:
            permissions (List[str]): A list of permissions.
            session (async_scoped_session AsyncSession
        | Session): A database scoped session.

        Returns:
            info_return_schema: The information return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        info = (
            (await smart_run(self._generate_info_schema, permissions, session))
            if self._default_info_schema
            else self.info_return_schema()
        )
        await smart_run(self.pre_info, info, permissions, session)
        return info

    async def pre_info(
        self,
        info: InfoResponse,
        permissions: List[str],
        session: async_scoped_session[AsyncSession] | scoped_session[Session],
    ):
        """
        Pre-process the info response before returning it.
        The response still needs to adhere to the InfoResponse schema.

        Args:
            info (InfoResponse): The info response.
            permissions (List[str]): A list of permissions.
            session (async_scoped_session AsyncSession
        | Session): A database scoped session.
        """
        pass

    def download(self):
        """
        Download endpoint for the API.
        """
        priority(8)(self.download_headless)
        permission_name("download")(self.download_headless)
        expose(
            "/download",
            methods=["GET"],
            name="Download",
            description="Download list of items in CSV format.",
            dependencies=[Depends(has_access_dependency(self, "download"))],
        )(self.download_headless)

    async def download_headless(
        self,
        q: QuerySchema = SelfType.with_depends().query_schema,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
        export_mode: ExportMode = "simplified",
        delimiter: str = ",",
        quotechar: str | None = None,
        label: str = "",
        check_validity: bool = False,
    ):
        """
        Downloads a file in a headless mode.

        Args:
            body (QueryBody): The query body.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.
            export_mode (str): The export mode. Can be "simplified" or "detailed". Defaults to "simplified".
            delimiter (str): The delimiter for the CSV file. Defaults to ",".
            quotechar (str | None): Quote character for the CSV file. If not given, it will not be used. Defaults to None.
            label (str): The label for the CSV file. Defaults to the resource name.
            check_validity (bool): If True, only checks the validity of the request and returns a 200 OK response.

        Returns:
            StreamingResponse: The streaming response.
        """
        for filter in q.filters:
            if filter.col not in self.search_columns:
                raise HTTPException(
                    status_code=400, detail=f"Invalid filter: {filter.col}"
                )

        list_columns: list[str] = self.list_columns.copy()
        label_columns = self.label_columns.copy()

        if export_mode == "detailed":
            list_columns = []
            for column in self.list_columns:
                if self.datamodel.is_relation_one_to_one(
                    column
                ) or self.datamodel.is_relation_many_to_one(column):
                    rel_interface = self.datamodel.get_related_interface(column)
                    cols = [
                        x
                        for x in self.datamodel.get_columns_from_related_col(column)
                        if not rel_interface.is_relation(x.split(".")[-1])
                    ]
                    for col in cols:
                        list_columns.append(col)
                        label_columns[col] = label_columns.get(col, col)
                    continue

                if column not in list_columns:
                    list_columns.append(column)

        if check_validity:
            return GeneralResponse(detail="OK")

        try:
            return StreamingResponse(
                self._export_data(
                    query.yield_per(
                        session,
                        100,
                        {
                            "list_columns": self.list_select_columns,
                            "order_column": q.order_column,
                            "order_direction": q.order_direction,
                            "filters": q.filters,
                            "filter_classes": self.download_base_filters,
                        },
                    ),
                    list_columns,
                    label_columns,
                    self.list_obj_schema,
                    export_mode=export_mode,
                    delimiter=delimiter,
                    quotechar=quotechar,
                ),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={label or self.resource_name}.csv",
                },
            )
        finally:
            await safe_call(session.close())

    def upload(self):
        """
        Upload endpoint for the API.
        """
        priority(7)(self.upload_headless)
        permission_name("upload")(self.upload_headless)
        expose(
            "/upload",
            methods=["POST"],
            name="Upload",
            description="Upload a CSV file to be added to the database.",
            dependencies=[Depends(has_access_dependency(self, "upload"))],
        )(self.upload_headless)

    async def upload_headless(
        self,
        file: UploadFile,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
        delimiter: str = ",",
        quotechar: str | None = None,
    ):
        """
        Uploads a file in a headless mode.

        Args:
            file (UploadFile): The uploaded file.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.
            delimiter (str, optional): The delimiter for the CSV file. Defaults to ",".
            quotechar (str | None): Quote character for the CSV file. If not given, it will not be used. Defaults to None.

        Raises:
            HTTPException: If the file type is not CSV.

        Returns:
            list[dict[str, typing.Any]]: The list of items added to the database.
        """
        if not file.content_type.endswith("csv"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only CSV files are allowed.",
            )

        return await self._import_data(
            await file.read(), query, session, delimiter, quotechar=quotechar
        )

    def bulk(self):
        """
        Bulk endpoint for the API.
        """
        priority(6)(self.bulk_headless)
        permission_name("bulk")(self.bulk_headless)
        expose(
            "/bulk/{handler}",
            methods=["POST"],
            name="Bulk",
            description="Handle bulk operations.",
            dependencies=[Depends(has_access_dependency(self, "bulk"))],
        )(self.bulk_headless)

    async def bulk_headless(
        self,
        handler: str,
        body: dict | list = Body(...),
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Bulk handler in headless mode.

        Args:
            handler (str): The handler name.
            body (dict | list): The request body.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.

        Returns:
            Response: The response object.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        bulk_handler: Callable | None = getattr(self, f"bulk_{handler}", None)
        if not bulk_handler:
            raise HTTPException(status_code=404, detail="Handler not found")
        try:
            return await smart_run(bulk_handler, body, query, session)
        except NotImplementedError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def bulk_handler(
        self,
        body: dict | list,
        query: QueryManager,
        session: AsyncSession | Session,
    ) -> Response:
        """
        Bulk handler for the API.
        To be implemented by the subclass.

        Example:
        ```python
        async def bulk_read(self, body: dict | list, query: QueryManager, session: AsyncSession | Session) -> Response:
            items = await smart_run(query.get_many, session, params={"where_in": (self.datamodel.get_pk_attr(), [item["id"] for item in body])})
            pks, data = self.datamodel.convert_to_result(items)
            return data
        ```

        Args:
            body (dict | list): The request body.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.

        Returns:
            Response: The response object.

        Raises:
            NotImplementedError: If the method is not implemented. To be implemented by the subclass.
        """
        raise NotImplementedError("Bulk handler not implemented")

    def get_list(self):
        """
        List endpoint for the API.
        """
        priority(5)(self.get_list_headless)
        permission_name("get")(self.get_list_headless)
        expose(
            "/",
            methods=["GET"],
            name="Get items",
            description="Get a list of items.",
            response_model=self.list_return_schema,
            dependencies=[Depends(has_access_dependency(self, "get"))],
        )(self.get_list_headless)

    async def get_list_headless(
        self,
        q: QuerySchema = SelfType.with_depends().query_schema,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
        session_count: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Retrieves all items in a headless mode.

        Args:
            q (QuerySchema): The query schema.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.
            session_count (AsyncSession | Session): A database scoped session for counting.

        Returns:
            list_return_schema: The list return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        for filter in q.filters:
            if filter.col not in self.search_columns:
                raise HTTPException(
                    status_code=400, detail=f"Invalid filter: {filter.col}"
                )
        base_order = None
        base_order_direction = None
        if self.base_order:
            base_order, base_order_direction = self.base_order
        filter_classes = self.base_filters
        try:
            async with asyncio.TaskGroup() as tg:
                task_items = tg.create_task(
                    smart_run(
                        query.get_many,
                        session,
                        params={
                            "list_columns": self.list_select_columns,
                            "page": q.page,
                            "page_size": q.page_size,
                            "order_column": q.order_column or base_order,
                            "order_direction": q.order_direction
                            or base_order_direction,
                            "filters": q.filters,
                            "filter_classes": filter_classes,
                            "global_filter": q.global_filter,
                        },
                    )
                )
                task_count = tg.create_task(
                    smart_run(query.count, session_count, q.filters, filter_classes)
                )
        except* HTTPException as e:
            for ex in e.exceptions:
                raise ex

        items, count = await task_items, await task_count
        pks, data = self.datamodel.convert_to_result(items)
        async with AsyncColumnHandler.populate_async_columns():
            body = await smart_run(
                self.list_return_schema,
                result=data,
                count=count,
                ids=pks,
                description_columns=self.description_columns,
                label_columns=self.label_columns,
                list_columns=self.list_columns,
                list_title=self.list_title,
                order_columns=self.order_columns,
            )

        await smart_run(
            self.pre_get_list,
            body,
            PARAM_IDS_Q_QUERY_SESSION_ITEMS(
                ids=pks, q=q, query=query, session=session, items=items
            ),
        )
        return body

    async def pre_get_list(
        self, body: BaseResponseMany, params: PARAM_IDS_Q_QUERY_SESSION_ITEMS
    ):
        """
        Pre-process the list response before returning it.
        The response still needs to adhere to the BaseResponseMany schema.

        Args:
            body (BaseResponseMany): The response body.
            params (Params): Additional data passed to the handler.
        """
        pass

    def get(self):
        """
        Get endpoint for the API.
        """
        priority(4)(self.get_headless)
        permission_name("get")(self.get_headless)
        expose(
            "/{id}",
            methods=["GET"],
            name="Get item",
            description="Get a single item.",
            response_model=self.show_return_schema,
            dependencies=[Depends(has_access_dependency(self, "get"))],
        )(self.get_headless)

    async def get_headless(
        self,
        id=SelfType().datamodel.id_schema,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Retrieves a single item in a headless mode.

        Args:
            id (str): The id of the item.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.

        Returns:
            show_return_schema: The show return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        item = await smart_run(
            query.get_one,
            session,
            params={
                "list_columns": self.show_select_columns,
                "where_id": id,
                "filter_classes": self.show_base_filters,
            },
        )
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        pk, data = self.datamodel.convert_to_result(item)
        async with AsyncColumnHandler.populate_async_columns():
            body = await smart_run(
                self.show_return_schema,
                id=pk,
                result=data,
                description_columns=self.description_columns,
                label_columns=self.label_columns,
                show_columns=self.show_columns,
                show_title=self.show_title,
            )
        await smart_run(
            self.pre_get,
            body,
            PARAM_ID_QUERY_SESSION_ITEM(id=id, query=query, session=session, item=item),
        )
        return body

    async def pre_get(
        self, body: BaseResponseSingle, params: PARAM_ID_QUERY_SESSION_ITEM
    ):
        """
        Pre-process the get response before returning it.
        The response still needs to adhere to the BaseResponseSingle schema.

        Args:
            body (BaseResponseSingle): The response body.
            params (Params): Additional data passed to the handler.
        """
        pass

    def post(self):
        """
        Post endpoint for the API.
        """
        priority(3)(self.post_headless)
        permission_name("post")(self.post_headless)
        expose(
            "/",
            methods=["POST"],
            name="Add item",
            description="Add a new item.",
            response_model=self.add_return_schema,
            dependencies=[Depends(has_access_dependency(self, "post"))],
        )(self.post_headless)

    async def post_headless(
        self,
        body: BaseModel = SelfType().add_schema,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Creates a new item in a headless mode.

        Args:
            body (BaseModel): The request body.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.

        Returns:
            add_return_schema: The add return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        body_json = await smart_run(
            self._process_body,
            session,
            body,
            self.add_query_rel_fields,
            self.add_schema_extra_fields.keys()
            if self.add_schema_extra_fields
            else None,
        )
        item = self.datamodel.obj(**body_json)
        await smart_run(
            self.pre_add,
            item,
            PARAM_BODY_QUERY_SESSION(body=body, query=query, session=session),
        )
        query.add(session, item)
        await safe_call(query.commit(session))
        item = await smart_run(
            query.get_one,
            session,
            params={
                "list_columns": self.show_select_columns,
                "where_id": getattr(item, self.datamodel.get_pk_attr()),
            },
        )
        await smart_run(
            self.post_add,
            item,
            PARAM_BODY_QUERY_SESSION(body=body, query=query, session=session),
        )
        pk, data = self.datamodel.convert_to_result(item)
        async with AsyncColumnHandler.populate_async_columns():
            body = await smart_run(self.add_return_schema, id=pk, result=data)
        return body

    async def pre_add(self, item: Model, params: PARAM_BODY_QUERY_SESSION):
        """
        Pre-process the item before adding it to the database.

        Args:
            item (Model): The item to be added to the database.
            params (Params): Additional data passed to the handler.
        """
        pass

    async def post_add(self, item: Model, params: PARAM_BODY_QUERY_SESSION):
        """
        Post-process the item after adding it to the database.
        But before sending the response.

        Args:
            item (Model): The item to be added to the database.
            params (Params): Additional data passed to the handler.
        """
        pass

    def put(self):
        """
        Put endpoint for the API.
        """
        priority(2)(self.put_headless)
        permission_name("put")(self.put_headless)
        expose(
            "/{id}",
            methods=["PUT"],
            name="Update item",
            description="Update an item.",
            response_model=self.edit_return_schema,
            dependencies=[Depends(has_access_dependency(self, "put"))],
        )(self.put_headless)

    async def put_headless(
        self,
        id=SelfType().datamodel.id_schema,
        body: BaseModel = SelfType().edit_schema,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Updates an item in a headless mode.

        Args:
            id (str): The id of the item.
            body (BaseModel): The request body.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.

        Returns:
            add_return_schema: The add return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        item = await smart_run(
            query.get_one,
            session,
            params={
                "list_columns": self.show_select_columns,
                "where_id": id,
            },
        )
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        body_json = await smart_run(
            self._process_body,
            session,
            body,
            self.edit_query_rel_fields,
            self.edit_schema_extra_fields.keys()
            if self.edit_schema_extra_fields
            else None,
        )
        item.update(body_json)
        await smart_run(
            self.pre_update,
            item,
            PARAM_BODY_QUERY_SESSION(body=body, query=query, session=session),
        )
        query.add(session, item)
        await safe_call(query.commit(session))
        await safe_call(query.refresh(session, item))
        await smart_run(
            self.post_update,
            item,
            PARAM_BODY_QUERY_SESSION(body=body, query=query, session=session),
        )
        pk, data = self.datamodel.convert_to_result(item)
        async with AsyncColumnHandler.populate_async_columns():
            body = await smart_run(self.edit_return_schema, id=pk, result=data)
        return body

    async def pre_update(self, item: Model, params: PARAM_BODY_QUERY_SESSION):
        """
        Pre-process the item before updating it in the database.

        Args:
            item (Model): The item that will be updated in the database.
            params (Params): Additional data passed to the handler.
        """
        pass

    async def post_update(self, item: Model, params: PARAM_BODY_QUERY_SESSION):
        """
        Post-process the item after updating it in the database.
        But before sending the response.

        Args:
            item (Model): The item that was be updated in the database.
            params (Params): Additional data passed to the handler.
        """
        pass

    def delete(self):
        """
        Delete endpoint for the API.
        """
        priority(1)(self.delete_headless)
        permission_name("delete")(self.delete_headless)
        expose(
            "/{id}",
            methods=["DELETE"],
            response_model=GeneralResponse,
            name="Delete item",
            description="Delete an item.",
            dependencies=[Depends(has_access_dependency(self, "delete"))],
        )(self.delete_headless)

    async def delete_headless(
        self,
        id=SelfType().datamodel.id_schema,
        query: QueryManager = SelfDepends().get_query_manager,
        session: AsyncSession | Session = SelfDepends().get_api_session,
    ):
        """
        Deletes an item in a headless mode.

        Args:
            id (str): The id of the item.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): A database scoped session.

        Returns:
            GeneralResponse: The general response.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        item = await smart_run(
            query.get_one,
            session,
            params={
                "list_columns": self.show_select_columns,
                "where_id": id,
            },
        )
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        await smart_run(
            self.pre_delete,
            item,
            PARAM_ID_QUERY_SESSION(id=id, query=query, session=session),
        )
        await safe_call(query.delete(session, item))
        await safe_call(query.commit(session))
        await smart_run(
            self.post_delete,
            item,
            PARAM_ID_QUERY_SESSION(id=id, query=query, session=session),
        )
        body = GeneralResponse(detail="Item deleted")
        return body

    async def pre_delete(self, item: Model, params: PARAM_ID_QUERY_SESSION):
        """
        Pre-process the item before deleting it from the database.

        Args:
            item (Model): The item that will be deleted from the database.
            params (Params): Additional data passed to the handler.
        """
        pass

    async def post_delete(self, item: Model, params: PARAM_ID_QUERY_SESSION):
        """
        Post-process the item after deleting it from the database.
        But before sending the response.

        Args:
            item (Model): The item that was be deleted from the database.
            params (Params): Additional data passed to the handler.
        """
        pass

    def _create_request_schema(
        self, schema: Type[BaseModel], optional=False, name: str | None = None
    ):
        """
        Create a request schema based on the provided `schema` parameter. Useful for creating request schemas for add and edit endpoints, as it will transform the relation columns into the appropriate schema.

        Args:
            schema (Type[BaseModel]): The base schema to create the request schema from.
            optional (bool, optional): Flag indicating whether the request schema is optional. Defaults to False.
            name (str | None, optional): The name of the request schema. Defaults to None.

        Returns:
            pydantic.BaseModel: The created request schema.
        """
        columns = [
            x
            for x in schema.model_fields.keys()
            if not self.datamodel.is_pk(x) and self.datamodel.is_relation(x)
        ]
        rel_schema = dict()
        for col in columns:
            params = {}
            if optional:
                params["default"] = None
            elif self.datamodel.is_nullable(col):
                params["default"] = None
            # For relation, where the relation is one-to-one or many-to-one
            if self.datamodel.is_relation_one_to_one(
                col
            ) or self.datamodel.is_relation_many_to_one(col):
                related_interface = self.datamodel.get_related_interface(col)
                type = related_interface.id_schema | RelInfo
                if optional:
                    type = type | None
                if self.datamodel.is_nullable(col):
                    type = type | None
                rel_schema[col] = (
                    type,
                    Field(**params),
                )
            else:
                if not optional:
                    params["default"] = []
                type = (
                    List[self.datamodel.get_related_interface(col).id_schema]
                    | List[RelInfo]
                )
                if optional:
                    type = type | None
                if self.datamodel.is_nullable(col):
                    type = type | None
                related_interface = self.datamodel.get_related_interface(col)
                rel_schema[col] = (
                    type,
                    Field(**params),
                )

        new_schema_name = f"{self.__class__.__name__}-{schema.__name__}"
        new_schema = create_model(
            name or new_schema_name,
            **rel_schema,
            __base__=schema,
        )
        new_schema.model_config["extra"] = "forbid"
        return new_schema

    async def _generate_info_schema(
        self, permissions: List[str], session: AsyncSession | Session
    ):
        """
        Generates the information schema for the API based on the given permissions and database session.

        Args:
            permissions (List[str]): The list of permissions for the API.
            session (AsyncSession | Session): The database session.

        Returns:
            InfoSchema: The calculated information schema for the API.
        """
        schema = self.info_return_schema()
        schema.permissions = permissions
        schema.add_columns = []
        schema.edit_columns = []
        schema.filters = {}

        for key, val in self.filter_options.items():
            val = await smart_run(val) if callable(val) else val
            schema.filter_options[key] = val

        rel_cache = {}

        if f"{PERMISSION_PREFIX}post" in permissions:
            for col in self.add_columns:
                filters = self.add_query_rel_fields.get(col)
                order_column, order_direction = self.order_rel_fields.get(
                    col, (None, None)
                )
                cache_key = f"{col}_{filters}_{order_column}_{order_direction}"
                col_info = rel_cache.get(cache_key)
                if not col_info:
                    col_info = await smart_run(
                        self.datamodel.get_column_info,
                        col,
                        session,
                        params={
                            "page": 0,
                            "page_size": self.max_page_size,
                            "order_column": order_column,
                            "order_direction": order_direction,
                            "filter_classes": filters,
                        },
                        description_columns=self.description_columns,
                        label_columns=self.label_columns,
                        dictionary_cache=self.cache,
                        cache_key=f"column_info_{col}",
                    )
                    rel_cache[cache_key] = col_info
                schema.add_columns.append(col_info)

            schema.add_schema = (
                self.add_jsonforms_schema
                or self._generate_jsonforms_schema(
                    self.add_obj_schema, schema.add_columns
                )
            )
            schema.add_uischema = self.add_jsonforms_uischema

        if f"{PERMISSION_PREFIX}put" in permissions:
            for col in self.edit_columns:
                filters = self.edit_query_rel_fields.get(col)
                order_column, order_direction = self.order_rel_fields.get(
                    col, (None, None)
                )
                cache_key = f"{col}_{filters}_{order_column}_{order_direction}"
                col_info = rel_cache.get(cache_key)
                if not col_info:
                    col_info = await smart_run(
                        self.datamodel.get_column_info,
                        col,
                        session,
                        params={
                            "page": 0,
                            "page_size": self.max_page_size,
                            "order_column": order_column,
                            "order_direction": order_direction,
                            "filter_classes": filters,
                        },
                        description_columns=self.description_columns,
                        label_columns=self.label_columns,
                        dictionary_cache=self.cache,
                        cache_key=f"column_info_{col}",
                    )
                    rel_cache[cache_key] = col_info
                schema.edit_columns.append(col_info)

            schema.edit_schema = (
                self.edit_jsonforms_schema
                or self._generate_jsonforms_schema(
                    self.edit_obj_schema, schema.edit_columns
                )
            )
            schema.edit_uischema = self.edit_jsonforms_uischema

        for col in self.search_columns:
            info = dict()
            datamodel, col_to_get = self._get_datamodel_and_column(col)

            filters = self.cache.get(f"info_filters_{col}", None)
            if not filters:
                filters = datamodel.filters[col_to_get]
                # Add search filters and search exclude filters to the filters
                if "." in col:
                    filters.extend(self.datamodel.filters[col])
                    filters = [
                        f
                        for f in filters
                        if f.arg_name not in self.datamodel.exclude_filters[col]
                    ]

                filters = [{"name": f.name, "operator": f.arg_name} for f in filters]
                self.cache[f"info_filters_{col}"] = filters
            info["filters"] = filters
            info["label"] = self.label_columns.get(col)
            query_filters = self.search_query_rel_fields.get(col)
            order_column, order_direction = self.order_rel_fields.get(col, (None, None))
            cache_key = f"{col}_{query_filters}_{order_column}_{order_direction}"
            info["schema"] = rel_cache.get(cache_key)
            if not info["schema"]:
                info["schema"] = await smart_run(
                    datamodel.get_column_info,
                    col_to_get,
                    session,
                    params={
                        "page": 0,
                        "page_size": self.max_page_size,
                        "order_column": order_column,
                        "order_direction": order_direction,
                        "filter_classes": query_filters,
                    },
                    description_columns=self.description_columns,
                    label_columns=self.label_columns,
                    dictionary_cache=self.cache,
                    cache_key=f"column_info_{col}",
                )
                info["schema"].name = col
            schema.filters[col] = info

        return schema

    def _get_datamodel_and_column(self, col: str):
        """
        Gets the corresponding datamodel and column name for a given column. Useful for handling relations.

        Args:
            col (str): The column name.

        Returns:
            Tuple[SQLAInterface, str]: The datamodel and the related column name.
        """
        datamodel = self.datamodel
        col_to_get = col
        while "." in col_to_get:
            rel_col, col_to_get = col_to_get.split(".", 1)
            datamodel = datamodel.get_related_interface(rel_col)
        return datamodel, col_to_get

    async def _process_body(
        self,
        session: AsyncSession | Session,
        body: BaseModel | Dict[str, Any],
        filter_dict: dict[str, list[tuple[str, BaseFilter, Any]]],
        exclude: list[str] | None = None,
    ) -> Dict[str, Any]:
        """
        Process the body of the request by handling relations and returning a new body dictionary.

        Args:
            session (AsyncSession | Session): The session object for the database connection.
            body (BaseModel | Dict[str, Any]): The request body.
            filter_dict (dict[str, list[tuple[str, BaseFilter, Any]]): The filter dictionary.
            exclude (list[str] | None, optional): The list of fields to exclude from the body. Defaults to None.

        Returns:
            Dict[str, Any]: The transformed body dictionary.

        Raises:
            HTTPException: If any related items are not found or if an item is not found for a one-to-one or many-to-one relation.
        """
        body_json = (
            body.model_dump(exclude_unset=True, exclude=exclude)
            if isinstance(body, BaseModel)
            else body
        )
        new_body = {}
        for key, value in body_json.items():
            # Return the value as is if it is not a relation
            if not self.datamodel.is_relation(key):
                new_body[key] = value
                continue

            if not value:
                if self.datamodel.is_relation_one_to_many(
                    key
                ) or self.datamodel.is_relation_many_to_many(key):
                    new_body[key] = []
                else:
                    new_body[key] = None
                continue

            related_interface = self.datamodel.get_related_interface(key)
            query = QueryManager(related_interface)
            related_items = None

            if isinstance(value, list):
                value = [
                    val.get("id") if isinstance(val, dict) else val for val in value
                ]
                related_items = await smart_run(
                    query.get_many,
                    session,
                    params={
                        "where_id_in": value,
                        "filter_classes": filter_dict.get(key),
                    },
                )
                # If the length is not equal, then some items were not found
                if len(related_items) != len(value):
                    raise HTTPException(
                        status_code=400, detail=f"Some items in {key} not found"
                    )

                new_body[key] = related_items
                continue

            value = value.get("id") if isinstance(value, dict) else value
            related_item = await smart_run(
                query.get_one,
                session,
                params={"where_id": value, "filter_classes": filter_dict.get(key)},
            )
            if not related_item:
                raise HTTPException(400, detail=f"{key} not found")
            new_body[key] = related_item

        return new_body

    """
    -----------------------------------------
         HELPER FUNCTIONS
    -----------------------------------------
    """

    def _gen_labels_columns(self, list_columns: List[str]) -> None:
        """
        Auto generates pretty label_columns from list of columns
        """
        for col in list_columns:
            if not self.label_columns.get(col):
                self.label_columns[col] = self._prettify_column(col)

    @staticmethod
    def _prettify_name(name: str) -> str:
        """
        Prettify pythonic variable name.

        For example, 'HelloWorld' will be converted to 'Hello World'

        :param name:
            Name to prettify.
        """
        return re.sub(r"(?<=.)([A-Z])", r" \1", name)

    @staticmethod
    def _prettify_column(name: str) -> str:
        """
        Prettify pythonic variable name.

        For example, 'hello_world' will be converted to 'Hello World'

        :param name:
            Name to prettify.
        """
        return re.sub("[._]", " ", name).title()

    def _init_filter(
        self, datamodel: SQLAInterface, filter: List[Tuple[str, Type[BaseFilter], Any]]
    ):
        """
        Initialize the filter for the API.

        Args:
            datamodel (SQLAInterface): The datamodel object.
            filter (List[Tuple[str, Type[BaseFilter], Any]]): The list of filters to initialize.

        Returns:
            List[Tuple[str, Type[BaseFilter], Any]]: The initialized filters.
        """
        return [
            (
                x[0],
                x[1](
                    datamodel
                    if "." not in x[0]
                    else datamodel.get_related_interface(x[0].split(".")[0])
                ),
                x[2],
            )
            for x in filter
        ]

    def _handle_schema_extra_fields(
        self,
        schema_extra_fields: dict[str, type | tuple[type, pydantic.fields.FieldInfo]],
    ):
        """
        Handle the schema extra fields for the API.
        This will transform the fields into a dictionary with the field name as the key and the field type as the value if the field is not a tuple.

        Args:
            schema_extra_fields (dict[str, type | tuple[type, pydantic.fields.FieldInfo]]): The schema extra fields to handle.

        Returns:
            dict[str, tuple[type, pydantic.fields.FieldInfo]]: The transformed schema extra fields.
        """
        result: dict[str, tuple[type, pydantic.fields.FieldInfo]] = dict()

        for key in schema_extra_fields:
            value = schema_extra_fields[key]
            if not isinstance(value, tuple):
                is_nullable = False
                try:
                    args = typing.get_args(value)
                    for arg in args:
                        if arg is types.NoneType:
                            is_nullable = True
                            break
                except Exception:
                    pass

                result[key] = (
                    value,
                    Field(**{"default": None} if is_nullable else {}),
                )
            else:
                result[key] = value

        return result

    def _generate_jsonforms_schema(
        self,
        schema: type[BaseModel],
        info_columns: list[ColumnInfo | ColumnEnumInfo | ColumnRelationInfo],
    ):
        """
        Generate the JSONForms schema for the API.

        Args:
            schema (type[BaseModel]): The schema to generate the JSONForms schema from.
            info_columns (list[ColumnInfo | ColumnEnumInfo | ColumnRelationInfo]): The list of columns to include in the JSONForms schema.

        Returns:
            dict: The generated JSONForms schema.
        """
        jsonforms_schema = schema.model_json_schema()

        # Remove unused vars
        jsonforms_schema.pop("$defs", None)

        for key, value in jsonforms_schema["properties"].items():
            description = self.description_columns.get(key)
            if description:
                value["description"] = description

            if self.datamodel.is_boolean(key):
                value["type"] = "boolean"
            elif self.datamodel.is_integer(key):
                value["type"] = "integer"
            elif self.datamodel.is_enum(key):
                value["type"] = "string"
                enum_val = self.datamodel.get_enum_value(key)
                if isinstance(enum_val, enum.EnumType):
                    enum_val = [str(item.value) for item in enum_val]
                value["enum"] = enum_val
            elif self.datamodel.is_json(key) or self.datamodel.is_jsonb(key):
                value["type"] = "object"
            elif self.datamodel.is_relation(key):
                info = [x for x in info_columns if x.name == key]
                if not info:
                    raise Exception(f"Could not find info for {key} in {info_columns}")
                info = info[0]

                value["type"] = "string"
                value["oneOf"] = [
                    {
                        "const": str(item.id),
                        "title": item.value,
                    }
                    for item in info.values
                ]
                if not value["oneOf"]:
                    value["oneOf"].append(
                        {
                            "const": "null",
                            "title": "null",
                        }
                    )
                    value["readOnly"] = True

                if self.datamodel.is_relation_one_to_many(
                    key
                ) or self.datamodel.is_relation_many_to_many(key):
                    value["type"] = "array"
                    value["uniqueItems"] = True
                    value["items"] = {"oneOf": value["oneOf"]}
                    del value["oneOf"]
            else:
                # Check for anyOf (multiple possible types) and convert it to only one type
                anyOf = value.get("anyOf")
                if anyOf:
                    anyOf = filter(lambda x: x.get("type") != "null", anyOf)
                    for item in anyOf:
                        deep_merge(value, item)

            # Check whether it is nullable
            if self.datamodel.is_nullable(key):
                value["type"] = [value["type"], "null"]

            # Remove unused vars
            value.pop("anyOf", None)
            value.pop("default", None)
            value.pop("$ref", None)

            # Check whether the value should be a `secret`
            if key in g.sensitive_data.get(self.datamodel.obj.__name__, []):
                value["format"] = "password"

        return jsonforms_schema

    async def _export_data(
        self,
        data: list[Model],
        list_columns: list[str],
        label_columns: dict[str, str],
        schema: type[BaseModel],
        *,
        export_mode: ExportMode = "simplified",
        delimiter: str = ",",
        quotechar: str | None = None,
    ):
        """
        Export data to CSV format.

        Args:
            data (list[Model]): List of data to export.
            list_columns (list[str]): List of columns to include in the export.
            label_columns (dict[str, str]): Mapping of column names to labels.
            schema (type[BaseModel]): Schema for the data.
            export_mode (ExportMode, optional): Export mode (simplified or detailed). Defaults to "simplified".
            delimiter (str, optional): Delimiter for the CSV file. Defaults to ",".
            quotechar (str | None, optional): Quote character for the CSV file. If not given, it will not be used. Defaults to None.

        Yields:
            str: CSV formatted data.
        """
        line = Line()
        writer = csv.writer(line, delimiter=delimiter, quotechar=quotechar)

        # header
        labels = []
        for key in list_columns:
            if export_mode == "detailed":
                labels.append(key)
            else:
                labels.append(label_columns[key])

        # rows
        writer.writerow(labels)
        yield line.read()

        async for chunk in data:
            for item in chunk:
                async with AsyncColumnHandler.populate_async_columns():
                    item_model = schema.model_validate(item, from_attributes=True)
                item_dict = item_model.model_dump()
                row = CSVJSONConverter._json_to_csv(
                    item_dict,
                    list_columns=list_columns,
                    delimiter=delimiter,
                    export_mode=export_mode,
                )
                writer.writerow(row)
                yield line.read()

    async def _import_data(
        self,
        data: str | bytes,
        query: QueryManager,
        session: AsyncSession | Session,
        *,
        delimiter: str = ",",
        quotechar: str | None = None,
    ):
        """
        Import data from CSV format. This will parse the CSV data and resolve any relationships.

        Args:
            data (str | bytes): The CSV data to import.
            query (QueryManager): The query manager object.
            session (AsyncSession | Session): The session object for the database connection.
            delimiter (str, optional): Delimiter for the CSV file. Defaults to ",".
            quotechar (str | None, optional): Quote character for the CSV file. If not given, it will not be used. Defaults to None.

        Raises:
            HTTPException: If the length of the items does not match the number of items found for one-to-many or many-to-many relationships.

        Returns:
            list[dict[str, typing.Any]]: List of dictionaries containing the imported data with relationships resolved.
        """
        list_data = await smart_run(
            CSVJSONConverter.csv_to_json,
            data,
            delimiter=delimiter,
            quotechar=quotechar,
        )

        # Parse relationships
        for dat in list_data:
            relation_data = {}

            for col in self.add_columns:
                if col not in dat:
                    continue

                if self.datamodel.is_relation(col):
                    rel_interface = self.datamodel.get_related_interface(col)
                    rel_query = QueryManager(rel_interface)

                    item = dat.get(col)
                    if isinstance(item, list):
                        items = await rel_query.get_many(
                            session,
                            params={
                                "where_id_in": item,
                            },
                        )
                        if len(items) != len(item):
                            raise HTTPException(
                                status_code=400,
                                detail=f"Length of {col} does not match the number of items found.",
                            )
                        item = items
                        continue
                    else:
                        item = await rel_query.get_one(
                            session,
                            params={
                                "where": [(k, v) for k, v in dat.get(col, {}).items()]
                            },
                        )
                        if not item:
                            item = rel_interface.obj(**dat.get(col, {}))
                            rel_query.add(session, item)
                            await safe_call(rel_query.flush(session))
                            await safe_call(rel_query.refresh(session, item))

                    relation_data[col] = item
                    dat[col] = item

            dat.update(
                **{
                    **self.add_obj_schema(**dat).model_dump(exclude_unset=True),
                    **relation_data,
                },
            )
            query.add(session, self.datamodel.obj(**dat))
        await safe_call(query.commit(session))

        return list_data
