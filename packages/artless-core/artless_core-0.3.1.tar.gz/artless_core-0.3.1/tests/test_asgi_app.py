from collections import deque
from http import HTTPStatus
from logging import getLogger
from re import compile
from typing import Any, Awaitable, Callable, Deque
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from artless import (
    ASGIApp,
    ASGIReceiveT,
    ASGISendT,
    Config,
    Request,
    Response,
    plain,
)

logger = getLogger("artless")
config = Config()


class ASGITestClient:
    def __init__(self, app: ASGIApp):
        self.app = app
        self.received: Deque = deque()

    async def __call__(self, scope: dict[str, Any], receive: ASGIReceiveT, send: ASGISendT) -> None:
        async def intercepted_send(message: dict[str, Any]) -> None:
            self.received.append(message)
            await send(message)

        await self.app(scope, receive, intercepted_send)


class TestASGIApp(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app = ASGIApp()
        self.client = ASGITestClient(self.app)
        self.default_scope = {
            "type": "http",
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "headers": [(b"Accept", b"*/*")],
        }
        self.default_receive_data = {
            "type": "http.request.body",
            "body": b"",
            "more_body": False,
        }

    def tearDown(self) -> None:
        config.replace({"debug": False})

    async def _make_request(
        self,
        scope_overrides: dict[str, Any] | None = None,
        receive_data: dict[str, Any] | None = None,
    ) -> None:
        scope = {**self.default_scope, **(scope_overrides or {})}
        receive_data = receive_data or self.default_receive_data

        async def receive() -> dict[str, Any]:
            return receive_data

        async def send(message: dict[str, Any]) -> None:
            pass

        await self.client(scope, receive, send)

    async def test_app_protocol(self) -> None:
        self.assertTrue(callable(self.app))

    async def test_setting_unique_routes(self) -> None:
        async def sample_handler() -> None:
            pass

        self.app.set_routes(
            [
                ("GET", "/test/url/1/", sample_handler),
                ("GET", "/test/url/2/", sample_handler),
            ]
        )

        self.assertEqual(
            self.app.routes,
            {
                "GET": {
                    compile(r"/test/url/1/"): sample_handler,
                    compile(r"/test/url/2/"): sample_handler,
                },
            },
        )

    async def test_setting_same_routes(self) -> None:
        async def sample_handler() -> None:
            pass

        url = "/test/url/1/"

        with self.assertRaises(ValueError) as exc:
            self.app.set_routes(
                [
                    ("GET", url, sample_handler),
                    ("GET", url, sample_handler),
                ]
            )

        self.assertEqual(str(exc.exception), f'Route "GET {url}" already exists!')

    async def test_regular_calling_asgi_app(self) -> None:
        async def ping_handler(request: Request) -> Response:
            return plain("pong")

        self.app.set_routes([("GET", "/ping/", ping_handler)])
        await self._make_request({"path": "/ping/"})

        response_head, response_tail = self.client.received
        self.assertEqual(response_head["type"], "http.response.start")
        self.assertEqual(response_head["status"], HTTPStatus.OK)
        self.assertEqual(
            response_head["headers"],
            [(b"Content-Type", b"text/plain"), (b"Content-Length", b"5")],
        )
        self.assertEqual(response_tail["type"], "http.response.body")
        self.assertEqual(response_tail["body"], b"pong\n")

    async def test_not_http_asgi_request(self) -> None:
        await self._make_request({"type": "rmq"})

        response_head, response_tail = self.client.received
        self.assertEqual(response_head["type"], "http.response.start")
        self.assertEqual(response_head["status"], HTTPStatus.NOT_IMPLEMENTED)
        self.assertEqual(response_head["headers"], [(b"Content-Type", b"text/plain")])
        self.assertEqual(response_tail["type"], "http.response.body")
        self.assertEqual(response_tail["body"], b"")

    async def test_not_http_asgi_request_with_invalid_body_type(self) -> None:
        async def ping_handler(request: Request) -> Response:
            return plain("pong")

        self.app.set_routes([("GET", "/ping/", ping_handler)])
        await self._make_request(
            {"path": "/ping/"},
            {"more_body": True, "type": "http.invalid.type"},
        )

        response_head, response_tail = self.client.received
        self.assertEqual(response_head["type"], "http.response.start")
        self.assertEqual(response_head["status"], HTTPStatus.OK)
        self.assertEqual(
            response_head["headers"],
            [(b"Content-Type", b"text/plain"), (b"Content-Length", b"5")],
        )
        self.assertEqual(response_tail["type"], "http.response.body")
        self.assertEqual(response_tail["body"], b"pong\n")

    async def test_request_with_invalid_method(self) -> None:
        self.app.set_routes([("GET", "/", lambda _: None)])
        await self._make_request({"method": "POST"})

        response_head, response_tail = self.client.received
        self.assertEqual(response_head["type"], "http.response.start")
        self.assertEqual(response_head["status"], HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertEqual(response_head["headers"], [(b"Content-Type", b"text/plain")])
        self.assertEqual(response_tail["type"], "http.response.body")
        self.assertEqual(response_tail["body"], b"")

    async def test_request_not_found(self) -> None:
        async def ping_handler(request: Request) -> Response:
            return plain("pong")

        self.app.set_routes([("GET", r"^/$", ping_handler)])
        await self._make_request({"path": "/not/found/resource"})

        response_head, _ = self.client.received
        self.assertEqual(response_head["status"], HTTPStatus.NOT_FOUND)

    async def test_request_with_error(self) -> None:
        async def ping_handler(request: Request) -> None:
            raise Exception("Test")

        self.app.set_routes([("GET", r"^/$", ping_handler)])

        with self.subTest("DEBUG mode is False"):
            with patch.object(logger, "error") as mock_logger:
                await self._make_request()

            response_head, response_tail = self.client.received
            self.assertEqual(response_head["status"], HTTPStatus.INTERNAL_SERVER_ERROR)
            self.assertEqual(response_tail["body"], b"")
            mock_logger.assert_called_once()

        with self.subTest("DEBUG mode is True"):
            config.replace({"debug": True})
            with patch.object(logger, "error") as mock_logger:
                await self._make_request()

            *_, response_head, response_tail = self.client.received
            self.assertEqual(response_head["status"], HTTPStatus.INTERNAL_SERVER_ERROR)
            self.assertNotEqual(response_tail["body"], b"")
            mock_logger.assert_called_once()
            config.replace({"debug": False})

    async def test_regular_calling_asgi_app_with_query_string(self) -> None:
        async def ping_handler(request: Request) -> Response:
            self.assertEqual(request.url, "/ping/?param1=value1&param1=value2&param2=value")
            self.assertEqual(request.path, "/ping/")
            self.assertEqual(request.query, "param1=value1&param1=value2&param2=value")
            self.assertEqual(request.params, {"param1": ["value1", "value2"], "param2": "value"})
            return plain("pong")

        self.app.set_routes([("GET", "/ping/", ping_handler)])
        await self._make_request(
            {
                "path": "/ping/",
                "query_string": b"param1=value1&param1=value2&param2=value",
            }
        )

        response_head, response_tail = self.client.received
        self.assertEqual(response_head["type"], "http.response.start")
        self.assertEqual(response_head["status"], HTTPStatus.OK)
        self.assertEqual(
            response_head["headers"],
            [(b"Content-Type", b"text/plain"), (b"Content-Length", b"5")],
        )
        self.assertEqual(response_tail["type"], "http.response.body")
        self.assertEqual(response_tail["body"], b"pong\n")
