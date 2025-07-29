from typing import TYPE_CHECKING, Any, Dict

from fastapi import APIRouter, Depends

from ..const import PERMISSION_PREFIX, logger
from ..utils import update_signature

if TYPE_CHECKING:
    from ..fastapi_react_toolkit import FastAPIReactToolkit

__all__ = ["BaseApi"]


class BaseApi:
    """
    Base Class for FastAPI APIs.
    """

    version = "v1"
    """
    Version for the API. Defaults to "v1".
    """
    resource_name: str = None
    """
    The name of the resource. If not given, will use the class name.
    """
    description = ""
    """
    Description for the API. Will be used for the API documentation via `fastapi-rtk export api-docs`.
    """
    base_permissions: list[str] | None = None
    """
    List of base permissions for the API. Defaults to None.

    Example:
        base_permissions = ["can_get", "can_post"]
    """
    permissions: list[str] = None
    """
    List of permissions for the API.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    messages: list[str] = None
    """
    List of messages to log when the API is added to the toolkit.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    toolkit: "FastAPIReactToolkit" = None
    """
    The FastAPIReactToolkit object. Automatically set when the API is added to the toolkit.
    """
    _cache: Dict[str, Any] = None
    """
    The cache for the API.
    
    DO NOT MODIFY.
    """
    _router: APIRouter | None = None
    """
    The FastAPI router object.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """

    def __init__(self):
        """
        If you override this method, make sure to call `super().__init__()` at the end.
        """
        self.resource_name = self.resource_name or self.__class__.__name__.lower()
        self.permissions = self.permissions or []
        self.messages = self.messages or []
        self._initialize_router()

    async def on_startup(self):
        """
        Method to run on startup.
        """
        pass

    async def on_shutdown(self):
        """
        Method to run on shutdown.
        """
        pass

    def integrate_router(self, app: APIRouter):
        """
        Integrates the router into the FastAPI app.

        Args:
            app (APIRouter): The FastAPI app.
        """
        for message in self.messages:
            logger.info(message)
        app.include_router(self.router)

    @property
    def router(self):
        """
        Returns the router object.

        Returns:
            APIRouter: The router object.
        """
        if not self._router:
            self._router = APIRouter(
                prefix=f"/api/{self.version}/{self.resource_name}",
                tags=[self.__class__.__name__],
            )
        return self._router

    @property
    def cache(self):
        """
        Returns the cache dictionary.

        If the cache dictionary is not initialized, it initializes it as an empty dictionary.

        Returns:
            dict: The cache dictionary.
        """
        if not self._cache:
            self._cache = {}
        return self._cache

    def _initialize_router(self):
        """
        Initializes the router for the API. This method is called automatically when the API is initialized.
        """
        priority_routes = []
        exclude_routes = [f"{x}_headless" for x in getattr(self, "exclude_routes", [])]
        for attr_name in dir(self):
            if attr_name in exclude_routes:
                continue

            attr = getattr(self, attr_name)
            if hasattr(attr, "_permission_name"):
                permission_name = getattr(attr, "_permission_name")
                permission_name_with_prefix = f"{PERMISSION_PREFIX}{permission_name}"

                if not self._is_in_base_permissions(permission_name):
                    continue

                self.permissions.append(permission_name_with_prefix)

            if hasattr(attr, "_url"):
                data = attr._url
                if hasattr(attr, "_response_model_str"):
                    data["response_model"] = getattr(self, attr._response_model_str)

                extra_dependencies = []
                if hasattr(attr, "_dependencies"):
                    extra_dependencies = attr._dependencies
                if extra_dependencies and not data.get("dependencies"):
                    data["dependencies"] = []
                for dep in extra_dependencies:
                    func, kwargs = dep
                    if kwargs:
                        for key, val in kwargs.items():
                            if val == ":self":
                                kwargs[key] = self
                            elif val.startswith(":f"):
                                prop = val.split(".")[1]
                                kwargs[key] = getattr(attr, prop)
                        func = Depends(func(**kwargs))
                    else:
                        func = Depends(func)
                    data["dependencies"].append(func)

                path, methods, rest_data = (
                    data["path"],
                    data["methods"],
                    {k: v for k, v in data.items() if k != "methods"},
                )

                self.messages.append(
                    f"Registering route {self.router.prefix}{path} {methods}"
                )

                for method in methods:
                    method = method.lower()
                    router_func = getattr(self.router, method)

                    priority = getattr(attr, "_priority", None)

                    # If it is a bound method of a class, get the function
                    if hasattr(attr, "__func__"):
                        attr = attr.__func__

                    #! Update self parameter in the function signature, so that self is not treated as a parameter
                    attr = update_signature(self, attr)

                    if priority is not None:
                        priority_routes.append((priority, router_func, rest_data, attr))
                        continue

                    # Add the route to the router
                    router_func(**rest_data)(attr)

        # Sort the priority routes by priority
        priority_routes.sort(key=lambda x: x[0], reverse=True)

        # Add the priority routes to the router
        for _, router_func, rest_data, attr in priority_routes:
            router_func(**rest_data)(attr)

    def _is_in_base_permissions(self, permission: str):
        """
        Check if the permission is in the `base_permissions`.

        If the `base_permissions` are not set, it will return True.

        Args:
            permission (str): The permission to check.

        Returns:
            bool: True if the permission is in the `base_permissions` or if the `base_permissions` are not set, False otherwise.
        """
        return (
            f"{PERMISSION_PREFIX}{permission}" in self.base_permissions
            if self.base_permissions
            else True
        )
