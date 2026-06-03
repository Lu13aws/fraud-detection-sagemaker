#!/bin/bash
# git-validate.sh — Pre-commit security check
# Detects secrets, large files, and other risky changes before commit
# Usage: ./scripts/git-validate.sh

set -e

FAIL=0
WARN=0

echo "🔍 Running pre-commit validation..."
echo ""

# Color output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check for staged changes
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || true)
if [ -z "$STAGED_FILES" ]; then
    echo -e "${YELLOW}⚠ No staged files. Run 'git add <files>' first.${NC}"
    exit 1
fi

echo "Staged files:"
echo "$STAGED_FILES" | sed 's/^/  /'
echo ""

# 1. Check for secrets and credentials
echo "Checking for secrets and credentials..."
SECRETS_PATTERNS=("\.env$" "\.pem$" "\.key$" "credentials\.json$" "\.aws" "secret" "password" "token")
FOUND_SECRETS=0

for pattern in "${SECRETS_PATTERNS[@]}"; do
    if echo "$STAGED_FILES" | grep -q -i "$pattern"; then
        echo -e "${RED}✗ Found potential secret: $pattern${NC}"
        echo "$STAGED_FILES" | grep -i "$pattern" | sed 's/^/    /'
        FOUND_SECRETS=1
        FAIL=1
    fi
done

if [ $FOUND_SECRETS -eq 0 ]; then
    echo -e "${GREEN}✓ No secrets detected${NC}"
fi
echo ""

# 2. Check for large files
echo "Checking for large files (> 50MB)..."
LARGE_FILES=$(git diff --cached --name-only --diff-filter=A -z | xargs -0 ls -lh 2>/dev/null | awk '$5 ~ /[0-9]+M|G/ && $(NF-4) > 50 {print $NF}' || true)

if [ -n "$LARGE_FILES" ]; then
    echo -e "${RED}✗ Found large files:${NC}"
    echo "$LARGE_FILES" | sed 's/^/    /'
    FAIL=1
else
    echo -e "${GREEN}✓ No large files detected${NC}"
fi
echo ""

# 3. Check for binary files
echo "Checking for uncommon binary files..."
BINARY_PATTERNS=("\.pkl$" "\.joblib$" "\.model$" "\.parquet$" "\.h5$" "\.onnx$")
FOUND_BINARIES=0

for pattern in "${BINARY_PATTERNS[@]}"; do
    if echo "$STAGED_FILES" | grep -q "$pattern"; then
        echo -e "${YELLOW}⚠ Found binary artifact: $pattern${NC}"
        echo "$STAGED_FILES" | grep "$pattern" | sed 's/^/    /'
        WARN=1
    fi
done
echo ""

# 4. Check for merge conflicts
echo "Checking for merge conflict markers..."
CONFLICTS=$(git diff --cached | grep -E "^[+<>|=]" | head -5 || true)
if [ -n "$CONFLICTS" ]; then
    echo -e "${RED}✗ Found merge conflict markers${NC}"
    FAIL=1
else
    echo -e "${GREEN}✓ No merge conflicts${NC}"
fi
echo ""

# 5. Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ Validation passed${NC}"
    if [ $WARN -gt 0 ]; then
        echo -e "${YELLOW}⚠ Warnings detected (see above)${NC}"
    fi
    echo ""
    echo "Safe to commit. Run:"
    echo "  git commit -m '<message>'"
    exit 0
else
    echo -e "${RED}✗ Validation failed${NC}"
    echo ""
    echo "DO NOT COMMIT. Issues found:"
    echo "  - Remove secrets before staging"
    echo "  - Reduce file sizes or use LFS"
    echo "  - Resolve merge conflicts"
    echo ""
    echo "After fixing, run: git add <files> && ./scripts/git-validate.sh"
    exit 1
fi
