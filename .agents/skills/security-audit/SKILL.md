---
name: security-audit
description: Audits prompt-injection defenses, input sanitization, API key handling, and health guardrails/disclaimers.
---

# Security Audit Skill

Use this skill to audit security defenses across the codebase:
1. Input sanitization and bounds checking on all API endpoints.
2. Prompt injection defense and delimiter isolation for GenAI models.
3. Safe HTML rendering and XSS mitigation (no raw `innerHTML` injection of unescaped user text).
4. Strict `.env` handling: no hardcoded API keys in client-side code or public repos.
5. Non-medical disclaimer and health guardrails for urban smog recommendations.

## Execution
Run the automated security verification script:
```bash
python3 .agents/skills/security-audit/scripts/run_audit.py
```
Or review against `.agents/skills/security-audit/references/checklist.md`.
