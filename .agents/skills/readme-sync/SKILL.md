---
name: readme-sync
description: Validates and synchronizes README.md to ensure all four required sections (Vertical, Approach, Usage, Assumptions) are thoroughly documented.
---

# README Sync Skill

Use this skill to ensure `README.md` strictly adheres to competition submission criteria:
1. **Chosen Vertical:** Urban Families & Community Environmental Resilience (Winter Smog & Air Quality).
2. **Approach and Logic:** Context-driven decision engine, hybrid GenAI + deterministic rule architecture, and impact quantification methodology.
3. **How the Solution Works:** Architecture overview, setup guide (`.env.example` -> dependencies -> run -> test), and representative user flows.
4. **Assumptions Made:** Air quality data sources & fallbacks, PM2.5/CO2e formulas, health boundaries (non-medical), and regional winter smog characteristics.

## Execution
Run the verification script:
```bash
python3 .agents/skills/readme-sync/scripts/verify_readme.py
```
Or reference `templates/README_template.md`.
