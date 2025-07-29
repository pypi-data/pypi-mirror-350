from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException

from .api.base_api import BaseApi
from .const import PERMISSION_PREFIX, logger
from .db import QueryManager
from .globals import g
from .models import PermissionApi, User

if TYPE_CHECKING:
    from .api import SQLAInterface
    from .generic.api import GenericInterface

    interface_type = SQLAInterface | GenericInterface

__all__ = [
    "set_global_user",
    "permissions",
    "current_permissions",
    "has_access_dependency",
    "get_query_manager",
]


def set_global_user():
    """
    A dependency for FastAPI that will set the current user to the global variable `g.user`.

    Usage:
    ```python
    async def get_info(
            *,
            session: AsyncSession | Session = Depends(get_async_session),
            none: None = Depends(set_global_user()),
        ):
    ...more code
    """

    async def set_global_user_dependency(
        user: User | None = Depends(
            g.auth.fastapi_users.current_user(active=True, default_to_none=True)
        ),
    ):
        g.user = user

    return set_global_user_dependency


def check_g_user():
    """
    A dependency for FastAPI that will check if the current user is set to the global variable `g.user`.

    Usage:
    ```python
    async def get_info(
            *,
            session: AsyncSession | Session = Depends(get_async_session),
            none: None = Depends(check_g_user()),
        ):
    ...more code
    """

    async def check_g_user_dependency():
        if not g.user:
            raise HTTPException(status_code=403, detail="Forbidden")

    return check_g_user_dependency


def permissions(as_object=False):
    """
    A dependency for FastAPI that will return all permissions of the current user.

    This will implicitly call the `current_user` dependency from `fastapi_users`. Therefore, it can return `403 Forbidden` if the user is not authenticated.

    Args:
        as_object (bool): Whether to return the `PermissionApi` objects or return the api names (E.g "AuthApi" or "AuthApi|UserApi").

    Usage:
    ```python
    async def get_info(
            *,
            permissions: List[str] = Depends(permissions()),
            session: AsyncSession | Session = Depends(get_async_session),
        ):
    ...more code
    ```
    """

    async def permissions_depedency():
        if not g.user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not g.user.roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        permissions = []
        for role in g.user.roles:
            for permission_api in role.permissions:
                if as_object:
                    permissions.append(permission_api)
                else:
                    permissions.append(permission_api.api.name)
        permissions = list(set(permissions))

        return permissions

    return permissions_depedency


def current_permissions(api: BaseApi):
    """
    A dependency for FastAPI that will return all permissions of the current user for the specified API.

    Because it will implicitly call the `permissions` dependency, it can return `403 Forbidden` if the user is not authenticated.

    Args:
        api (BaseApi): The API to be checked.

    Usage:
    ```python
    async def get_info(
            *,
            permissions: List[str] = Depends(current_permissions(self)),
            session: AsyncSession | Session = Depends(get_async_session),
        ):
    ...more code
    ```
    """

    async def current_permissions_depedency(
        permissions_apis: list[PermissionApi] = Depends(permissions(as_object=True)),
    ):
        permissions = []
        for permission_api in permissions_apis:
            if api.__class__.__name__ in permission_api.api.name.split("|"):
                permissions = permissions + permission_api.permission.name.split("|")
        if api.base_permissions:
            permissions = [x for x in permissions if x in api.base_permissions]
        return list(set(permissions))

    return current_permissions_depedency


def has_access_dependency(
    api: BaseApi,
    permission: str,
):
    """
    A dependency for FastAPI to check whether current user has access to the specified API and permission.

    Because it will implicitly call the `current_permissions` dependency, it can return `403 Forbidden` if the user is not authenticated.

    Usage:
    ```python
    @self.router.get(
            "/_info",
            response_model=self.info_return_schema,
            dependencies=[Depends(has_access(self, "info"))],
        )
    ...more code
    ```

    Args:
        api (BaseApi): The API to be checked.
        permission (str): The permission to check.
    """

    async def check_permission(
        permissions: list[str] = Depends(current_permissions(api)),
    ):
        if f"{PERMISSION_PREFIX}{permission}" not in permissions:
            raise HTTPException(status_code=403, detail="Forbidden")
        return

    return check_permission


def get_query_manager(
    interface: "interface_type",
    generic: bool = False,
    select_cols: list[str] | None = None,
):
    """
    A Dependency for FastAPI to get a query manager based on the given interface.

    Args:
        interface (SQLAInterface | GenericInterface): The interface to be used for the query manager.
        generic (bool, optional): Specifies whether to use a generic query manager. Defaults to False.

    Returns:
        Callable: A dependency function that provides a query manager based on the given interface.

    Usage:
    ```python
    @self.router.get(
            "/_info",
            response_model=self.info_return_schema,
            dependencies=[
                Depends(get_query_manager(self.interface)),
            ],
        )
    ...more code
    ```
    """

    def get_query_manager_dependency():
        if generic:
            from .generic.db import GenericQueryManager

            return GenericQueryManager(interface)
        if select_cols:
            #! Deprecated
            logger.warning(
                "The `select_cols` argument is deprecated and will be removed in the future."
            )
        return QueryManager(interface)

    return get_query_manager_dependency
