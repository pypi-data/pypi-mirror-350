"""The artless and minimalistic web library for creating small applications or APIs."""

__author__ = "Peter Bro"
__version__ = "0.3.1"
__license__ = "MIT"
__all__ = ["ASGIApp", "Config", "Request", "Response", "WSGIApp", "html", "json", "plain", "redirect"]

from copy import deepcopy
from datetime import datetime
from http import HTTPStatus
from logging import Logger, config, getLogger
from re import Pattern, compile, match
from traceback import format_exc
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    ParamSpec,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    runtime_checkable,
)
from urllib.parse import SplitResult, parse_qs, quote, urlsplit
from uuid import UUID, uuid4
from wsgiref.types import StartResponse, WSGIEnvironment

# Prioritized import of josn library: orjson || ujson || cjson || json (standart module)
try:
    from orjson import JSONEncoder, loads
except ImportError:
    try:
        from json import JSONEncoder

        from ujson import loads
    except ImportError:
        try:
            from cjson import JSONEncoder, loads
        except ImportError:
            from json import JSONEncoder, loads

T = TypeVar("T")
P = ParamSpec("P")

CommonDictT = dict[str, Any]
CommonDataT = Mapping | Sequence[T] | str | int | float | bool | datetime | None

ASGIReceiveT = Callable[[], Awaitable[Any]]
ASGISendT = Callable[[CommonDictT], Awaitable[None]]

RouteT = tuple[str, str, Callable]
HandlerT = Callable[["Request"], "Response"]
RoutingTableT = MutableMapping[str, MutableMapping[Pattern, HandlerT]]

WSGI_HTTP_PREFIX: str = "HTTP_"
WSGI_UNPREFIXED_HEADERS: frozenset[str] = frozenset(["CONTENT_TYPE", "CONTENT_LENGTH"])
ASGI_SCOPE_TYPE: str = "http"
ASGI_REQUEST_BODY_TYPE: str = "http.request.body"
ASGI_RESPONSE_START_TYPE: str = "http.response.start"
ASGI_RESPONSE_BODY_TYPE: str = "http.response.body"
CTYPE_HEADER_NAME: str = "Content-Type"
DEFAULT_CTYPE: str = "text/plain"
DEFAULT_CONFIG: CommonDictT = {
    "debug": False,
    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[{asctime}] [{process:d}] [{levelname}] {message}",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "style": "{",
            },
        },
        "handlers": {
            "stdout": {
                "formatter": "default",
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "artless": {
                "level": "INFO",
                "handlers": ["stdout"],
                "propagate": False,
            }
        },
        "root": {"level": "WARNING", "handlers": ["stdout"]},
    },
}


@runtime_checkable
class BodyDecoder(Protocol):
    def decode(self, body: bytes) -> Mapping[str, CommonDataT]: ...


class Config:
    __config: CommonDictT
    _instance: ClassVar[Optional["Config"]] = None

    def __new__(cls: Type["Config"]):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__config = deepcopy(DEFAULT_CONFIG)
        return cls._instance

    def __getattr__(self, name: str) -> Any:
        return self.__config[name]

    @property
    def current(self) -> CommonDictT:
        return self.__config

    def replace(self, params: CommonDictT) -> None:
        self.__config |= params


config.dictConfig(Config().logging)
logger: Logger = getLogger(__name__)


def encode_json(data: CommonDataT, encoder: Type[JSONEncoder] = JSONEncoder) -> str:
    return encoder().encode(data)


class WSGIHeadersParser:
    __slots__ = ("headers",)

    def __init__(self, environ: WSGIEnvironment) -> None:
        self.headers: Mapping[str, str] = {}

        for header, value in environ.items():
            if name := self._transcribe_header_name(header):
                self.headers[name] = value

    def _transcribe_header_name(self, header: str) -> Optional[str]:
        if header.startswith(WSGI_HTTP_PREFIX):
            # NOTE: hardcoded constant length instead of calculating len(WSGI_HTTP_PREFIX)
            header = header[5:]
        elif header not in WSGI_UNPREFIXED_HEADERS:
            return None
        return header.replace("_", "-").title()


class ASGIHeadersParser:
    __slots__ = ("headers",)

    def __init__(self, raw_headers: Sequence[tuple[bytes, bytes]]) -> None:
        self.headers: Mapping[str, str] = {}

        for name, value in raw_headers:
            self.headers[name.decode().title()] = value.decode()


