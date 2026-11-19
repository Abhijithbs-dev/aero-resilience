"""
Fast, multi-threaded HTTP server and REST API for Winter Smog & Urban Air Quality Assistant.
Built using standard library ThreadingHTTPServer for zero-dependency, ultra-lightweight execution.
Hardened with STRIDE threat modeling, OWASP Top 10 defenses, and Content Security Policy.
"""
import json
import os
import sys
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

from backend.models.schemas import HouseholdProfile
from backend.services.aqi_service import AQIService, SEVERITY_PRESETS
from backend.services.ai_service import AIService
from backend.utils.sanitization import sanitize_household_payload, sanitize_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.realpath(os.path.join(BASE_DIR, "frontend"))

aqi_service = AQIService()
ai_service = AIService()

class SmogAssistantRequestHandler(BaseHTTPRequestHandler):
    server_version = "SmogResilienceServer/1.0"

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        # Security hardening headers
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://geocoding-api.open-meteo.com https://air-quality-api.open-meteo.com;")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Health check
        if path == "/api/health":
            self._set_headers(200)
            payload = {
                "status": "healthy",
                "service": "GenAI Winter Smog & Urban Air Quality Assistant",
                "version": "1.0.0",
                "engine": "hybrid_genai_rules",
                "has_gemini": bool(ai_service.gemini_key and ai_service.gemini_key != "your_gemini_api_key_here"),
                "has_openai": bool(ai_service.openai_key and ai_service.openai_key != "your_openai_api_key_here")
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        # 2. Presets endpoint
        if path == "/api/presets":
            self._set_headers(200)
            self.wfile.write(json.dumps(SEVERITY_PRESETS).encode("utf-8"))
            return

        # 3. Live AQI lookup
        if path == "/api/aqi":
            city = query.get("city", ["Delhi"])[0]
            sanitized_city = sanitize_string(city, max_length=60) or "Delhi"
            aqi_ctx = aqi_service.fetch_live_aqi(sanitized_city)
            self._set_headers(200)
            self.wfile.write(json.dumps(aqi_ctx.to_dict()).encode("utf-8"))
            return

        # 4. Static Frontend file serving
        self._serve_static(path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/recommendations":
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 50000:  # 50 KB payload cap
                self._set_headers(413)
                self.wfile.write(json.dumps({"error": "Payload too large. Maximum size is 50 KB."}).encode("utf-8"))
                return

            body = self.rfile.read(content_length).decode("utf-8")
            try:
                raw_payload = json.loads(body) if body else {}
            except Exception:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode("utf-8"))
                return

            # Sanitize & validate inputs
            clean = sanitize_household_payload(raw_payload)

            # Determine AQI Context
            if clean["aqi_input_type"] == "live":
                aqi_ctx = aqi_service.fetch_live_aqi(clean["location"])
            elif clean["aqi_input_type"] == "custom":
                aqi_ctx = aqi_service.get_custom(clean["custom_aqi"], location=clean["location"])
            else:
                aqi_ctx = aqi_service.get_preset(clean["preset_severity"], location=clean["location"])

            # Build Household Profile
            profile = HouseholdProfile(
                commute_mode=clean["commute_mode"],
                housing_type=clean["housing_type"],
                cooking_heating=clean["cooking_heating"],
                budget_tier=clean["budget_tier"],
                vulnerable_members=clean["vulnerable_members"],
                time_of_day=clean["time_of_day"]
            )

            # Generate Recommendations
            rec = ai_service.generate_recommendations(
                aqi_ctx=aqi_ctx,
                profile=profile,
                user_question=clean.get("user_question", "")
            )

            response_data = rec.to_dict()
            response_data["aqi_context"] = aqi_ctx.to_dict()

            self._set_headers(200)
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def _serve_static(self, path: str):
        # Whitelisted static assets with strict path traversal protection
        routes = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/index.html": ("index.html", "text/html; charset=utf-8"),
            "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "application/javascript; charset=utf-8"),
        }

        if path not in routes:
            self._set_headers(404, "text/plain")
            self.wfile.write(b"404 Not Found")
            return

        filename, content_type = routes[path]
        file_path = os.path.realpath(os.path.join(FRONTEND_DIR, filename))

        # Enforce canonical path is inside FRONTEND_DIR
        if not file_path.startswith(FRONTEND_DIR) or not os.path.isfile(file_path):
            self._set_headers(403, "text/plain")
            self.wfile.write(b"403 Forbidden")
            return

        with open(file_path, "rb") as f:
            data = f.read()

        self._set_headers(200, content_type=content_type)
        self.wfile.write(data)

def run_server(host: str = "0.0.0.0", port: int = 8000):
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, SmogAssistantRequestHandler)
    print(f"🚀 GenAI Winter Smog Assistant server running at http://{host}:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server cleanly...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    run_server(host=host, port=port)
