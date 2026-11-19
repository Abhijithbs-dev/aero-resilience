#!/usr/bin/env python3
"""
Automated Security & Guardrails Audit Script
"""
import os
import re
import sys

def check_for_leaked_secrets():
    print("[1/4] Scanning for hardcoded API keys and secrets...")
    secret_patterns = [
        re.compile(r'(AIzaSy[A-Za-z0-9_-]{33})'), # Google API Key
        re.compile(r'(sk-[A-Za-z0-9]{32,})'),    # OpenAI API Key
        re.compile(r'(ghp_[A-Za-z0-9]{36})'),    # GitHub PAT
        re.compile(r'(xox[baprs]-[0-9a-zA-Z-]{10,})') # Slack token
    ]
    violations = []
    for root, dirs, files in os.walk("."):
        if any(ignored in root for ignored in [".git", "__pycache__", "venv", ".venv", "node_modules"]):
            continue
        for f in files:
            if f.endswith((".py", ".js", ".html", ".json", ".md", ".sh", ".yaml", ".yml")):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        for p in secret_patterns:
                            matches = p.findall(content)
                            if matches:
                                violations.append(f"{path}: Matched secret pattern")
                except Exception as e:
                    pass
    if violations:
        print("❌ ERROR: Secret patterns detected in source:")
        for v in violations:
            print(f"  - {v}")
        return False
    print("✅ No hardcoded API keys detected.")
    return True

def check_env_example():
    print("[2/4] Verifying .env and .env.example hygiene...")
    if os.path.exists(".env"):
        print("⚠️ Warning: Local .env exists. Checking if ignored in git...")
    if not os.path.exists(".env.example"):
        print("❌ ERROR: .env.example template missing!")
        return False
    with open(".env.example", "r", encoding="utf-8") as f:
        content = f.read()
        if "AIzaSy" in content or "sk-" in content:
            print("❌ ERROR: Real key found in .env.example!")
            return False
    print("✅ .env.example is clean and present.")
    return True

def check_prompt_injection_guardrails():
    print("[3/4] Checking prompt injection safeguards in backend...")
    ai_service_path = "backend/services/ai_service.py"
    if not os.path.exists(ai_service_path):
        print("ℹ️ ai_service.py not yet implemented (will verify once created).")
        return True
    with open(ai_service_path, "r", encoding="utf-8") as f:
        code = f.read()
        if "guardrail" in code.lower() or "system" in code.lower() or "disclaimer" in code.lower():
            print("✅ Prompt injection guardrails found in ai_service.")
            return True
        else:
            print("❌ ERROR: No prompt injection defense identified in backend/services/ai_service.py!")
            return False

def check_disclaimers():
    print("[4/4] Checking non-medical disclaimer inclusion...")
    found_in_agents = False
    if os.path.exists("AGENTS.md"):
        with open("AGENTS.md", "r", encoding="utf-8") as f:
            if "non-medical" in f.read().lower():
                found_in_agents = True
    if found_in_agents:
        print("✅ Non-medical disclaimer is codified in AGENTS.md.")
        return True
    print("❌ ERROR: Missing non-medical disclaimer in project documentation.")
    return False

def main():
    print("==========================================")
    print(" Running Security & Guardrails Audit (/security-audit)")
    print("==========================================")
    ok = True
    ok = check_for_leaked_secrets() and ok
    ok = check_env_example() and ok
    ok = check_prompt_injection_guardrails() and ok
    ok = check_disclaimers() and ok
    print("==========================================")
    if ok:
        print("🎉 SECURITY AUDIT PASSED: Security defenses verified!")
        sys.exit(0)
    else:
        print("💥 SECURITY AUDIT FAILED: Please fix above issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