class JSONBodyDecoder(BodyDecoder):
    def decode(self, body: bytes) -> CommonDictT:
        return loads(body)


class WWWFormBodyDecoder(BodyDecoder):
    def decode(self, body: bytes) -> CommonDictT:
        result = {}
        for param, value in parse_qs(body.decode()).items():
            result[param] = value if len(value) > 1 else value[0]
        return result


class Request:
    __slots__ = ("_splitted_url", "body", "headers", "id", "method", "params", "url")

    def __init__(self, method: str, url: str, headers: Mapping[str, str], body: bytes) -> None:
        self.id: UUID = uuid4()
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

        self._splitted_url: SplitResult = urlsplit(self.url)

        # Unpack single values ​​for simplicity
        self.params: CommonDictT = {
            param: (values[0] if len(values) == 1 else values)
            for param, values in parse_qs(self._splitted_url.query).items()
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.method} {self.url}>"

    @property
    def path(self) -> str:
        return self._splitted_url.path

    @property
    def query(self) -> str:
        return self._splitted_url.query

    @property
    def fragment(self) -> str:
        return self._splitted_url.fragment

    @property
    def content_type(self) -> str:
        return self.headers.get("Content-Type", "").partition(";")[0]

    @property
    def user_agent(self) -> Optional[str]:
        return self.headers.get("User-Agent")

    @property
    def json(self) -> CommonDictT:
        if self.content_type != "application/json":
            raise ValueError("Content type does not match as a json")
        return JSONBodyDecoder().decode(self.body)

    @property
    def form(self) -> CommonDictT:
        if self.content_type != "application/x-www-form-urlencoded":
            raise ValueError("Content type does not match as a form")
        return WWWFormBodyDecoder().decode(self.body)


class Response:
    __slots__ = ("_body", "_status", "headers")

    def __init__(self, *, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._body: bytes = b""
        self._status: HTTPStatus = status
        self.headers: MutableMapping[str, str] = {CTYPE_HEADER_NAME: DEFAULT_CTYPE}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.status}>"

    @property
    def status(self) -> str:
        return f"{self._status.value} {self._status.phrase}"

    @status.setter
    def status(self, status: HTTPStatus) -> None:
        self._status = status

    @property
    def content_type(self) -> str:
        return self.headers[CTYPE_HEADER_NAME]

    @content_type.setter
    def content_type(self, value: str) -> None:
        self.headers[CTYPE_HEADER_NAME] = value

    @property
    def body(self) -> bytes:
        return self._body

    @body.setter
    def body(self, data: Union[str, bytes]) -> None:
        if isinstance(data, str):
            self._body = (data + "\n").encode("utf-8")
        elif isinstance(data, bytes):
            data += b"\n"
            self._body = data
        else:
            raise TypeError(f"Response body must be only string or bytes, not {type(data)}")
        self.headers["Content-Length"] = str(len(self._body))

    def _dump_headers(self, need_encode: bool = False) -> list[tuple[str, str] | tuple[bytes, bytes]]:
        return (
            [(name.encode(), value.encode()) for name, value in self.headers.items()]
            if need_encode
            else [(name, value) for name, value in self.headers.items()]
        )


class BaseApp:
    __slots__ = ("routes",)

    def __init__(self) -> None:
        self.routes: RoutingTableT = {}

    def add_route(self, route: RouteT) -> None:
        method, path, handler = route
        method = method.upper()
        compiled_re_path: Pattern = compile(path)
        if method not in self.routes:
            self.routes[method] = {}
        if compiled_re_path in self.routes[method]:
            raise ValueError(f'Route "{method} {path}" already exists!')
        self.routes[method][compiled_re_path] = handler

    def set_routes(self, routes: Sequence[RouteT]) -> None:
        for route in routes:
            self.add_route(route)


