"""
007 Security Hardening & Red Team Attack Suite
Executes active penetration probes and threat modeling against AeroResilience endpoints.
"""
import json
import os
import unittest
import urllib.error
import urllib.request

class Test007SecurityAudit(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8000"

    def test_red_team_oversized_payload_dos(self):
        """Red Team Attack 1: Send oversized payload (>50KB) to attempt buffer overflow / DoS."""
        oversized = "A" * 60000
        payload = json.dumps({"location": oversized, "user_question": oversized}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/recommendations",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req, timeout=3)
            self.fail("Server should reject oversized payload with 413")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 413, "Expected 413 Payload Too Large")
            body = json.loads(e.read().decode())
            e.close()
            self.assertIn("error", body)

    def test_red_team_malformed_json_fuzzing(self):
        """Red Team Attack 2: Send invalid/malformed JSON to test error boundary."""
        garbage_data = b"{{invalid_json;;<<<>>>"
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/recommendations",
            data=garbage_data,
            headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req, timeout=3)
            self.fail("Server should reject malformed JSON with 400")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400, "Expected 400 Bad Request")
            body = json.loads(e.read().decode())
            e.close()
            self.assertIn("error", body)

    def test_red_team_path_traversal(self):
        """Red Team Attack 3: Directory traversal probes to access sensitive OS files."""
        probes = [
            "/../../../../etc/passwd",
            "/..%2F..%2F..%2Fetc/passwd",
            "/frontend/../../app.py",
            "/%2e%2e/%2e%2e/backend/server.py",
            "/styles.css/../../app.py"
        ]
        for probe in probes:
            req = urllib.request.Request(f"{self.BASE_URL}{probe}")
            try:
                urllib.request.urlopen(req, timeout=3)
                self.fail(f"Path traversal probe {probe} was not blocked!")
            except urllib.error.HTTPError as e:
                code = e.code
                e.close()
                self.assertIn(code, [400, 403, 404], f"Expected 400, 403 or 404 on traversal, got {code}")

    def test_red_team_xss_and_html_injection(self):
        """Red Team Attack 4: Script tags and SVG event handlers in user inputs."""
        xss_payload = {
            "location": "<script>alert('xss_location')</script>",
            "aqi_input_type": "preset",
            "preset_severity": "Severe",
            "user_question": "<img src=x onerror=alert('xss_img')>"
        }
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/recommendations",
            data=json.dumps(xss_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            # Output must NOT contain unescaped script tag or unescaped onerror handler
            raw_str = json.dumps(data)
            self.assertNotIn("<script>", raw_str)
            self.assertNotIn("<img src=x", raw_str)

    def test_blue_team_security_headers_present(self):
        """Blue Team Check: Confirm strict CSP, nosniff, frame options, and referrer policy."""
        req = urllib.request.Request(f"{self.BASE_URL}/")
        with urllib.request.urlopen(req, timeout=3) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            self.assertEqual(headers.get("x-content-type-options"), "nosniff")
            self.assertEqual(headers.get("x-frame-options"), "DENY")
            self.assertEqual(headers.get("referrer-policy"), "no-referrer")
            self.assertIn("content-security-policy", headers)
            self.assertIn("default-src 'self'", headers["content-security-policy"])

if __name__ == "__main__":
    unittest.main()
