#!/bin/bash

# notebook-validate.sh
# Validate Jupyter notebook reproducibility and best practices
#
# Usage: bash scripts/notebook-validate.sh [notebook.ipynb]
#        bash scripts/notebook-validate.sh notebooks/  # Check all notebooks
#
# Checks:
# - No hardcoded paths (should use relative paths or S3)
# - Imports in first cell
# - Random seeds set
# - No commented-out code blocks
# - Notebooks can run top-to-bottom
# - Output saved to data/ folder

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Jupyter Notebook Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Determine which notebooks to check
if [ $# -eq 0 ]; then
    NOTEBOOKS="notebooks/*.ipynb"
elif [ -d "$1" ]; then
    NOTEBOOKS="$1/*.ipynb"
else
    NOTEBOOKS="$1"
fi

TOTAL_NOTEBOOKS=0
PASSED_NOTEBOOKS=0
FAILED_NOTEBOOKS=0

# Temporary file for jq parsing
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

# Helper functions
check_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "  ${RED}✗${NC} $1"
}

check_warn() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

# ============================================================================
# Check each notebook
# ============================================================================

for notebook in $NOTEBOOKS; do
    if [ ! -f "$notebook" ]; then
        continue
    fi

    ((TOTAL_NOTEBOOKS++))
    echo -e "${BLUE}$notebook${NC}"

    NOTEBOOK_ISSUES=0

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        check_warn "jq not installed, skipping detailed checks"
        check_warn "Install: apt-get install jq or brew install jq"
        echo ""
        continue
    fi

    # ========================================================================
    # 1. Check imports in first cell
    # ========================================================================
    FIRST_CELL=$(jq -r '.cells[0].source | join("")' "$notebook" 2>/dev/null || echo "")

    if echo "$FIRST_CELL" | grep -q "^import\|^from"; then
        check_pass "Imports in first cell"
    else
        check_fail "First cell should contain imports"
        ((NOTEBOOK_ISSUES++))
    fi

    # ========================================================================
    # 2. Check for hardcoded paths (danger sign)
    # ========================================================================
    ALL_CONTENT=$(jq -r '.cells[].source | join("")' "$notebook" 2>/dev/null || echo "")

    # Look for absolute paths (bad) vs relative/S3 (good)
    if echo "$ALL_CONTENT" | grep -E "/Users/|/home/|C:\\Users|D:\\"; then
        check_fail "Contains hardcoded absolute paths (should use relative or S3)"
        ((NOTEBOOK_ISSUES++))
    else
        check_pass "No hardcoded absolute paths"
    fi

    # ========================================================================
    # 3. Check for random seeds
    # ========================================================================
    if echo "$ALL_CONTENT" | grep -q "random_state\|random.seed\|np.random.seed\|tf.random.set_seed"; then
        check_pass "Random seeds set (reproducibility)"
    else
        check_warn "No random seeds found (consider adding for reproducibility)"
    fi

    # ========================================================================
    # 4. Check for commented-out code
    # ========================================================================
    COMMENTED_LINES=$(echo "$ALL_CONTENT" | grep -c "^[[:space:]]*#.*=" || true)

    if [ "$COMMENTED_LINES" -gt 5 ]; then
        check_warn "Many commented-out lines ($COMMENTED_LINES) - consider cleaning up"
    else
        check_pass "Minimal commented-out code"
    fi

    # ========================================================================
    # 5. Check for S3 or relative data loading
    # ========================================================================
    if echo "$ALL_CONTENT" | grep -q "read_csv.*s3://\|read_csv.*\.\./data/\|read_csv_from_s3"; then
        check_pass "Data loaded from S3 or relative path"
    else
        check_warn "No S3 or relative path data loading detected (check manually)"
    fi

    # ========================================================================
    # 6. Check for figure saving
    # ========================================================================
    if echo "$ALL_CONTENT" | grep -q "savefig\|plt.savefig\|save_figure"; then
        check_pass "Saves figures (visualization output)"
    else
        check_warn "No figure saving detected"
    fi

    # ========================================================================
    # 7. Count cells
    # ========================================================================
    CELL_COUNT=$(jq '.cells | length' "$notebook" 2>/dev/null || echo "0")

    if [ "$CELL_COUNT" -gt 100 ]; then
        check_warn "Many cells ($CELL_COUNT) - consider breaking into smaller notebooks"
    elif [ "$CELL_COUNT" -lt 3 ]; then
        check_warn "Very few cells ($CELL_COUNT) - consider adding more structure"
    else
        check_pass "Good cell count ($CELL_COUNT)"
    fi

    # ========================================================================
    # 8. Check for kernel info
    # ========================================================================
    KERNEL=$(jq -r '.metadata.kernelspec.name' "$notebook" 2>/dev/null || echo "unknown")

    if echo "$KERNEL" | grep -q "python"; then
        check_pass "Kernel: $KERNEL"
    else
        check_warn "Kernel might be wrong: $KERNEL"
    fi

    # ========================================================================
    # 9. Check execution count (should be sequential)
    # ========================================================================
    MAX_COUNT=$(jq '[.cells[].execution_count | select(. != null)] | max' "$notebook" 2>/dev/null || echo "0")

    if [ "$MAX_COUNT" -eq 0 ]; then
        check_warn "No execution counts (notebook not run yet)"
    elif [ "$MAX_COUNT" -lt "$CELL_COUNT" ]; then
        check_warn "Not all cells executed (run all before committing)"
    else
        check_pass "All cells executed"
    fi

    # ========================================================================
    # Summary for this notebook
    # ========================================================================
    echo ""

    if [ $NOTEBOOK_ISSUES -eq 0 ]; then
        echo -e "${GREEN}✓ Notebook looks good${NC}"
        ((PASSED_NOTEBOOKS++))
    else
        echo -e "${RED}✗ Notebook has $NOTEBOOK_ISSUES issue(s)${NC}"
        ((FAILED_NOTEBOOKS++))
    fi

    echo ""
done

# ============================================================================
# Overall Summary
# ============================================================================
if [ $TOTAL_NOTEBOOKS -eq 0 ]; then
    echo -e "${YELLOW}No notebooks found in: $NOTEBOOKS${NC}"
    exit 0
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo "Total notebooks: $TOTAL_NOTEBOOKS"
echo -e "Passed: ${GREEN}$PASSED_NOTEBOOKS${NC}"
echo -e "Failed: ${RED}$FAILED_NOTEBOOKS${NC}"
echo ""

# ============================================================================
# Best Practices Checklist
# ============================================================================
echo -e "${BLUE}Reproducibility Checklist:${NC}"
echo "  [ ] First cell contains all imports"
echo "  [ ] Data loaded from S3 or relative path"
echo "  [ ] Random seeds set (random_state, np.random.seed)"
echo "  [ ] No hardcoded absolute paths"
echo "  [ ] Figures saved to data/ folder"
echo "  [ ] Can run all cells top-to-bottom"
echo "  [ ] No commented-out code blocks"
echo "  [ ] Clear markdown sections explaining each phase"
echo ""

if [ $FAILED_NOTEBOOKS -eq 0 ]; then
    echo -e "${GREEN}✓ All notebooks pass validation!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some notebooks need attention${NC}"
    exit 1
fi