class WSGIApp(BaseApp):
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        script_name: str = environ.get("SCRIPT_NAME", "").rstrip("/")
        path_info: str = (
            environ.get("PATH_INFO", "/").replace("/", "", 1).encode("latin-1").decode("utf-8", "ignore")
        )
        url: str = f"{script_name}/{path_info}"
        if query_string := environ.get("QUERY_STRING"):
            url += f"?{query_string}"

        request = Request(
            method=environ["REQUEST_METHOD"].upper(),
            url=url,
            headers=WSGIHeadersParser(environ).headers,
            body=environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH") or "0")),
        )

        method, path = (request.method, request.path)
        if method not in self.routes:
            return self._wsgi_response(start_response, Response(status=HTTPStatus.METHOD_NOT_ALLOWED))

        handler, params = (None, {})
        for pattern, _handler in self.routes[method].items():
            if match_result := match(pattern, path):
                handler, params = (_handler, match_result.groupdict())

        if not handler:
            return self._wsgi_response(start_response, Response(status=HTTPStatus.NOT_FOUND))

        try:
            response = handler(request, **params)
        except Exception:
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            stack_trace = format_exc()
            if Config().debug:
                response.body = stack_trace  # type: ignore[assignment]
            logger.error(f"[{request.id}] {stack_trace}")

        return self._wsgi_response(start_response, response)

    @staticmethod
    def _wsgi_response(start_response: StartResponse, response: Response) -> Iterable[bytes]:
        headers = cast(list[tuple[str, str]], response._dump_headers())
        start_response(response.status, headers)
        return [response.body]


class ASGIApp(BaseApp):
    async def __call__(self, scope: CommonDictT, receive: ASGIReceiveT, send: ASGISendT) -> None:
        if scope["type"] != ASGI_SCOPE_TYPE:
            await self._asgi_response(send, Response(status=HTTPStatus.NOT_IMPLEMENTED))
            return None

        request = Request(
            method=scope["method"],
            url=self._get_url(scope),
            headers=ASGIHeadersParser(scope["headers"]).headers,
            body=await self._get_body(receive),
        )

        method, path = (request.method, request.path)
        if method not in self.routes:
            await self._asgi_response(send, Response(status=HTTPStatus.METHOD_NOT_ALLOWED))
            return None

        handler, params = (None, {})
        for pattern, _handler in self.routes[method].items():
            if match_result := match(pattern, path):
                handler, params = (_handler, match_result.groupdict())

        if not handler:
            await self._asgi_response(send, Response(status=HTTPStatus.NOT_FOUND))
            return None

        try:
            response = await handler(request, **params)  # type: ignore[misc]
        except Exception:
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            stack_trace = format_exc()
            if Config().debug:
                response.body = stack_trace
            logger.error(f"[{request.id}] {stack_trace}")

        await self._asgi_response(send, response)

    @staticmethod
    async def _asgi_response(send: ASGISendT, response: Response) -> None:
        await send(
            {
                "type": ASGI_RESPONSE_START_TYPE,
                "status": response._status.value,
                "headers": response._dump_headers(need_encode=True),
            }
        )
        await send({"type": ASGI_RESPONSE_BODY_TYPE, "body": response.body})

    @staticmethod
    def _get_url(scope: CommonDictT) -> str:
        url = scope["path"]
        if query_string := scope["query_string"]:
            url += f"?{query_string.decode()}"
        return url

    @staticmethod
    async def _get_body(receive: ASGIReceiveT) -> bytes:
        body, more_body = b"", True

        while more_body:
            message = await receive()
            if message["type"] != ASGI_REQUEST_BODY_TYPE:
                break
            body += message.get("body", b"")
            more_body = message.get("more_body", False)

        return body


def plain(message: str, /, *, status: HTTPStatus = HTTPStatus.OK) -> Response:
    response = Response(status=status)
    response.body = message  # type: ignore[assignment]
    return response


def html(template: str, /, *, status: HTTPStatus = HTTPStatus.OK) -> Response:
    response = Response(status=status)
    response.content_type = "text/html"
    response.body = template  # type: ignore[assignment]
    return response


def json(data: CommonDataT, /, *, status: HTTPStatus = HTTPStatus.OK) -> Response:
    response = Response(status=status)
    response.content_type = "application/json"
    response.body = encode_json(data)  # type: ignore[assignment]
    return response


def redirect(url: str, /, *, status: HTTPStatus = HTTPStatus.MOVED_PERMANENTLY) -> Response:
    response = Response(status=status)
    response.headers["Location"] = quote(url)
    del response.headers[CTYPE_HEADER_NAME]
    return response
