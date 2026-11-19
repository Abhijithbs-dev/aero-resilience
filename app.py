#!/usr/bin/env python3
"""
Entrypoint for GenAI Winter Smog & Urban Air Quality Assistant.
Usage:
    python3 app.py
"""
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.server import run_server

def main():
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    run_server(host=host, port=port)

if __name__ == "__main__":
    main()
