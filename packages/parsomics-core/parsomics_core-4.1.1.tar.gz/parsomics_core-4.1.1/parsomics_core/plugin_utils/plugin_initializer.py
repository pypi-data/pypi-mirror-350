from typing import Callable

from pydantic import BaseModel


class PluginInitializer(BaseModel):
    subject: str
    plugin_name: str
    populate_func: Callable
