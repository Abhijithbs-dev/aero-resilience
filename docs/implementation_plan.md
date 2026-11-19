# Implementation Plan: GenAI Winter Smog & Urban Air Quality Assistant

## 1. Executive Summary & Chosen Vertical
- **Vertical:** Urban Families & Community Environmental Resilience (Winter Smog & Air Quality Guidance)
- **Target Audience:** Families with children, elderly residents, asthmatic/respiratory-vulnerable individuals, daily urban commuters, and neighborhood community leaders in smog-impacted metros.
- **Core Value Proposition:** Move beyond passive AQI displays to actionable, context-driven behavioral routines, low-cost indoor air quality (IAQ) hacks, and community alternatives, with physical mechanism and impact quantification for every recommendation.

---

## 2. Architecture & Technology Stack

### Stack Components (Lightweight & < 10 MB Footprint):
1. **Backend Server:** Python 3.10+ with `FastAPI` and `uvicorn`. Standard library and lightweight dependencies (`pydantic`, `httpx`, `pytest`). Total installed dependencies take zero tracked repo bytes.
2. **Frontend UI:** Semantic HTML5, CSS3 with high-contrast tokens, and vanilla modern JavaScript. No build step or bloated dependencies required; runs instantly via FastAPI static file serving.
3. **Data Layer & Fallbacks:**
   - Free, keyless public air quality API (`Open-Meteo Air Quality API`) querying PM2.5, PM10, and European/US AQI indices.
   - Built-in offline severity presets (Moderate: AQI 80, Poor: AQI 160, Very Poor: AQI 260, Severe/Hazardous: AQI 420+) and custom manual input support.
   - Local in-memory caching to eliminate redundant API requests and respect rate limits.
4. **GenAI Layer:**
   - Multi-provider support: Google Gemini API, OpenAI API, and an offline deterministic rule-based inference engine.
   - Strict JSON Schema output enforcement with health guardrails and prompt-injection boundary tokens.

---

## 3. User Personas & Context Input Matrix

| Persona | Key Vulnerabilities / Constraints | Priority Focus Areas |
| :--- | :--- | :--- |
| **P1: Parent with Young Children (Ages 2-7)** | Developing lungs, high inhalation rate, school commutes | Morning inversion avoidance, sealable playroom, DIY air cleaners, school-run carpooling |
| **P2: Multigenerational Home with Senior / Asthmatic** | Bronchial hypersensitivity, high risk of exacerbation | 24/7 clean room creation, strict indoor emission elimination, wet cleaning protocols |
| **P3: Budget-Conscious Renter / Daily Commuter** | Cannot afford expensive HEPA purifiers, uses two-wheeler/bus | DIY Corsi-Rosenthal box, draft proofing with rolled towels, N95 route optimization |
| **P4: Community Organizer / Resident Welfare Rep** | Seeks neighborhood-scale reduction in emission triggers | Coordinated vehicle-pooling, prohibition of biomass/leaf burning, community clean rooms |

### Context Inputs Schema:
- `location`: City or neighborhood name (e.g. "Delhi", "Lahore", "Kathmandu").
- `aqi_input_type`: `"live"`, `"preset"`, or `"custom"`.
- `aqi_value`: Integer AQI / PM2.5 estimate.
- `time_of_day`: `"morning"` (peak inversion), `"afternoon"` (solar boundary layer lift), `"evening"`, `"night"`.
- `household_type`: `"apartment"`, `"independent_house"`, `"multistory_flat"`.
- `commute_mode`: `"two_wheeler"`, `"public_bus_metro"`, `"car_alone"`, `"carpool_walk"`.
- `cooking_heating`: `"lpg_gas"`, `"induction_electric"`, `"biomass_kerosene"`, `"wood_coal"`.
- `budget_tier`: `"free"`, `"low_cost"`, `"equipment_ready"`.
- `vulnerable_members`: List of flags (`has_infant`, `has_senior`, `has_asthma`, `pregnant`).

---

## 4. Logical Decision Engine & Impact Explanations

### 4.1 Low-Emission Daily Routines
1. **Diurnal Inversion Timing:** Winter meteorology traps particulate matter under surface temperature inversions between 05:00 and 09:30. Assistant reschedules outdoor physical activity and ventilation to 12:00–16:00 when the atmospheric boundary layer expands.
2. **School-Run & Commute Shifts:** Convert solitary idling vehicular runs to clustered neighborhood carpooling or public rapid transit.
3. **Indoor Emission Avoidance:** Eliminates incense, mosquito coils (which emit PM2.5 equivalent to 75–100 cigarettes), unvented kerosene heaters, and high-smoke frying.

### 4.2 Tiered Indoor Air Quality (IAQ) Hacks
1. **Tier 1 (Zero Cost / Free):**
   - *Micro-ventilation timing:* Seal during temperature inversions; open high-level windows briefly at midday if outdoor PM2.5 drops.
   - *Damp cleaning:* Wet mopping instead of dry broom sweeping prevents particulate re-suspension by 60–80%.
   - *Dedicated Clean Room:* Select a central interior room with minimal exterior walls and seal doors with damp rolled towels.
2. **Tier 2 (Low Cost / < $15):**
   - *DIY Weatherstripping:* Foam draft tape around window sashes and door sweeps.
   - *DIY Corsi-Rosenthal Box:* Standard 20-inch box fan paired with MERV-13 furnace filter (delivers CADR comparable to $300 commercial HEPA units at 15% of the cost).
3. **Tier 3 (Equipment / Medium Cost):**
   - Strategic HEPA air purifier placement away from corners and drafts, run continuously on medium fan speed rather than short bursts on high.

### 4.3 Sustainable Community Alternatives
- Substituting garden waste / leaf burning with microbial composting pits.
- Shifting solid biomass heating to radiant oil-filled heaters or thick wool thermal insulation.
- Neighborhood transit clusters and school walking buses when air quality permits, or shared transit on severe smog days.

### 4.4 Direct Impact Calculation Model
Every recommendation is paired with an actionable impact equation:
- **PM2.5 Exposure Drop:** Estimated indoor concentration drop (e.g., -45% to -75% ug/m3).
- **Avoided Household Emissions:** Avoided tailpipe CO2e and particulate mass (e.g., 1.8 kg CO2e per car trip averted).
- **Physical Mechanism:** Plain-language scientific explanation.

---

## 5. Security, Guardrails & Accessibility
1. **Non-Medical Disclaimer:** Standardized medical safety boundary clearly stating that advice is environmental risk mitigation and does not substitute professional medical care.
2. **Prompt Injection Defense:** Strict input sanitization, delimiters, length limits, and structured JSON parsing.
3. **WCAG 2.1 AA:** Accessible forms, visible focus rings, high contrast ratios, non-color-dependent AQI indicators, and ARIA live regions for screen readers.
