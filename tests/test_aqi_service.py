"""
Unit tests for Air Quality Service, presets, and classification.
"""
import unittest
from backend.services.aqi_service import AQIService, SEVERITY_PRESETS

class TestAQIService(unittest.TestCase):
    def setUp(self):
        self.service = AQIService(cache_ttl=60)

    def test_classify_aqi_tiers(self):
        self.assertEqual(self.service.classify_aqi(30), "Good")
        self.assertEqual(self.service.classify_aqi(85), "Moderate")
        self.assertEqual(self.service.classify_aqi(165), "Poor")
        self.assertEqual(self.service.classify_aqi(265), "Very Poor")
        self.assertEqual(self.service.classify_aqi(450), "Severe")

    def test_estimate_pm25_from_aqi(self):
        # Monotonically increasing check
        pm_good = self.service.estimate_pm25_from_aqi(40)
        pm_mod = self.service.estimate_pm25_from_aqi(80)
        pm_poor = self.service.estimate_pm25_from_aqi(150)
        pm_severe = self.service.estimate_pm25_from_aqi(400)
        self.assertTrue(pm_good < pm_mod < pm_poor < pm_severe)

    def test_get_preset_returns_expected_tier(self):
        ctx = self.service.get_preset("Severe", "Delhi")
        self.assertEqual(ctx.severity_tier, "Severe")
        self.assertEqual(ctx.aqi, 420)
        self.assertGreater(ctx.pm2_5, 200)

    def test_custom_aqi_generation(self):
        ctx = self.service.get_custom(350, "Custom Station")
        self.assertEqual(ctx.severity_tier, "Severe")
        self.assertEqual(ctx.aqi, 350)
        self.assertEqual(ctx.source, "custom")

    def test_geocoding_fallback_to_known_hotspot(self):
        geo = self.service.geocode_city("Delhi")
        self.assertIsNotNone(geo)
        lat, lon, name = geo
        self.assertAlmostEqual(lat, 28.6139, places=2)

if __name__ == "__main__":
    unittest.main()
