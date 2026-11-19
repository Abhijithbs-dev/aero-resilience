# Antigravity Always-On Project Guardrails & Instructions

## 1. Non-Negotiable Challenge Constraints
- **Single Branch Rule:** All commits, development, and tags must exist exclusively on the `main` branch. Never create or push secondary branches (e.g. `feature/*`, `dev`, `test`).
- **Repository Size Limit:** Total repository footprint must stay **strictly under 10 MB**. Never track `node_modules/`, `.venv/`, `venv/`, `__pycache__/`, large datasets, or binary assets.
- **Zero Secrets Policy:** Never commit secrets, tokens, private keys, or `.env` files. Always use `.env.example` with safe placeholder strings and load secrets from process environment variables.
- **Attempt Cap Awareness:** Maximum 3 submission attempts—always run all verification skills (`/repo-guard`, `/security-audit`, `/a11y-audit`, `/readme-sync`) prior to any submission push.

## 2. Chosen Vertical & Core Mission
- **Vertical:** Urban Families & Community Environmental Resilience (Winter Smog & Air Quality Guidance).
- **Core Mission:** Deliver tailored, actionable, and science-grounded recommendations for families and urban communities during peak winter smog episodes:
  1. **Low-Emission Daily Routines:** Smart scheduling for outdoor chores, transit/carpool swaps, school-run adjustments, and low-smoke cooking/heating.
  2. **Indoor Air Quality (IAQ) Hacks:** Tiered interventions (Free: wet mopping, cross-ventilation timing; Low-cost: door/window draft sweeps, DIY Corsi-Rosenthal box fans; Equipment: HEPA placement).
  3. **Sustainable Alternatives:** Household and community-scale substitutions (active travel, clean fuels, dry-leaf composting over open burning).
  4. **Direct Impact Explanations:** Clear, transparent explanation of *why* each action matters, quantifying mechanism, exposure reduction, and community emissions avoided.

## 3. Architecture & Code Quality Principles
- **Lightweight, Zero-Bloat Stack:** Built with Python (FastAPI/Uvicorn) backend and clean semantic HTML5 / Modern CSS / Vanilla JS frontend. No heavy client-side node_modules checked into repository.
- **Hybrid AI Architecture:** Dynamic GenAI reasoning with structured JSON output, backed by deterministic fallback rules and offline simulation mode so the assistant works seamlessly even without an external API key or internet connection.
- **Strict Input Validation & Security:** Sanitize and bounds-check all user inputs. Defend against prompt-injection attacks. Escape all user-provided outputs to prevent XSS.
- **Health & Safety Guardrails:** Clear non-medical disclaimer displayed on UI and backend responses. Never prescribe pharmaceutical or medical treatment.
- **Accessibility Standard:** Strictly adhere to WCAG 2.1 AA standards: semantic landmarks, visible focus rings, ARIA live regions for AI responses, and multi-modal cues (text labels + icons + colors) for AQI severity tiers.

## 4. Verification Skills
- `/repo-guard` → Enforce < 10 MB, single branch, no secrets.
- `/security-audit` → Audit input sanitization, prompt injection safeguards, and API credential hygiene.
- `/a11y-audit` → Verify WCAG 2.1 AA compliance, ARIA attributes, and keyboard navigability.
- `/readme-sync` → Ensure comprehensive documentation across vertical, architecture, setup, and assumptions.
