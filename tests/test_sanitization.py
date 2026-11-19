"""
Unit tests for input sanitization, validation, and boundary defenses.
"""
import unittest
from backend.utils.sanitization import (
    sanitize_string, validate_aqi, validate_pm25, validate_choice, sanitize_household_payload
)

class TestSanitization(unittest.TestCase):
    def test_sanitize_string_escapes_xss(self):
        malicious = "<script>alert('xss')</script>"
        cleaned = sanitize_string(malicious)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("&lt;script&gt;", cleaned)

    def test_sanitize_string_trims_length(self):
        long_str = "a" * 300
        cleaned = sanitize_string(long_str, max_length=50)
        self.assertEqual(len(cleaned), 50)

    def test_validate_aqi_boundaries(self):
        self.assertEqual(validate_aqi(-10), 0)
        self.assertEqual(validate_aqi(250), 250)
        self.assertEqual(validate_aqi(1500), 1000)
        self.assertEqual(validate_aqi("invalid", default=150), 150)

    def test_validate_pm25_boundaries(self):
        self.assertEqual(validate_pm25(-5.0), 0.0)
        self.assertEqual(validate_pm25(120.456), 120.46)
        self.assertEqual(validate_pm25(2000.0), 1500.0)
        self.assertEqual(validate_pm25("not_a_num", default=40.0), 40.0)

    def test_validate_choice_allowlist(self):
        allowed = ["moderate", "poor", "severe"]
        self.assertEqual(validate_choice("Severe", allowed, "moderate"), "severe")
        self.assertEqual(validate_choice("hacked_choice", allowed, "moderate"), "moderate")

    def test_sanitize_household_payload(self):
        payload = {
            "location": "  Delhi<script> ",
            "aqi_input_type": "invalid_type",
            "preset_severity": "Severe",
            "custom_aqi": "450",
            "commute_mode": "car_alone",
            "vulnerable_members": ["children", "asthma", "fake_vulnerability"]
        }
        clean = sanitize_household_payload(payload)
        self.assertIn("Delhi", clean["location"])
        self.assertNotIn("<script>", clean["location"])
        self.assertEqual(clean["aqi_input_type"], "preset") # fell back to default
        self.assertEqual(clean["preset_severity"], "Severe")
        self.assertEqual(clean["custom_aqi"], 450)
        self.assertEqual(clean["commute_mode"], "car_alone")
        self.assertEqual(clean["vulnerable_members"], ["children", "asthma"]) # excluded fake

if __name__ == "__main__":
    unittest.main()
