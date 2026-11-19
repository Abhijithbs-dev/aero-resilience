"""
Integration tests for HTTP server, endpoints, and error handling.
"""
import json
import threading
import time
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer

from backend.server import SmogAssistantRequestHandler

TEST_PORT = 8999
BASE_URL = f"http://127.0.0.1:{TEST_PORT}"

class TestAPIServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", TEST_PORT), SmogAssistantRequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self):
        url = f"{BASE_URL}/api/health"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data["status"], "healthy")
            self.assertIn("AeroResilience" in data["service"] or "Smog" in data["service"], [True])

    def test_presets_endpoint(self):
        url = f"{BASE_URL}/api/presets"
        with urllib.request.urlopen(url, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("Severe", data)
            self.assertIn("Moderate", data)
            self.assertEqual(data["Severe"]["aqi"], 420)

    def test_aqi_endpoint_delhi(self):
        url = f"{BASE_URL}/api/aqi?city=Delhi"
        with urllib.request.urlopen(url, timeout=15) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("aqi", data)
            self.assertIn("pm2_5", data)
            self.assertIn("severity_tier", data)

    def test_recommendations_endpoint_valid_payload(self):
        url = f"{BASE_URL}/api/recommendations"
        payload = {
            "location": "Delhi-NCR",
            "preset_severity": "Severe",
            "commute_mode": "two_wheeler",
            "housing_type": "apartment",
            "cooking_heating": "lpg_gas",
            "budget_tier": "low_cost",
            "vulnerable_members": ["children", "asthma"]
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("risk_summary", data)
            self.assertIn("daily_routines", data)
            self.assertIn("iaq_hacks", data)
            self.assertIn("sustainable_alternatives", data)
            self.assertIn("direct_impacts", data)
            self.assertEqual(data["risk_summary"]["severity_tier"], "Severe")

    def test_static_index_serving(self):
        url = f"{BASE_URL}/"
        with urllib.request.urlopen(url, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            content = resp.read().decode()
            self.assertIn("<title>", content)
            self.assertIn("AeroResilience", content)

    def test_distinct_microclimates_for_different_locations(self):
        """Verify that different locations return distinct real-time atmospheric microclimates."""
        url_mumbai = f"{BASE_URL}/api/aqi?city=Mumbai"
        url_london = f"{BASE_URL}/api/aqi?city=London"

        with urllib.request.urlopen(url_mumbai, timeout=15) as r1:
            data_mumbai = json.loads(r1.read().decode())
        with urllib.request.urlopen(url_london, timeout=15) as r2:
            data_london = json.loads(r2.read().decode())

        self.assertIn("temperature", data_mumbai)
        self.assertIn("temperature", data_london)
        self.assertIn("humidity", data_mumbai)
        self.assertIn("humidity", data_london)
        self.assertIn("wind_speed", data_mumbai)
        self.assertIn("wind_speed", data_london)

        # Microclimates must be distinct between tropical Mumbai and temperate London
        self.assertNotEqual(data_mumbai["temperature"], data_london["temperature"])
        self.assertNotEqual(data_mumbai["latitude"], data_london["latitude"])

    def test_malformed_json_handling(self):
        url = f"{BASE_URL}/api/recommendations"
        bad_bytes = b"this is not json {{"
        req = urllib.request.Request(url, data=bad_bytes, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 400)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
            e.close()

    def test_slides_endpoint(self):
        url = f"{BASE_URL}/slides.html"
        with urllib.request.urlopen(url, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            html = resp.read().decode("utf-8")
            self.assertIn("AeroResilience", html)
            self.assertIn("slide-card", html)

if __name__ == "__main__":
    unittest.main()
