---
name: a11y-audit
description: Audits WCAG 2.1 AA accessibility compliance, ARIA live regions, contrast ratios, and keyboard navigation.
---

# Accessibility Audit Skill

Use this skill to audit frontend accessibility (WCAG 2.1 AA):
1. Semantic HTML landmarks (`<main>`, `<nav>`, `<header>`, `<section>`, `<article>`).
2. Multi-modal AQI severity indications (never rely solely on red/yellow/green color).
3. Text contrast ratio >= 4.5:1 for standard text.
4. Visible focus indicators on all interactive inputs and buttons.
5. ARIA live regions (`aria-live="polite"`, `role="status"`) for dynamic AI recommendation updates.
6. Accessible labels (`aria-label`, `<label for="...">`) for all form fields.

## Execution
Run the automated a11y scanner script:
```bash
python3 .agents/skills/a11y-audit/scripts/run_a11y_check.py
```
Or review against `.agents/skills/a11y-audit/references/wcag_rules.md`.
