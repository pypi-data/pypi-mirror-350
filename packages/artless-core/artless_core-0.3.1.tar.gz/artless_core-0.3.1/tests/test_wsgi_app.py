from io import BytesIO
from logging import getLogger
from re import compile
from typing import MutableMapping
from unittest import TestCase
from unittest.mock import Mock, patch

from artless import Config, Request, Response, WSGIApp, plain

logger = getLogger("artless")
config = Config()


def start_response(*args, **kwargs):
    pass


class TestWSGIApp(TestCase):
    def test_app_protocol(self):
        app = WSGIApp()

        self.assertTrue(callable(app))

    def test_setting_unique_routes(self):
        def sample_handler():
            pass

        app = WSGIApp()
        app.set_routes([("GET", "/test/url/1/", sample_handler), ("GET", "/test/url/2/", sample_handler)])

        self.assertEqual(
            app.routes,
            {
                "GET": {
                    compile(r"/test/url/1/"): sample_handler,
                    compile(r"/test/url/2/"): sample_handler,
                },
            },
        )

    def test_setting_same_routes(self):
        def sample_handler():
            pass

        app = WSGIApp()
        url = "/test/url/1/"

        with self.assertRaises(ValueError) as exc:
            app.set_routes([("GET", url, sample_handler), ("GET", url, sample_handler)])

        self.assertEqual(str(exc.exception), f'Route "GET {url}" already exists!')

    def test_regular_calling_wsgi_app(self):
        def ping_handler(request):
            return plain("pong")

        environ = {
            "SCRIPT_URL": "",
            "PATH_INFO": "/ping/",
            "CONTENT_LENGTH": 0,
            "REQUEST_METHOD": "GET",
            "QUERY_STRING": "?p1=1&p2=2",
            "HTTP_HOST": "test.com",
            "HTTP_USER_AGENT": "test ua",
            "HTTP_CONTENT_TYPE": "text/plain; charset=utf-8",
            "wsgi.input": BytesIO(),
        }
        app = WSGIApp()
        app.set_routes([("GET", "/ping/", ping_handler)])

        response_body = app(environ, start_response)

        self.assertEqual(response_body[0], b"pong\n")

    def test_calling_wsgi_app_with_not_allowed_method(self):
        environ = {
            "SCRIPT_URL": "",
            "PATH_INFO": "/ping/",
            "CONTENT_LENGTH": 0,
            "REQUEST_METHOD": "GET",
            "QUERY_STRING": "",
            "HTTP_HOST": "test.com",
            "HTTP_USER_AGENT": "test ua",
            "HTTP_CONTENT_TYPE": "text/plain; charset=utf-8",
            "wsgi.input": BytesIO(),
        }

        def _fake_wsgi_response(start_response, response):
            self.assertEqual(response.status, ("405 Method Not Allowed"))

        app = WSGIApp()
        app.set_routes([("POST", "/ping/", lambda: None)])
        app._wsgi_response = _fake_wsgi_response

        app(environ, start_response)

    def test_calling_wsgi_app_with_unexpected_url(self):
        environ = {
            "SCRIPT_URL": "",
            "PATH_INFO": "/some/resource/",
            "CONTENT_LENGTH": 0,
            "REQUEST_METHOD": "GET",
            "QUERY_STRING": "",
            "HTTP_HOST": "test.com",
            "HTTP_USER_AGENT": "test ua",
            "HTTP_CONTENT_TYPE": "text/plain; charset=utf-8",
            "wsgi.input": BytesIO(),
        }

        def _fake_wsgi_response(start_response, response):
            self.assertEqual(response.status, ("404 Not Found"))

        app = WSGIApp()
        app.set_routes([("GET", "/ping/", lambda: None)])
        app._wsgi_response = _fake_wsgi_response
        app(environ, start_response)

    def test_calling_wsgi_app_internal_server_error(self):
        environ = {
            "SCRIPT_URL": "",
            "PATH_INFO": "/some/resource/",
            "CONTENT_LENGTH": 0,
            "REQUEST_METHOD": "GET",
            "QUERY_STRING": "",
            "HTTP_HOST": "test.com",
            "HTTP_USER_AGENT": "test ua",
            "HTTP_CONTENT_TYPE": "text/plain; charset=utf-8",
            "wsgi.input": BytesIO(),
        }

        def _fake_wsgi_response(start_response, response):
            self.assertEqual(response.status, ("500 Internal Server Error"))

        def _fake_request_hanler(*args, **kwargs):
            raise Exception("Some server error")

        with self.subTest("DEBUG mode is FALSE"):
            app = WSGIApp()
            app.set_routes([("GET", "/some/resource/", _fake_request_hanler)])
            app._wsgi_response = _fake_wsgi_response

            with patch.object(logger, "error") as mock_logger:
                app(environ, start_response)

            mock_logger.assert_called_once()

        with self.subTest("DEBUG mode is TRUE"):
            config.replace({"debug": True})
            app = WSGIApp()
            app.set_routes([("GET", "/some/resource/", _fake_request_hanler)])
            app._wsgi_response = _fake_wsgi_response

            with patch.object(logger, "error") as mock_logger:
                app(environ, start_response)

            mock_logger.assert_called_once()
