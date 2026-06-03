#!/bin/bash
# git-feature-branch.sh — Create and set up a feature branch
# Enforces naming conventions and sets upstream tracking
# Usage: ./scripts/git-feature-branch.sh feature/my-feature
#        ./scripts/git-feature-branch.sh bugfix/issue-123
#        ./scripts/git-feature-branch.sh docs/update-readme

set -e

BRANCH_NAME="$1"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🌿 Create Feature Branch${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Validate branch name provided
if [ -z "$BRANCH_NAME" ]; then
    echo -e "${RED}✗ Branch name required${NC}"
    echo ""
    echo "Usage: ./scripts/git-feature-branch.sh <branch-name>"
    echo ""
    echo "Valid prefixes:"
    echo "  feature/    — new functionality"
    echo "  bugfix/     — bug fixes"
    echo "  docs/       — documentation only"
    echo "  refactor/   — code refactoring (no logic changes)"
    echo ""
    echo "Examples:"
    echo "  ./scripts/git-feature-branch.sh feature/add-validation"
    echo "  ./scripts/git-feature-branch.sh bugfix/fix-edge-case"
    echo "  ./scripts/git-feature-branch.sh docs/api-docs"
    exit 1
fi

# Validate naming convention
PREFIX=$(echo "$BRANCH_NAME" | cut -d'/' -f1)
VALID_PREFIXES=("feature" "bugfix" "docs" "refactor" "hotfix")
PREFIX_VALID=0

for valid_prefix in "${VALID_PREFIXES[@]}"; do
    if [ "$PREFIX" = "$valid_prefix" ]; then
        PREFIX_VALID=1
        break
    fi
done

if [ $PREFIX_VALID -eq 0 ]; then
    echo -e "${RED}✗ Invalid branch prefix: $PREFIX${NC}"
    echo ""
    echo "Valid prefixes: ${VALID_PREFIXES[*]}"
    exit 1
fi

if [ -z "$(echo "$BRANCH_NAME" | cut -d'/' -f2)" ]; then
    echo -e "${RED}✗ Branch name must have format: <prefix>/<name>${NC}"
    exit 1
fi

echo "Branch name: $BRANCH_NAME"
echo "Prefix: $PREFIX"
echo ""

# Check current branch is clean
echo "Step 1: Checking working tree is clean..."
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}✗ Uncommitted changes detected${NC}"
    echo "Commit or stash changes first: git stash"
    exit 1
fi
echo -e "${GREEN}✓ Working tree clean${NC}"
echo ""

# Ensure we're on main/master
echo "Step 2: Switching to main branch..."
if git rev-parse --verify main >/dev/null 2>&1; then
    MAIN_BRANCH="main"
elif git rev-parse --verify master >/dev/null 2>&1; then
    MAIN_BRANCH="master"
else
    echo -e "${RED}✗ No main or master branch found${NC}"
    exit 1
fi

git checkout $MAIN_BRANCH >/dev/null 2>&1
echo -e "${GREEN}✓ On $MAIN_BRANCH${NC}"
echo ""

# Fetch latest
echo "Step 3: Fetching latest changes..."
git fetch origin >/dev/null 2>&1
git reset --hard origin/$MAIN_BRANCH >/dev/null 2>&1
echo -e "${GREEN}✓ Updated to latest${NC}"
echo ""

# Create branch
echo "Step 4: Creating branch..."
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Branch already exists${NC}"
    echo "Switch to existing branch with: git checkout $BRANCH_NAME"
    exit 1
fi

git checkout -b "$BRANCH_NAME" >/dev/null 2>&1
echo -e "${GREEN}✓ Branch created locally${NC}"
echo ""

# Set upstream tracking
echo "Step 5: Setting upstream tracking..."
git push -u origin "$BRANCH_NAME" >/dev/null 2>&1
echo -e "${GREEN}✓ Upstream set to origin/$BRANCH_NAME${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ Branch ready!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Current branch: $(git symbolic-ref --short HEAD)"
echo ""
echo "Next steps:"
echo "  1. Make your changes"
echo "  2. git add <files>"
echo "  3. ./scripts/git-validate.sh"
echo "  4. git commit -m '<message>'"
echo "  5. ./scripts/git-publish.sh"
