from io import BytesIO
from clovers import Result, Plugin
from io import BytesIO
from clovers import EventProtocol, Result, Plugin
from typing import Protocol, Literal, overload


class Event(EventProtocol, Protocol):
    user_id: str
    group_id: str | None
    tarot: None

    @overload
    async def call(self, key: Literal["text"], message: str): ...

    @overload
    async def call(self, key: Literal["image"], message: BytesIO | bytes): ...

    @overload
    async def call(self, key: Literal["list"], message: list[Result]): ...


def build_result(result):
    if isinstance(result, Result):
        return result
    if isinstance(result, str):
        return Result("text", result)
    if isinstance(result, BytesIO):
        return Result("image", result)
    if isinstance(result, list):
        return Result("list", [build_result(seg) for seg in result if seg])


def create_plugin() -> Plugin:
    plugin = Plugin(build_result=build_result, priority=10)
    plugin.set_protocol("properties", Event)
    return plugin
