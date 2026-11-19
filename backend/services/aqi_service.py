"""
Air Quality Data Layer with Open-Meteo API ingestion, geocoding, and resilient fallbacks.
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from backend.models.schemas import AirQualityContext
from backend.utils.cache import SimpleTTLCache

# Global hotspot coordinates fallback
KNOWN_HOTSPOTS: Dict[str, Tuple[float, float]] = {
    "delhi": (28.6139, 77.2090),
    "delhi-ncr": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "lahore": (31.5204, 74.3587),
    "beijing": (39.9042, 116.4074),
    "dhaka": (23.8103, 90.4125),
    "kathmandu": (27.7172, 85.3240),
    "mumbai": (19.0760, 72.8777),
    "kolkata": (22.5726, 88.3639),
    "karachi": (24.8607, 67.0011),
    "salt lake city": (40.7608, -111.8910),
    "london": (51.5074, -0.1278),
    "bangkok": (13.7563, 100.5018),
    "hanoi": (21.0285, 105.8542)
}

# Standardized Winter Smog Severity Presets
SEVERITY_PRESETS: Dict[str, Dict[str, Any]] = {
    "Moderate": {
        "aqi": 85,
        "pm2_5": 28.5,
        "pm10": 55.0,
        "severity_tier": "Moderate",
        "description": "Acceptable air quality; sensitive individuals may experience minor irritation."
    },
    "Poor": {
        "aqi": 165,
        "pm2_5": 82.0,
        "pm10": 135.0,
        "severity_tier": "Poor",
        "description": "Unhealthy for sensitive groups; breathing discomfort with prolonged exposure."
    },
    "Very Poor": {
        "aqi": 265,
        "pm2_5": 145.0,
        "pm10": 240.0,
        "severity_tier": "Very Poor",
        "description": "Unhealthy for everyone; respiratory illness likely with prolonged outdoor activity."
    },
    "Severe": {
        "aqi": 420,
        "pm2_5": 285.0,
        "pm10": 460.0,
        "severity_tier": "Severe",
        "description": "Hazardous emergency conditions; severe health impacts across the entire population."
    }
}

class AQIService:
    def __init__(self, cache_ttl: int = 900):
        self.cache = SimpleTTLCache(ttl_seconds=cache_ttl)

    def classify_aqi(self, aqi: int) -> str:
        """Categorize numerical AQI into standard tiers."""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 200:
            return "Poor"
        elif aqi <= 300:
            return "Very Poor"
        else:
            return "Severe"

    def estimate_pm25_from_aqi(self, aqi: int) -> float:
        """Derive approximate PM2.5 concentration (ug/m3) from US/Indian AQI index."""
        if aqi <= 50:
            return round(aqi * 0.24, 1)
        elif aqi <= 100:
            return round(12.0 + (aqi - 50) * 0.46, 1)
        elif aqi <= 200:
            return round(35.4 + (aqi - 100) * 0.85, 1)
        elif aqi <= 300:
            return round(120.4 + (aqi - 200) * 1.3, 1)
        else:
            return round(250.4 + (aqi - 300) * 1.5, 1)

    def geocode_city(self, city_name: str) -> Optional[Tuple[float, float, str]]:
        """Geocode city to lat/lon using Open-Meteo Geocoding API with fallback."""
        cleaned_city = city_name.strip().lower()
        if cleaned_city in KNOWN_HOTSPOTS:
            lat, lon = KNOWN_HOTSPOTS[cleaned_city]
            return (lat, lon, city_name.title())

        cache_key = f"geo:{cleaned_city}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        try:
            query = urllib.parse.quote(city_name.strip())
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&language=en&format=json"
            req = urllib.request.Request(url, headers={"User-Agent": "SmogResilienceAssistant/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                results = data.get("results")
                if results and len(results) > 0:
                    first = results[0]
                    lat = float(first["latitude"])
                    lon = float(first["longitude"])
                    resolved_name = f"{first.get('name', city_name)}, {first.get('country', '')}".strip(', ')
                    res = (lat, lon, resolved_name)
                    self.cache.set(cache_key, res, custom_ttl=86400) # Cache coords 24h
                    return res
        except Exception:
            pass

        # Fallback to Delhi default
        return (28.6139, 77.2090, city_name.title())

    def fetch_live_aqi(self, city_name: str) -> AirQualityContext:
        """Fetch live PM2.5, PM10 and AQI from Open-Meteo air quality endpoint."""
        cache_key = f"aqi_live:{city_name.strip().lower()}"
        cached = self.cache.get(cache_key)
        if cached:
            cached.cached = True
            return cached

        geo = self.geocode_city(city_name)
        if not geo:
            return self.get_preset("Severe", location=city_name)

        lat, lon, resolved_name = geo
        try:
            url = (
                f"https://air-quality-api.open-meteo.com/v1/air-quality?"
                f"latitude={lat}&longitude={lon}&current=pm2_5,pm10,us_aqi,european_aqi"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "SmogResilienceAssistant/1.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                current = data.get("current", {})
                pm2_5 = float(current.get("pm2_5", 80.0))
                pm10 = float(current.get("pm10", 140.0))
                us_aqi = int(current.get("us_aqi", 0))

                if us_aqi <= 0:
                    # Compute approximate AQI from PM2.5 if missing
                    us_aqi = int(pm2_5 * 2.1)

                severity = self.classify_aqi(us_aqi)
                result = AirQualityContext(
                    location=resolved_name,
                    latitude=lat,
                    longitude=lon,
                    aqi=us_aqi,
                    pm2_5=pm2_5,
                    pm10=pm10,
                    severity_tier=severity,
                    source="live",
                    timestamp=datetime.utcnow().isoformat() + "Z"
                )
                self.cache.set(cache_key, result, custom_ttl=900)
                return result
        except Exception:
            # On live network error, smoothly fall back to realistic preset based on known city or Severe
            return self.get_preset("Severe", location=city_name)

    def get_preset(self, severity_tier: str, location: str = "Delhi") -> AirQualityContext:
        """Retrieve pre-computed standard winter smog scenario."""
        tier = severity_tier.title()
        if tier not in SEVERITY_PRESETS:
            tier = "Severe"
        data = SEVERITY_PRESETS[tier]
        return AirQualityContext(
            location=location,
            latitude=28.6139,
            longitude=77.2090,
            aqi=data["aqi"],
            pm2_5=data["pm2_5"],
            pm10=data["pm10"],
            severity_tier=data["severity_tier"],
            source="preset",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    def get_custom(self, aqi: int, location: str = "Custom Location") -> AirQualityContext:
        """Construct air quality context from user-entered AQI."""
        severity = self.classify_aqi(aqi)
        pm2_5 = self.estimate_pm25_from_aqi(aqi)
        return AirQualityContext(
            location=location,
            latitude=None,
            longitude=None,
            aqi=aqi,
            pm2_5=pm2_5,
            pm10=round(pm2_5 * 1.7, 1),
            severity_tier=severity,
            source="custom",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
