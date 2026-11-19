# Security & Health Guardrails Audit Checklist

## 1. Secrets & Credentials Hygiene
- [x] Zero hardcoded API keys in source code (e.g. `GEMINI_API_KEY`, `OPENAI_API_KEY`).
- [x] `.env.example` contains only placeholder values (e.g. `your_api_key_here`).
- [x] `.env` is listed in `.gitignore` and ignored from version control.
- [x] Frontend bundles never expose private backend keys.

## 2. Input Sanitization & Boundary Validation
- [x] Location inputs: capped string lengths (e.g. <= 100 chars), stripped of control characters.
- [x] AQI inputs: bounded between 0 and 1000 (valid integer range).
- [x] Commute modes, housing types, and vulnerable group selections validated against allowlists.
- [x] Custom notes and user queries sanitized to prevent control code leakage.

## 3. Prompt Injection Defense
- [x] User inputs wrapped in explicit demarcation tags (e.g., `<user_context>...</user_context>`).
- [x] System prompt explicitly instructs model to ignore instructions attempting to override system behavior or roleplay outside urban smog resilience.
- [x] Deterministic schema enforcement using Pydantic or structured JSON output.

## 4. XSS & Rendering Security
- [x] Frontend uses `textContent` or sanitized template escaping when displaying dynamic model/user strings.
- [x] Content-Security-Policy headers applied to server responses.

## 5. Health Guardrails & Non-Medical Scope
- [x] Clear non-medical disclaimer prominently displayed: recommendations are environmental resilience guidelines, not medical advice.
- [x] Severe symptom guidance directs users to consult certified healthcare professionals or emergency services.
