from typing import Callable, Any, Optional, Dict, Union

class API:
    def add_route(self, uri_template: str, resource: Callable[..., None]) -> None: ...
    def add_sink(self, sink: Callable[..., None]) -> None: ...
    def set_error_serializer(self, serializer: Callable[[Exception, Any, Any], None]) -> None: ...

class Request:
    method: str
    path: str
    relative_uri: str
    url: str
    context: Dict[str, Any]
    headers: Dict[str, str]
    media: Any
    client_accepts_json: bool

    def get_param(self, name: str, default: Optional[str] = None) -> Optional[str]: ...

class Response:
    status: str
    headers: Dict[str, str]
    body: bytes
    context: Dict[str, Any]
    media: Any

    def set_header(self, name: str, value: Union[str, int, float]) -> None: ...
    def set_media(self, media: Any) -> None: ...
    def set_status(self, status: str) -> None: ...
