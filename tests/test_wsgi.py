import json
import unittest

from pythonanywhere_wsgi import application


def request(path, method="GET"):
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "SERVER_NAME": "testserver",
        "SERVER_PORT": "80",
    }
    result = {}

    def start_response(status, headers):
        result["status"] = status
        result["headers"] = dict(headers)

    body = b"".join(application(environ, start_response))
    return result, body


class WsgiApplicationTests(unittest.TestCase):
    def test_home_page(self):
        result, body = request("/")
        self.assertEqual(result["status"], "200 OK")
        self.assertIn(b"Spring", body)
        self.assertIn(b"Winter", body)

    def test_season_page(self):
        result, body = request("/season/autumn")
        self.assertEqual(result["status"], "200 OK")
        self.assertIn(b"Albert Camus", body)

    def test_api(self):
        result, body = request("/api/seasons")
        self.assertEqual(result["status"], "200 OK")
        self.assertEqual(len(json.loads(body)["seasons"]), 4)

    def test_static_image(self):
        result, body = request("/static/images/spring-kunming.jpg")
        self.assertEqual(result["status"], "200 OK")
        self.assertEqual(result["headers"]["Content-Type"], "image/jpeg")
        self.assertGreater(len(body), 10000)

    def test_unknown_route(self):
        result, _ = request("/not-a-page")
        self.assertEqual(result["status"], "404 Not Found")


if __name__ == "__main__":
    unittest.main()
