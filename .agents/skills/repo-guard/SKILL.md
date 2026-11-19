---
name: repo-guard
description: Enforce repository footprint (< 10 MB), single-branch constraint (main), and verify zero secret leaks or forbidden build artifacts.
---

# Repo Guard Verification Skill

Use this skill to verify non-negotiable repository submission constraints:
1. Total repository size is strictly under 10 MB.
2. Only a single Git branch (`main`) exists locally and remotely.
3. Zero secrets, `.env` files, or non-committed heavy directories (`node_modules/`, `.venv/`) are tracked.
4. Git working directory is clean.

## Execution
Run the bundled verification script:
```bash
bash .agents/skills/repo-guard/scripts/check_repo.sh
```

## Exit Conditions
- Returns `0` if all repository constraints are strictly met.
- Returns non-zero error with diagnostic messages if any threshold is violated.
