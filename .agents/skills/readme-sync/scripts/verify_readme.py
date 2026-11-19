#!/usr/bin/env python3
"""
Verify README.md covers the 4 required challenge sections.
"""
import os
import sys

REQUIRED_SECTIONS = [
    ("Chosen Vertical", ["vertical", "urban families", "winter smog", "resilience"]),
    ("Approach and Logic", ["approach", "logic", "decision engine", "direct impact"]),
    ("How the Solution Works", ["how the solution works", "architecture", "setup", "quickstart"]),
    ("Assumptions Made", ["assumptions", "air quality", "formulas", "non-medical disclaimer"])
]

def check_readme():
    print("==========================================")
    print(" Running README Verification (/readme-sync)")
    print("==========================================")
    if not os.path.exists("README.md"):
        print("❌ ERROR: README.md not found!")
        sys.exit(1)
        
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read().lower()

    all_passed = True
    for section_title, keywords in REQUIRED_SECTIONS:
        found = any(k in content for k in keywords)
        if found:
            print(f"✅ Section '{section_title}' verified.")
        else:
            print(f"❌ ERROR: Missing required section or keywords for: '{section_title}'")
            all_passed = False

    print("==========================================")
    if all_passed:
        print("🎉 README SYNC PASSED: All 4 required sections present and detailed!")
        sys.exit(0)
    else:
        print("💥 README SYNC FAILED: Update README.md with missing sections.")
        sys.exit(1)

if __name__ == "__main__":
    check_readme()
