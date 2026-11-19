"""
Air Quality Data Layer with Open-Meteo API ingestion, geocoding, and resilient fallbacks.
Integrates live real-time air quality telemetry and live atmospheric meteorology.
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional, List
from backend.models.schemas import AirQualityContext
from backend.utils.cache import SimpleTTLCache

# Global hotspot coordinates and monitoring station registry
KNOWN_HOTSPOTS: Dict[str, Tuple[float, float]] = {
    # Delhi & Regional Monitoring Corridors
    "delhi": (28.6139, 77.2090),
    "delhi-ncr": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "anand vihar": (28.6502, 77.3027),
    "anand vihar, delhi": (28.6502, 77.3027),
    "jahangirpuri": (28.7328, 77.1706),
    "jahangirpuri, delhi": (28.7328, 77.1706),
    "wazirpur": (28.6998, 77.1654),
    "wazirpur, delhi": (28.6998, 77.1654),
    "rk puram": (28.5638, 77.1863),
    "rk puram, delhi": (28.5638, 77.1863),
    "igi airport": (28.5562, 77.1000),
    "igi airport (t3)": (28.5562, 77.1000),
    "igi airport (t3), delhi": (28.5562, 77.1000),
    "lodhi road": (28.5918, 77.2273),
    "lodhi road, delhi": (28.5918, 77.2273),
    "lodhi road (clean corridor)": (28.5918, 77.2273),
    # Indo-Gangetic Basin & Indian Metros
    "mumbai": (19.0760, 72.8777),
    "kolkata": (22.5726, 88.3639),
    "chennai": (13.0827, 80.2707),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "ahmedabad": (23.0225, 72.5714),
    "lucknow": (26.8467, 80.9462),
    "patna": (25.5941, 85.1376),
    "kanpur": (26.4499, 80.3319),
    "varanasi": (25.3176, 82.9739),
    "chandigarh": (30.7333, 76.7794),
    "jaipur": (26.9124, 75.7873),
    # Key Global Smog Metros
    "lahore": (31.5204, 74.3587),
    "dhaka": (23.8103, 90.4125),
    "beijing": (39.9042, 116.4074),
    "kathmandu": (27.7172, 85.3240),
    "karachi": (24.8607, 67.0011),
    "salt lake city": (40.7608, -111.8910),
    "london": (51.5074, -0.1278),
    "new york": (40.7128, -74.0060),
    "bangkok": (13.7563, 100.5018),
    "hanoi": (21.0285, 105.8542)
}

# Regional monitoring stations benchmarks
DEFAULT_HOTSPOTS = [
    {"station": "Anand Vihar, Delhi", "aqi": 488, "pm2_5": 340.2, "status": "Hazardous", "multiplier": "22.7x WHO"},
    {"station": "Jahangirpuri, Delhi", "aqi": 465, "pm2_5": 315.0, "status": "Hazardous", "multiplier": "21.0x WHO"},
    {"station": "Wazirpur, Delhi", "aqi": 452, "pm2_5": 298.5, "status": "Hazardous", "multiplier": "19.9x WHO"},
    {"station": "RK Puram, Delhi", "aqi": 418, "pm2_5": 272.0, "status": "Severe", "multiplier": "18.1x WHO"},
    {"station": "IGI Airport (T3), Delhi", "aqi": 376, "pm2_5": 242.0, "status": "Severe", "multiplier": "16.1x WHO"},
    {"station": "Lodhi Road (Clean Corridor)", "aqi": 295, "pm2_5": 168.0, "status": "Very Poor", "multiplier": "11.2x WHO"}
]

# Standardized Winter Smog Severity Presets with Distinct Seasonal Microclimates
SEVERITY_PRESETS: Dict[str, Dict[str, Any]] = {
    "Moderate": {
        "aqi": 85,
        "pm2_5": 28.5,
        "pm10": 55.0,
        "no2": 24.0,
        "so2": 8.0,
        "co": 0.6,
        "o3": 38.0,
        "temperature": 23.5,
        "humidity": 52,
        "wind_speed": 11.2,
        "severity_tier": "Moderate",
        "who_multiplier": 1.9,
        "cigarette_equiv": 1.3,
        "description": "Acceptable air quality; ventilated boundary layer with moderate breeze."
    },
    "Poor": {
        "aqi": 165,
        "pm2_5": 82.0,
        "pm10": 135.0,
        "no2": 48.0,
        "so2": 16.0,
        "co": 1.4,
        "o3": 30.0,
        "temperature": 20.0,
        "humidity": 68,
        "wind_speed": 6.8,
        "severity_tier": "Poor",
        "who_multiplier": 5.5,
        "cigarette_equiv": 3.7,
        "description": "Unhealthy for sensitive groups; moderate winter haze with declining wind speed."
    },
    "Very Poor": {
        "aqi": 265,
        "pm2_5": 145.0,
        "pm10": 240.0,
        "no2": 72.0,
        "so2": 28.0,
        "co": 2.6,
        "o3": 22.0,
        "temperature": 17.5,
        "humidity": 79,
        "wind_speed": 4.1,
        "severity_tier": "Very Poor",
        "who_multiplier": 9.7,
        "cigarette_equiv": 6.6,
        "description": "Unhealthy for entire population; pronounced boundary inversion trapping smoke."
    },
    "Severe": {
        "aqi": 420,
        "pm2_5": 285.0,
        "pm10": 460.0,
        "no2": 118.0,
        "so2": 45.0,
        "co": 4.8,
        "o3": 14.0,
        "temperature": 14.2,
        "humidity": 86,
        "wind_speed": 2.4,
        "severity_tier": "Severe",
        "who_multiplier": 19.0,
        "cigarette_equiv": 13.0,
        "description": "Hazardous emergency conditions; deep nocturnal inversion lid with calm winds."
    }
}

class AQIService:
    def __init__(self, cache_ttl: int = 900):
        self.cache = SimpleTTLCache(ttl_seconds=cache_ttl, max_size=1000)

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
        """Geocode city to lat/lon using local registry or Open-Meteo Geocoding API."""
        cleaned_city = city_name.strip().lower()
        if cleaned_city in KNOWN_HOTSPOTS:
            lat, lon = KNOWN_HOTSPOTS[cleaned_city]
            return (lat, lon, city_name.title())

        # Check prefix match for known stations (e.g., "Anand Vihar" in "Anand Vihar, Delhi")
        for k, coords in KNOWN_HOTSPOTS.items():
            if k in cleaned_city or cleaned_city in k:
                return (coords[0], coords[1], city_name.title())

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
        """
        Fetch authentic live PM2.5, PM10, pollutant concentrations AND live meteorological weather
        (temperature, relative humidity, wind speed) from Open-Meteo API.
        """
        cache_key = f"aqi_live:{city_name.strip().lower()}"
        cached = self.cache.get(cache_key)
        if cached:
            cached.cached = True
            return cached

        geo = self.geocode_city(city_name)
        if not geo:
            return self.get_preset("Severe", location=city_name)

        lat, lon, resolved_name = geo

        # Default microclimate in case of network issues
        temperature = 17.5
        humidity = 76
        wind_speed = 3.2

        # 1. Fetch live meteorological weather from Open-Meteo Forecast API
        try:
            w_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
            )
            req_w = urllib.request.Request(w_url, headers={"User-Agent": "SmogResilienceAssistant/1.0"})
            with urllib.request.urlopen(req_w, timeout=4) as resp_w:
                w_data = json.loads(resp_w.read().decode())
                current_w = w_data.get("current", {})
                if "temperature_2m" in current_w:
                    temperature = float(current_w["temperature_2m"])
                if "relative_humidity_2m" in current_w:
                    humidity = int(current_w["relative_humidity_2m"])
                if "wind_speed_10m" in current_w:
                    wind_speed = float(current_w["wind_speed_10m"])
        except Exception:
            pass

        # 2. Fetch live atmospheric pollutant telemetry from Open-Meteo Air Quality API
        try:
            aq_url = (
                f"https://air-quality-api.open-meteo.com/v1/air-quality?"
                f"latitude={lat}&longitude={lon}&current=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi,european_aqi"
            )
            req_aq = urllib.request.Request(aq_url, headers={"User-Agent": "SmogResilienceAssistant/1.0"})
            with urllib.request.urlopen(req_aq, timeout=4) as resp_aq:
                data = json.loads(resp_aq.read().decode())
                current = data.get("current", {})
                pm2_5 = float(current.get("pm2_5", 80.0))
                pm10 = float(current.get("pm10", 140.0))
                no2 = float(current.get("nitrogen_dioxide", 55.0))
                so2 = float(current.get("sulphur_dioxide", 22.0))
                raw_co = float(current.get("carbon_monoxide", 1200.0))
                co = round(raw_co / 1000.0, 2)  # Convert ug/m3 to mg/m3
                o3 = float(current.get("ozone", 25.0))
                us_aqi = int(current.get("us_aqi", 0))

                if us_aqi <= 0:
                    us_aqi = int(pm2_5 * 2.1)

                severity = self.classify_aqi(us_aqi)
                who_mult = round(pm2_5 / 15.0, 1)
                cigs = round(pm2_5 / 22.0, 1)

                result = AirQualityContext(
                    location=resolved_name,
                    latitude=lat,
                    longitude=lon,
                    aqi=us_aqi,
                    pm2_5=pm2_5,
                    pm10=pm10,
                    severity_tier=severity,
                    source="live",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    no2=no2,
                    so2=so2,
                    co=co,
                    o3=o3,
                    temperature=temperature,
                    humidity=humidity,
                    wind_speed=wind_speed,
                    who_multiplier=who_mult,
                    cigarette_equiv=cigs,
                    hotspots=DEFAULT_HOTSPOTS
                )
                self.cache.set(cache_key, result, custom_ttl=900)
                return result
        except Exception:
            # On live network error, fall back to realistic preset with dynamic location
            preset = self.get_preset("Severe", location=city_name)
            preset.temperature = temperature
            preset.humidity = humidity
            preset.wind_speed = wind_speed
            return preset

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
            timestamp=datetime.now(timezone.utc).isoformat(),
            no2=data.get("no2", 45.0),
            so2=data.get("so2", 18.0),
            co=data.get("co", 1.2),
            o3=data.get("o3", 28.0),
            temperature=data.get("temperature", 14.2),
            humidity=data.get("humidity", 86),
            wind_speed=data.get("wind_speed", 2.4),
            who_multiplier=data.get("who_multiplier", 19.0),
            cigarette_equiv=data.get("cigarette_equiv", 13.0),
            hotspots=DEFAULT_HOTSPOTS
        )

    def get_custom(self, custom_aqi: int, location: str = "Custom Assessment") -> AirQualityContext:
        """Construct air quality context from user-provided custom AQI value."""
        severity = self.classify_aqi(custom_aqi)
        pm2_5 = self.estimate_pm25_from_aqi(custom_aqi)
        pm10 = round(pm2_5 * 1.62, 1)
        who_mult = round(pm2_5 / 15.0, 1)
        cigs = round(pm2_5 / 22.0, 1)
        no2 = round(pm2_5 * 0.42, 1)
        so2 = round(pm2_5 * 0.16, 1)
        co = round(0.5 + (custom_aqi / 100.0) * 0.8, 1)
        o3 = round(max(8.0, 45.0 - (custom_aqi / 20.0)), 1)

        # Diurnal inversion correlation: higher AQI correlates with colder temperature, higher humidity, lower wind
        ratio = min(1.0, custom_aqi / 400.0)
        temp = round(24.0 - ratio * 10.0, 1)
        hum = round(50 + ratio * 38)
        wind = round(max(1.5, 10.0 - ratio * 8.0), 1)

        return AirQualityContext(
            location=location,
            latitude=28.6139,
            longitude=77.2090,
            aqi=custom_aqi,
            pm2_5=pm2_5,
            pm10=pm10,
            severity_tier=severity,
            source="custom",
            timestamp=datetime.now(timezone.utc).isoformat(),
            no2=no2,
            so2=so2,
            co=co,
            o3=o3,
            temperature=temp,
            humidity=hum,
            wind_speed=wind,
            who_multiplier=who_mult,
            cigarette_equiv=cigs,
            hotspots=DEFAULT_HOTSPOTS
        )
