import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from app import SiteHandler


class SeasonsWebsiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), SiteHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path):
        return urlopen(f"{self.base_url}{path}", timeout=3)

    def test_home_page_contains_all_seasons(self):
        with self.request("/") as response:
            content = response.read().decode("utf-8")
            self.assertEqual(response.status, 200)
            for season_name in ("Spring", "Summer", "Autumn", "Winter"):
                self.assertIn(season_name, content)

    def test_each_season_page_loads(self):
        for slug in ("spring", "summer", "autumn", "winter"):
            with self.subTest(slug=slug), self.request(f"/season/{slug}") as response:
                self.assertEqual(response.status, 200)

    def test_unknown_season_returns_404(self):
        with self.assertRaises(HTTPError) as error:
            self.request("/season/monsoon")
        self.assertEqual(error.exception.code, 404)

    def test_api_returns_four_seasons(self):
        with self.request("/api/seasons") as response:
            data = json.load(response)
        self.assertEqual(len(data["seasons"]), 4)

    def test_static_image_is_available(self):
        with self.request("/static/images/spring-kunming.jpg") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "image/jpeg")

    def test_health_check(self):
        with self.request("/health") as response:
            data = json.load(response)
        self.assertEqual(data, {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
