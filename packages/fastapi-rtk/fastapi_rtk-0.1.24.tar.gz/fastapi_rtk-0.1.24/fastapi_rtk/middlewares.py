import os
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .globals import g
from .setting import Setting

__all__ = ["ProfilerMiddleware"]


async def profiler_middleware_dispatch(
    request: Request,
    call_next: Callable,
) -> Response:
    """
    Profile the current request

    Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
    with small improvements.
    """
    profile_type = Setting.PROFILER_TYPE
    renderer_name = Setting.PROFILER_RENDERER
    if not g.renderer_cache:
        g.renderer_cache = {}
    renderer = g.renderer_cache.get(renderer_name)
    if not renderer:
        renderer = getattr(g.pyinstrument.renderers, renderer_name)()
        g.renderer_cache[renderer_name] = renderer

    # we profile the request along with all additional middlewares, by interrupting
    # the program every 1ms1 and records the entire stack at that point
    with g.pyinstrument.Profiler(
        interval=0.0001, async_mode="enabled", use_timing_thread=True
    ) as profiler:
        response = await call_next(request)

    # we dump the profiling into a file
    folder_name = Setting.PROFILER_FOLDER + request.url.path
    os.makedirs(
        folder_name,
        exist_ok=True,
    )
    file_name = folder_name + f"/{request.method}.{profile_type}"
    with open(file_name, "w") as out:
        out.write(profiler.output(renderer=renderer))
    return response


class ProfilerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        os.makedirs(Setting.PROFILER_FOLDER, exist_ok=True)
        super().__init__(app, profiler_middleware_dispatch)
