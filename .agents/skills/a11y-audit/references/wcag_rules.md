# WCAG 2.1 AA Compliance Checklist for Air Quality Assistant

## 1. Perceivable
- **Guideline 1.1 Text Alternatives:** All informative icons and buttons have readable text labels or `aria-label` attributes.
- **Guideline 1.3 Adaptable:** Content structure relies on semantic landmarks (`<header>`, `<main>`, `<section>`, `<footer>`, `<fieldset>`, `<legend>`).
- **Guideline 1.4 Distinguishable:**
  - Color is not the sole conveyor of information (e.g. AQI Severe must feature an icon, text tier name, numerical value, and descriptive action like "Severe (AQI 420) – High Risk: Remain Indoors").
  - Contrast ratio >= 4.5:1 for body copy and >= 3:1 for large headlines.

## 2. Operable
- **Guideline 2.1 Keyboard Accessible:** All form controls, preset buttons, tab cards, and filter chips are fully reachable and activatable via `Tab` and `Enter`/`Space`.
- **Guideline 2.4 Navigable:** Logical tab order and clearly visible CSS focus rings (`:focus-visible`).

## 3. Understandable
- **Guideline 3.1 Readable:** Plain, human-readable explanations of complex atmospheric and IAQ science (PM2.5, ACH, thermal inversion).
- **Guideline 3.3 Input Assistance:** Clear form labels, error messages, and preset triggers.

## 4. Robust
- **Guideline 4.1 Compatible:** Use of ARIA live regions (`aria-live="polite"` or `role="status"`) for asynchronous GenAI responses so screen readers announce incoming recommendations.
