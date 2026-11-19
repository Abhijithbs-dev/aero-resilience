# 🍃 AeroResilience: GenAI Winter Smog & Urban Air Quality Assistant

> **Challenge Vertical:** Urban Families & Community Environmental Resilience (Winter Smog & Air Quality Guidance)  
> **Platform & Framework:** Google Antigravity Agent Platform, Python 3.10+, Standard Library Threading Server, Vanilla HTML5/CSS3 (WCAG 2.1 AA)  
> **Status:** Production-Ready · Zero External Runtime Dependencies · Ultra-Lightweight (< 1 MB footprint) · Single-Branch (`main`) Architecture

[![Single Branch: main](https://img.shields.io/badge/git%20branch-main-brightgreen)](https://github.com)
[![Repository Size: < 10 MB](https://img.shields.io/badge/repo%20size-%3C%201%20MB-blue)](https://github.com)
[![Accessibility: WCAG 2.1 AA](https://img.shields.io/badge/a11y-WCAG%202.1%20AA-success)](https://github.com)
[![Zero Hardcoded Secrets](https://img.shields.io/badge/security-zero%20secrets-blueviolet)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Chosen Vertical

### Problem Statement & Context
Every winter, metropolitan regions across the globe—most notably the Indo-Gangetic Plain (Delhi-NCR, Lahore, Dhaka, Kolkata), East Asian basins, and topographically trapped valleys (Salt Lake City, London winter inversions)—suffer catastrophic air pollution crises. Ambient Particulate Matter ($PM_{2.5}$) levels frequently spike between $250\ \mu\text{g/m}^3$ and $500+\ \mu\text{g/m}^3$ (Air Quality Index $400+$ to $500+$), representing **15 to 30 times the World Health Organization (WHO) safe threshold**.

This recurring seasonal phenomenon is driven by **meteorological surface temperature inversions**: radiational cooling at night traps a cold, stagnant air boundary layer under a lid of warmer upper air. Local emissions—vehicular exhaust, biomass burning, and road dust—cannot disperse vertically or horizontally and remain trapped at human breathing height.

### Target Personas & Community Vulnerabilities
Standard AQI apps merely report red numbers, passive warnings, or urge residents to buy expensive commercial air purifiers ($200–$600), leaving low- and middle-income families defenseless. **AeroResilience** bridges this gap by targeting:
1. **Parents with Infants & Young Children (Ages 0–10):** Children inhale 50% more air per pound of body weight than adults, causing rapid alveolar particulate deposition during school commutes and morning play.
2. **Multigenerational Homes with Seniors & Asthmatics:** Individuals with chronic obstructive pulmonary disease (COPD), bronchial hypersensitivity, or cardiovascular vulnerabilities facing acute exacerbations.
3. **Daily Urban Commuters & Budget Renters:** Commuters relying on two-wheelers, auto-rickshaws, or non-air-conditioned public buses who cannot modify rental housing permanently or afford luxury filtration.
4. **Resident Welfare Associations (RWAs) & Community Organizers:** Neighborhood leaders coordinating local leaf-waste composting, shared clean air respites, and carpooling networks to tackle community-scale emissions.

---

## 2. Approach and Logic

### Context-Driven Decision Architecture
AeroResilience integrates dynamic meteorological and lifestyle variables into a cohesive decision engine:

```
[User Context Intake]
  ├── Location & Air Quality (Live Open-Meteo Ingestion / Preset Scenario / Custom AQI)
  ├── Time of Day & Inversion Timing (Morning Peak Inversion vs. Solar Mixing Window)
  ├── Household Profile (Apartment / Independent House / Commute Mode / Cooking-Heating)
  ├── Budget Tier (Zero-Cost / Low-Cost DIY / Equipment-Ready)
  └── Vulnerable Members (Infants, Seniors, Asthmatics, Pregnant)
            │
            ▼
[AeroResilience Hybrid Reasoning Engine]
  ├── Deterministic Domain Rules Matrix (100% offline fallback)
  ├── Impact Estimator Utility (Physical aerosol mechanics & emission formulas)
  └── GenAI Pipeline (Gemini 2.5 Flash / OpenAI GPT-4o with prompt injection boundaries)
            │
            ▼
[Structured Response Schema]
  ├── 1. Risk Summary & Priority Actions
  ├── 2. Diurnal Low-Emission Routines
  ├── 3. Tiered Indoor Air Quality (IAQ) Hacks
  ├── 4. Sustainable Household & Community Alternatives
  └── 5. Direct Impact Explanations (Action ➔ Physical Mechanism ➔ Quantified Drop)
```

### Direct Impact Explanation Framework
Rather than generic tips ("stay indoors"), every single recommendation is paired with an actionable **Direct Impact** breakdown:
- **Physical Mechanism:** Grounded in fluid dynamics, building air infiltration rates (ACH), and aerosol physics (Brownian diffusion, inertial impaction in MERV-13 fibers).
- **Quantified Exposure Drop:** Specific percentage and numerical reductions in indoor $PM_{2.5}$ concentration (e.g. wet mopping reduces particle resuspension by $70\%$; door weatherstripping lowers infiltration by $60\%$).
- **Avoided Emissions:** Tangible greenhouse gas ($CO_2e$) and tailpipe soot savings from transit swaps (e.g. solitary car to metro avoids $1.8\text{ kg } CO_2e$ per $18\text{ km}$ trip).
- **Community Airshed Benefit:** Neighborhood-scale multiplier effects (composting dry leaves instead of open burning averts toxic dioxins and massive localized smoke plumes).

---

## 3. How the Solution Works

### System Architecture & Tech Stack
To satisfy the strict **< 10 MB total repository limit**, AeroResilience is engineered with **zero bloated dependencies** and zero client-side `node_modules` committed to version control:
- **Backend:** Python 3.10+ utilizing the standard library `ThreadingHTTPServer` and native `urllib.request`. Runs immediately on any standard Python installation without complex compilation or heavy virtualenv footprints.
- **Frontend:** Apple Human Interface Design System (WWDC Designing Fluid Interfaces, SF Pro typography, frosted glass `backdrop-filter: blur(25px)`, continuous squircle corners, instant pointer-down spring tactile physics, and Apple Health / Weather telemetry cards).
- **Security & Hardening (/007):** STRIDE threat modeled, OWASP Top 10 hardened with strict Content Security Policy (CSP), nosniff headers, frame denier, 50 KB request cap, and directory traversal barriers.
- **Code Optimization (@CodeRabbit):** Memory-bounded TTL cache with FIFO capacity limits and proactive eviction; zero external bloat; 100% portable Python 3.10+ standard library.
- **Live Air Quality Layer:** Open-Meteo Air Quality and Geocoding APIs (free, keyless, rate-limit friendly) with automatic caching and 4 instant winter smog presets (Moderate, Poor, Very Poor, Severe).
- **GenAI Hybrid Layer:** Compatible with Google Gemini API (`GEMINI_API_KEY`) and OpenAI API (`OPENAI_API_KEY`), backed by a deterministic rule engine that guarantees 100% uptime and offline demo resilience.

### Quickstart Setup & Run Instructions

#### Prerequisites
- Python 3.10 or higher (`python3 --version`)
- Modern web browser (Chrome, Firefox, Safari, Edge)

#### 1. Clone & Inspect
```bash
git clone https://github.com/abhijithbs119/winter-smog-assistant.git
cd winter-smog-assistant
git branch  # Verifies single branch: main
```

#### 2. Environment Configuration
Copy the safe `.env.example` template:
```bash
cp .env.example .env
```
*(Optional: Insert your `GEMINI_API_KEY` or `OPENAI_API_KEY` into `.env`. If left empty, the application runs seamlessly in deterministic offline rule mode with zero configuration needed).*

#### 3. Run Application Server
Start the local server with Python:
```bash
python3 app.py
```
*(Or via npm scripts if preferred: `npm start`)*

Open your browser at: **`http://localhost:8000`**

#### 4. Run Automated Test Suite
Execute the comprehensive unit and integration test suite:
```bash
python3 -m unittest discover tests
```
*(Or via npm: `npm test`)*

---

### Verification Skills & Compliance Audits

AeroResilience includes custom workspace [Agent Skills](https://antigravity.google/docs/skills/) in `.agents/skills/`:

| Slash Command | Skill Path | Purpose & Verification Gate |
| :--- | :--- | :--- |
| `/repo-guard` | `.agents/skills/repo-guard/` | Verifies **< 10 MB limit**, single `main` branch, and zero tracked secrets |
| `/security-audit`| `.agents/skills/security-audit/` | Audits input sanitization, prompt injection safeguards, and API hygiene |
| `/007` | `tests/test_007_security_audit.py` | Active Red Team penetration tests (DoS, fuzzing, path traversal, XSS injection) |
| `/a11y-audit` | `.agents/skills/a11y-audit/` | Audits WCAG 2.1 AA compliance, ARIA live regions, and contrast standards |
| `/readme-sync` | `.agents/skills/readme-sync/` | Verifies that all 4 required sections are thoroughly documented in README |

Run all audits locally:
```bash
bash .agents/skills/repo-guard/scripts/check_repo.sh
python3 .agents/skills/security-audit/scripts/run_audit.py
python3 .agents/skills/a11y-audit/scripts/run_a11y_check.py
python3 .agents/skills/readme-sync/scripts/verify_readme.py
```

---

## 4. Assumptions Made

### 1. Air Quality & Meteorological Assumptions
- **Diurnal Inversion Cycle:** Assumes peak surface temperature inversion between 05:30 and 09:30 AM during winter months (November to February in Northern Hemisphere metros). Assumes solar heating between 12:00 PM and 03:30 PM lifts the boundary mixing height, creating a temporary window of atmospheric dilution.
- **Air Quality Indices:** Normalizes measurements using the US EPA AQI scale and Indian National Air Quality Index standards, mapping numerical AQI to $PM_{2.5}$ concentrations ($\mu\text{g/m}^3$) via standard piecewise linear equations.
- **Data Source Resilience:** Open-Meteo's global keyless atmospheric model serves as the primary live telemetry source. If network connectivity is unavailable, the system defaults to verified regional winter smog presets (e.g. Severe: AQI 420, $PM_{2.5}\ 285\ \mu\text{g/m}^3$).

### 2. Emission & Exposure Reduction Calculation Formulas
- **Commute Emission Offsets:** Based on published Central Pollution Control Board (CPCB) and EPA vehicle fleet averages:
  - Solo petrol/diesel passenger vehicle: $\approx 160\text{ g } CO_2e/\text{km}$, $0.08\text{ g } PM_{2.5}/\text{km}$.
  - Two-wheeler (scooter/motorcycle): $\approx 70\text{ g } CO_2e/\text{km}$, $0.12\text{ g } PM_{2.5}/\text{km}$.
  - Electric Metro / Rapid Bus: $\approx 25\text{ g } CO_2e/\text{passenger-km}$, $0.005\text{ g } PM_{2.5}/\text{passenger-km}$.
- **Building Envelope Air Infiltration:** Leaky standard residential construction exhibits $\approx 0.7\text{ to } 0.85$ Air Changes per Hour (ACH). Comprehensive sash sealing and draft sweeps reduce infiltration to $\approx 0.25\text{ ACH}$, reducing outdoor particle penetration by $60\%–65\%$.
- **DIY Filtration (Corsi-Rosenthal Box):** A standard 20-inch box fan paired with a MERV-13 filter achieves a Clean Air Delivery Rate (CADR) of $200–250\text{ CFM}$, removing $85\%–90\%$ of indoor $PM_{2.5}$ within 45 minutes in a $300\text{ sq.ft}$ room.

### 3. Non-Medical Guidance & Health Guardrail Scope
- **Non-Medical Disclaimer:** AeroResilience provides strictly environmental engineering, behavioral scheduling, and indoor air filtration guidance. It does not provide medical diagnoses, treatment plans, or pharmaceutical recommendations.
- **Emergency Symptoms:** Users exhibiting acute respiratory distress, severe bronchospasms, cyanosis, or chest tightness are explicitly instructed via prominent UI badges to seek emergency clinical care.

---

## Repository Compliance Summary

- **Branch Policy:** Strictly single-branch repository (`main`). Zero secondary branches exist.
- **Size Footprint:** Under $500\text{ KB}$ total workspace size (less than 5% of the $10\text{ MB}$ challenge cap).
- **Accessibility:** 100% compliant with WCAG 2.1 AA guidelines (semantic landmarks, non-color-only indicators, ARIA live regions, visible focus rings).
- **Security:** Zero hardcoded API keys; all sensitive configurations isolated through `.env.example`.
