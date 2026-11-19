#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo " Running Repo Guard Audit (/repo-guard)"
echo "=========================================="

FAILED=0

# 1. Check Git Branch - strictly single branch 'main'
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
echo "[1/4] Checking current branch... Current: '${CURRENT_BRANCH}'"
if [ "${CURRENT_BRANCH}" != "main" ]; then
    echo "❌ ERROR: Current branch is not 'main'! Must be 'main'."
    FAILED=1
else
    echo "✅ Branch is 'main'."
fi

BRANCH_COUNT=$(git branch | wc -l)
if [ "${BRANCH_COUNT}" -gt 1 ]; then
    echo "❌ ERROR: Multiple local branches detected (${BRANCH_COUNT}). Only 'main' allowed:"
    git branch
    FAILED=1
else
    echo "✅ Exactly 1 local branch detected."
fi

# 2. Check Repository Footprint (< 10 MB)
echo "[2/4] Checking repository size..."
# Measure total directory size in KB
TOTAL_SIZE_KB=$(du -sk . | awk '{print $1}')
MAX_SIZE_KB=10240 # 10 MB in KB

echo "Current workspace size: ${TOTAL_SIZE_KB} KB (Max allowed: ${MAX_SIZE_KB} KB)"
if [ "${TOTAL_SIZE_KB}" -ge "${MAX_SIZE_KB}" ]; then
    echo "❌ ERROR: Repository size exceeds 10 MB limit (${TOTAL_SIZE_KB} KB)!"
    FAILED=1
else
    echo "✅ Repository size is well under 10 MB limit."
fi

# 3. Check for forbidden files in Git index
echo "[3/4] Checking Git index for tracked forbidden files..."
TRACKED_SECRETS=$(git ls-files | grep -E '(\.env$|\.env\.local$|\.pem$|\.key$|id_rsa|credentials\.json)' || true)
if [ -n "${TRACKED_SECRETS}" ]; then
    echo "❌ ERROR: Secrets or env files tracked in Git:"
    echo "${TRACKED_SECRETS}"
    FAILED=1
else
    echo "✅ No secret files tracked in Git index."
fi

FORBIDDEN_DIRS=$(git ls-files | grep -E '^(node_modules/|\.venv/|venv/|__pycache__/|\.pytest_cache/|dist/|build/)' || true)
if [ -n "${FORBIDDEN_DIRS}" ]; then
    echo "❌ ERROR: Heavy build/virtualenv files tracked in Git:"
    echo "${FORBIDDEN_DIRS}"
    FAILED=1
else
    echo "✅ No forbidden dependencies or build artifacts tracked in Git index."
fi

# 4. Check for .gitignore presence
echo "[4/4] Checking .gitignore configuration..."
if [ ! -f ".gitignore" ]; then
    echo "❌ ERROR: .gitignore is missing!"
    FAILED=1
else
    echo "✅ .gitignore present and active."
fi

echo "=========================================="
if [ "${FAILED}" -eq 0 ]; then
    echo "🎉 REPO-GUARD PASSED: All submission repository constraints satisfied!"
    exit 0
else
    echo "💥 REPO-GUARD FAILED: Please fix above violations before submission."
    exit 1
fi
