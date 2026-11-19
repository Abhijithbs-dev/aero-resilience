# Project Task Tracker: GenAI Winter Smog & Urban Air Quality Assistant

> **Platform:** [Google Antigravity](https://antigravity.google/blog/introducing-google-antigravity) (Agent Manager, Planning Mode, [Artifacts](https://antigravity.google/docs/artifacts/), [Agent Skills](https://antigravity.google/docs/skills/), Terminal Sandbox, and IDE Browser)
> **Status Legend:** `[ ]` Pending · `[/]` In Progress · `[x]` Completed

---

## Project Scope & Hard Submission Rules

- **Problem Statement:** Build a GenAI-powered assistant that helps families and communities navigate severe winter smog and urban air pollution by recommending **low-emission daily routines**, **indoor air quality (IAQ) hacks**, and **sustainable alternatives** tailored to their location and lifestyle, while clearly explaining the **direct impact** of each choice.
- **Chosen Vertical:** Urban Families & Community Environmental Resilience (Winter Smog & Air Quality Guidance)
- **Non-Negotiable Challenge Constraints:**
  - **Public Repository:** GitHub repository must be set to **Public**.
  - **Single Branch Only:** Keep all commits on **one branch** (`main`); delete any local/remote secondary branches before submission.
  - **Repository Size Limit:** Total repository size must stay **strictly under 10 MB** (no `node_modules`, `.venv`, build artifacts, or large media committed).
  - **Attempt Cap:** Maximum **3 submission attempts**—run all verification skills before each push/submission.

---

## Phase 0: Environment, Repo & Antigravity Setup

> **Antigravity Features:** Workspace Rules (`AGENTS.md` / `.agents/rules/`), [Agent Skills](https://antigravity.google/docs/skills/) (`.agents/skills/`), Terminal Sandbox

- [x] **0.1 Verify Prerequisites** `[High Impact | Compliance]`
  - Confirm Google Antigravity is installed and authenticated.
  - Confirm Git is installed and configured (`git config --list`) with your active GitHub account.
- [x] **0.2 Initialize Single-Branch Public Repository** `[High Impact | Compliance]`
  - Create a new **Public** repository on GitHub initialized with a single `main` branch.
  - Clone the repository inside Google Antigravity and verify only one branch exists (`git branch -a`).
  - Add a strict `.gitignore` excluding dependencies (`node_modules/`, `.venv/`, `__pycache__/`), environment files (`.env*`), build outputs, and large binaries to protect the **< 10 MB** limit.
- [x] **0.3 Configure Always-On Antigravity Rules (`AGENTS.md`)** `[Medium Impact | Code Quality & Security]`
  - Create `AGENTS.md` (or modular rule files in `.agents/rules/`) at the repository root defining persistent project guardrails:
    - Never commit secrets, API keys, or `.env` files.
    - Never create secondary Git branches; commit only to `main`.
    - Keep dependencies minimal and repository footprint under 10 MB.
    - Enforce clean modular structure, type safety, input validation, and WCAG 2.1 AA accessibility across generated code.
- [x] **0.4 Scaffold Custom Workspace Agent Skills (`.agents/skills/`)** `[Medium Impact | Efficiency & Quality]`
  - Create reusable, on-demand [Agent Skills](https://antigravity.google/docs/skills/) with `SKILL.md` YAML frontmatter (`name`, `description`) and optional `scripts/` (avoid deprecated `.agents/workflows/` per the [Workflows to Skills migration guide](https://antigravity.google/docs/migration/workflows-to-skills/)):
    - `.agents/skills/repo-guard/SKILL.md` → Invoked via `/repo-guard` to check repo size (< 10 MB), single-branch rule, and secret leaks.
    - `.agents/skills/security-audit/SKILL.md` → Invoked via `/security-audit` to audit prompt-injection defenses, input sanitization, and API key handling.
    - `.agents/skills/a11y-audit/SKILL.md` → Invoked via `/a11y-audit` to verify WCAG contrast, ARIA landmarks, and keyboard navigation.
    - `.agents/skills/readme-sync/SKILL.md` → Invoked via `/readme-sync` to keep `README.md` aligned with the vertical, architecture, logic, and assumptions.

---

## Phase 1: Architecture & Context-Driven Decision Design

> **Antigravity Features:** Planning Mode, `implementation_plan.md` Artifact, Paired Review Pattern

- [x] **1.1 Define Vertical, User Personas & Decision Matrix** `[High Impact | Problem Statement Alignment]`
  - Switch Antigravity to **Planning Mode** and generate an `implementation_plan.md` artifact before writing application code.
  - Define target personas (e.g., parents with young children, elderly residents, daily commuters, apartment renters, community organizers) and context inputs:
    - **Location & Air Quality Context:** City/neighborhood, AQI / PM2.5 severity tier (Moderate, Poor, Very Poor, Severe), time of day, weather/inversion notes.
    - **Household & Lifestyle Context:** Commute mode, cooking/heating source, housing type (apartment vs. independent home), budget tier, and vulnerable members (children, seniors, asthma/respiratory sensitivity).
- [x] **1.2 Design Logical Decision Engine & Impact Explanation Model** `[High Impact | Problem Statement Alignment]`
  - Map context inputs to deterministic + GenAI-hybrid recommendation pathways:
    - **Low-Emission Daily Routines:** Timing outdoor errands for lower-inversion windows, transit/carpool/active-travel swaps, school-run adjustments, and low-emission cooking/heating habits.
    - **Indoor Air Quality (IAQ) Hacks:** Budget-tiered options (DIY Corsi-Rosenthal box fans, wet mopping vs. dry sweeping, strategic cross-ventilation windows, door/window draft sealing, exhaust fan usage, HEPA placement).
    - **Sustainable Alternatives:** Practical local swaps (public transit/EV/cycling where safe, induction/LPG over biomass/solid fuel, community carpooling, dry-leaf composting instead of burning).
    - **Direct Impact Explanations:** Pair every suggestion with a clear, human-readable explanation of **why it matters** (e.g., indoor PM2.5 reduction mechanism, personal exposure drop, household emissions avoided, and community air-shed benefit).
- [x] **1.3 Review & Approve `implementation_plan.md` Artifact** `[High Impact | Code Quality]`
  - Use Antigravity's visual review pane to inspect the proposed folder structure, API contracts, data flow, and fallback behavior.
  - Confirm the stack is lightweight and easy to run locally (keeping total repo size well under 10 MB).

---

## Phase 2: Core GenAI Assistant & Backend Implementation

> **Antigravity Features:** Agent Manager (Mission Control), Concurrent Subagents, Code Diff Artifacts

- [x] **2.1 Build Context & Air Quality Data Layer** `[High Impact | Problem Statement Alignment]`
  - Implement location and AQI/PM2.5 ingestion (live public AQI API with graceful fallback to user-entered AQI or realistic severity presets so the app always works without brittle dependencies).
  - Normalize AQI tiers and pollution triggers into a clean context object passed to the decision engine.
- [x] **2.2 Implement Structured GenAI Prompting & Reasoning Pipeline** `[High Impact | Problem Statement Alignment & Efficiency]`
  - Build a modular prompt builder that injects user location, AQI severity, household profile, and lifestyle constraints.
  - Enforce structured JSON/schema output so recommendations always return distinct, verifiable sections:
    1. **Risk Summary & Action Priority** (tailored to severity and vulnerable household members)
    2. **Low-Emission Daily Routine Plan** (morning, commute, evening adjustments)
    3. **Indoor Air Quality Hacks** (tagged by cost: Free / Low-Cost / Equipment)
    4. **Sustainable Alternatives** (short-term swaps + community actions)
    5. **Direct Impact Breakdown** (clear "Action → Mechanism → Health/Emission Impact" explanation for every recommendation)
  - Include a deterministic rule-based fallback or offline demo mode if the LLM API key is missing or rate-limited.
- [x] **2.3 Implement Impact Estimator Utility** `[Medium Impact | Problem Statement Alignment]`
  - Add transparent, assumption-documented calculations (e.g., estimated daily CO2e avoided from commute swaps or relative exposure reduction) with clear labels distinguishing estimates from measured readings.
- [x] **2.4 Commit & Push Backend Milestone on `main`** `[High Impact | Compliance]`
  - Review code diffs in Antigravity, commit cleanly on `main`, and push progress.

---

## Phase 3: Frontend Interface & Inclusive Accessibility

> **Antigravity Features:** Agent Manager, Editor Side Panel, Visual Screenshots

- [x] **3.1 Build Context Intake & Interactive Assistant UI** `[High Impact | Usability]`
  - Create a clean, responsive interface allowing families and community members to:
    - Enter location / AQI level (or select quick winter-smog presets for instant testing).
    - Select household profile & lifestyle constraints (commute, housing, budget, sensitive groups).
    - Ask follow-up questions in a dynamic conversational assistant view.
- [x] **3.2 Design Actionable Impact Cards & Routine Views** `[High Impact | Usability & Alignment]`
  - Display recommendations in scannable cards grouped by **Daily Routines**, **IAQ Hacks**, and **Sustainable Alternatives**.
  - Highlight the **Direct Impact** badge/explanation on every card so users immediately understand the payoff of each choice.
  - Add a **Community Action / Shareable Family Checklist** view for practical real-world use.
- [x] **3.3 Implement Accessibility (WCAG 2.1 AA)** `[Medium Impact | Accessibility]`
  - Use semantic HTML (`<main>`, `<nav>`, `<section>`, `<button>`, `<label>`) and logical heading hierarchy.
  - Ensure >= 4.5:1 text color contrast (never rely on color alone for AQI severity—pair colors with icons and clear text labels like "Severe – Stay Indoors").
  - Support full keyboard navigation, visible focus states, ARIA live regions for dynamic GenAI responses, and plain-language microcopy.
- [x] **3.4 Run `/a11y-audit` Skill & Commit on `main`** `[Low Impact | Accessibility Polish]`
  - Execute the custom `a11y-audit` skill to catch missing labels, contrast issues, or keyboard traps, fix findings, and push to `main`.

---

## Phase 4: Security, Guardrails & Resource Efficiency

> **Antigravity Features:** Custom `/security-audit` Skill, Terminal Sandbox

- [x] **4.1 Secure API Keys & Configuration** `[High Impact | Security]`
  - Load all API keys strictly from environment variables (`.env` excluded via `.gitignore`); provide a safe `.env.example` template with placeholder keys only.
  - Never expose backend API keys in client-side bundles.
- [x] **4.2 Harden Inputs, Prompts & Health Guardrails** `[High Impact | Security]`
  - Validate and sanitize all user inputs (length caps, schema validation, XSS-safe rendering—avoid unsafe raw HTML injection).
  - Add system-prompt guardrails against prompt injection and off-topic abuse.
  - Include clear non-medical disclaimer framing for respiratory/health advice (advising users to consult healthcare professionals during medical emergencies).
- [x] **4.3 Optimize Resource & Token Efficiency** `[Medium Impact | Efficiency]`
  - Cache repeated AQI lookups and identical context queries to minimize redundant API calls and latency.
  - Keep prompts concise, set sensible `max_tokens` limits, and avoid heavy unused libraries or large static assets.
- [x] **4.4 Run `/security-audit` Skill & Commit on `main`** `[Medium Impact | Security]`
  - Run `/security-audit` to verify zero hardcoded secrets, safe output rendering, and proper error handling (no stack traces leaked to users).

---

## Phase 5: Automated Testing & Antigravity Browser Verification

> **Antigravity Features:** Terminal Sandbox, IDE Browser (Chrome Subagent), Browser Recordings & Screenshot Artifacts

- [x] **5.1 Write & Run Unit Tests in Terminal Sandbox** `[Medium Impact | Testing]`
  - Test context parsing, AQI severity classification, decision-engine routing, impact calculations, and input validation/sanitization.
  - Test edge cases: extreme/hazardous AQI (500+), missing location, empty inputs, API timeout/fallback behavior, and prompt-injection payloads.
- [x] **5.2 Write & Run Integration / API Tests** `[Medium Impact | Testing]`
  - Validate API endpoints (valid payload, malformed payload, rate-limit/error responses) with mocked LLM responses so tests run fast and deterministically without spending live tokens.
- [x] **5.3 End-to-End UI Verification with Antigravity IDE Browser** `[Medium Impact | Testing & Accessibility]`
  - Launch the app locally in the Terminal Sandbox and instruct Antigravity's **IDE Browser** to test complete user journeys:
    1. Family with children in severe winter smog (high PM2.5) → verify tailored IAQ hacks, indoor routine shifts, and direct impact explanations.
    2. Budget-conscious apartment commuter → verify low-cost IAQ hacks and transit/sustainable alternatives.
    3. Mobile viewport & keyboard-only navigation check.
  - Review the generated **browser recording** and **visual screenshot artifacts** in Antigravity's review pane to confirm zero layout breaks or console errors.
- [x] **5.4 Commit Passing Test Suite on `main`** `[Medium Impact | Testing]`
  - Ensure a single documented test command passes cleanly and push to `main`.

---

## Phase 6: Documentation, Compliance Audit & Final Submission

> **Antigravity Features:** Custom `/readme-sync` & `/repo-guard` Skills, Terminal Sandbox

- [x] **6.1 Author Complete `README.md`** `[High Impact | Submission Requirement]`
  - Run `/readme-sync` and verify `README.md` clearly covers all four required sections:
    1. **Chosen Vertical:** Urban Families & Community Environmental Resilience (Winter Smog & Air Quality).
    2. **Approach and Logic:** Context-driven decision architecture, GenAI + deterministic hybrid reasoning, and impact explanation methodology.
    3. **How the Solution Works:** Architecture overview, setup instructions (`.env.example` → install → run → test), and example user flows.
    4. **Assumptions Made:** AQI source/fallback assumptions, emission/exposure estimation formulas, non-medical guidance scope, and regional applicability.
- [x] **6.2 Run Final `/repo-guard` Compliance Gate** `[High Impact | Compliance]`
  - Execute `/repo-guard` in Terminal Sandbox and verify every hard rule passes:
    - [x] Repository size is **strictly < 10 MB** (`du -sh .` and `git count-objects -vH`).
    - [x] Exactly **one branch** exists locally and on GitHub (`git branch -a`).
    - [x] Repository visibility is **Public** on GitHub.
    - [x] Zero secrets, `.env` files, or junk artifacts tracked in Git (`git ls-files`).
    - [x] Clean clone test succeeds and all automated tests pass.
- [x] **6.3 Submit Public GitHub Repository Link** `[High Impact | Submission]`
  - Review the official submission guide document one final time.
  - Submit the public GitHub repository URL (conserving your **3-attempt maximum**).

---

## Custom Antigravity Skills Blueprint (`.agents/skills/`)

| Skill Folder | Slash Command | Purpose | Bundled Assets |
| :--- | :--- | :--- | :--- |
| `.agents/skills/repo-guard/` | `/repo-guard` | Enforces < 10 MB repo limit, single-branch rule, and secret-free Git tree | `SKILL.md`, `scripts/check_repo.sh` |
| `.agents/skills/security-audit/` | `/security-audit` | Checks input validation, XSS safety, prompt guardrails, and env-var usage | `SKILL.md`, `references/checklist.md` |
| `.agents/skills/a11y-audit/` | `/a11y-audit` | Audits semantic HTML, WCAG 2.1 AA contrast, ARIA roles, and keyboard flow | `SKILL.md`, `references/wcag_rules.md` |
| `.agents/skills/readme-sync/` | `/readme-sync` | Verifies README covers vertical, logic, usage, and assumptions | `SKILL.md`, `templates/README_template.md` |

---

## Evaluation Focus & Impact Alignment Matrix

| Evaluation Area | Impact Tier | Verification Artifact / Gate |
| :--- | :--- | :--- |
| **Problem Statement Alignment** | High Impact | Tailored routines, IAQ hacks, sustainable swaps, and direct impact explanations verified across personas |
| **Code Quality** | High / Medium Impact | Clean modular architecture, `AGENTS.md` standards, reviewed code diffs |
| **Security** | High / Medium Impact | Passing `/security-audit`, `.env` isolation, sanitized inputs, medical disclaimer |
| **Testing** | Medium Impact | Passing unit + mocked integration tests + Antigravity IDE Browser recording |
| **Efficiency** | Medium Impact | Response caching, concise prompts, lightweight repo (< 10 MB) |
| **Accessibility** | Medium / Low Impact | Passing `/a11y-audit`, keyboard navigation, non-color-only AQI indicators |
| **Polish & Documentation** | Low / High Impact | Complete 4-section `README.md`, clean Git history on single `main` branch |
