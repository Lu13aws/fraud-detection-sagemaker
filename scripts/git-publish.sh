#!/bin/bash
# git-publish.sh — Safe push workflow with verification
# Pushes commits to remote with pre-flight checks and post-push verification
# Usage: ./scripts/git-publish.sh [remote] [branch]
#        ./scripts/git-publish.sh origin main
#        ./scripts/git-publish.sh  # Uses current branch

set -e

# Parse arguments
REMOTE="${1:-origin}"
BRANCH="${2:-$(git symbolic-ref --short HEAD 2>/dev/null || echo 'HEAD')}"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🚀 Git Publish Workflow${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Check for uncommitted changes
echo "Step 1: Checking for uncommitted changes..."
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}✗ Uncommitted changes detected${NC}"
    echo ""
    echo "Run 'git add' and 'git commit' first, or:"
    echo "  git stash"
    exit 1
fi
echo -e "${GREEN}✓ No uncommitted changes${NC}"
echo ""

# 2. Confirm branch
echo "Step 2: Confirming branch..."
echo "Current branch: $BRANCH"
echo "Remote: $REMOTE"
echo ""

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo -e "${YELLOW}⚠ WARNING: Pushing to $BRANCH (main/master branch)${NC}"
    read -p "Continue? (yes/no): " -r CONFIRM
    if [[ ! $CONFIRM =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Push cancelled."
        exit 1
    fi
fi
echo ""

# 3. Fetch latest from remote
echo "Step 3: Fetching latest from remote..."
git fetch $REMOTE
echo -e "${GREEN}✓ Fetched${NC}"
echo ""

# 4. Check for diverged branches
echo "Step 4: Checking if branch has diverged..."
MERGE_BASE=$(git merge-base $BRANCH $REMOTE/$BRANCH 2>/dev/null || echo "")
LOCAL_HEAD=$(git rev-parse $BRANCH 2>/dev/null)
REMOTE_HEAD=$(git rev-parse $REMOTE/$BRANCH 2>/dev/null || echo "")

if [ "$REMOTE_HEAD" != "" ] && [ "$LOCAL_HEAD" != "$REMOTE_HEAD" ]; then
    if git merge-base --is-ancestor $REMOTE/$BRANCH $BRANCH 2>/dev/null; then
        echo -e "${GREEN}✓ Local is ahead of remote (can push)${NC}"
    else
        echo -e "${RED}✗ Branch has diverged. Remote has commits you don't have.${NC}"
        echo "Run: git rebase $REMOTE/$BRANCH"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Branches in sync${NC}"
fi
echo ""

# 5. Show commits to be pushed
echo "Step 5: Commits to be pushed:"
if [ "$REMOTE_HEAD" = "" ]; then
    git log $BRANCH --oneline | head -5 | sed 's/^/  /'
    COMMIT_COUNT=$(git log $BRANCH --oneline | wc -l)
else
    git log $REMOTE/$BRANCH..$BRANCH --oneline | head -5 | sed 's/^/  /'
    COMMIT_COUNT=$(git log $REMOTE/$BRANCH..$BRANCH --oneline | wc -l)
fi
echo "  ... ($COMMIT_COUNT total)"
echo ""

# 6. Confirm push
read -p "Ready to push? (yes/no): " -r FINAL_CONFIRM
if [[ ! $FINAL_CONFIRM =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Push cancelled."
    exit 1
fi
echo ""

# 7. Execute push
echo "Step 6: Pushing to $REMOTE/$BRANCH..."
if git push -u $REMOTE $BRANCH; then
    echo -e "${GREEN}✓ Push successful${NC}"
else
    echo -e "${RED}✗ Push failed${NC}"
    exit 1
fi
echo ""

# 8. Verify push reached remote
echo "Step 7: Verifying push reached remote..."
PUSHED_COMMIT=$(git rev-parse $BRANCH)
REMOTE_COMMIT=$(git rev-parse $REMOTE/$BRANCH)

if [ "$PUSHED_COMMIT" = "$REMOTE_COMMIT" ]; then
    echo -e "${GREEN}✓ Verified: Commit is now on remote${NC}"
    echo "Commit: $(git rev-parse --short $BRANCH)"
    echo "Remote: $REMOTE/$BRANCH"
else
    echo -e "${YELLOW}⚠ Warning: Commits don't match (this should not happen)${NC}"
    exit 1
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ Publish complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
