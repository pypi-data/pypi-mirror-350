from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `system_prompt_storage.resources` module.

    This is used so that we can lazily import `system_prompt_storage.resources` only when
    needed *and* so that users can just import `system_prompt_storage` and reference `system_prompt_storage.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("system_prompt_storage.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
