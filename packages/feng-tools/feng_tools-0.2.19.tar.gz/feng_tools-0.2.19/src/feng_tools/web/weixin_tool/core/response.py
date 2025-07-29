"""自定义响应"""
import typing

from starlette.responses import Response


class XmlResponse(Response):
    media_type = "text/xml"

    def render(self, content: typing.Any) -> bytes:
        return content.encode("utf-8")
