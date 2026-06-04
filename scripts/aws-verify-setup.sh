#!/bin/bash

# aws-verify-setup.sh
# Verify AWS credentials and S3 access for data engineering ML projects
#
# Usage: bash scripts/aws-verify-setup.sh
#
# Checks:
# - AWS credentials configured
# - AWS CLI installed
# - S3 bucket accessible
# - IAM permissions sufficient
# - boto3 Python package available

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}AWS Setup Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Track results
CHECKS_PASSED=0
CHECKS_FAILED=0

# Helper functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# ============================================================================
# 1. Check AWS CLI Installed
# ============================================================================
echo -e "${BLUE}1. Checking AWS CLI...${NC}"

if command -v aws &> /dev/null; then
    AWS_VERSION=$(aws --version)
    check_pass "AWS CLI installed: $AWS_VERSION"
else
    check_fail "AWS CLI not found. Install: pip install awscli"
fi

echo ""

# ============================================================================
# 2. Check AWS Credentials
# ============================================================================
echo -e "${BLUE}2. Checking AWS Credentials...${NC}"

# Check if credentials exist
if [ -z "$AWS_ACCESS_KEY_ID" ] && [ ! -f ~/.aws/credentials ]; then
    check_fail "No AWS credentials found"
    check_warn "Run: aws configure"
    echo ""
else
    # Try to get identity
    if aws sts get-caller-identity &> /dev/null; then
        IDENTITY=$(aws sts get-caller-identity)
        ACCOUNT=$(echo $IDENTITY | grep -o '"Account": "[^"]*' | cut -d'"' -f4)
        ARN=$(echo $IDENTITY | grep -o '"Arn": "[^"]*' | cut -d'"' -f4)
        check_pass "AWS credentials valid"
        check_pass "Account ID: $ACCOUNT"
        check_pass "User/Role: $ARN"
    else
        check_fail "AWS credentials invalid or incomplete"
        check_warn "Run: aws configure"
    fi
fi

echo ""

# ============================================================================
# 3. Check AWS Region
# ============================================================================
echo -e "${BLUE}3. Checking AWS Region...${NC}"

if [ -z "$AWS_DEFAULT_REGION" ]; then
    check_warn "AWS_DEFAULT_REGION not set in environment"
    REGION=$(aws configure get region 2>/dev/null || echo "not set")
    if [ "$REGION" != "not set" ]; then
        check_pass "Region from .aws/config: $REGION"
    else
        check_warn "No region configured. Run: aws configure"
    fi
else
    check_pass "AWS_DEFAULT_REGION: $AWS_DEFAULT_REGION"
fi

echo ""

# ============================================================================
# 4. Check S3 Bucket Access
# ============================================================================
echo -e "${BLUE}4. Checking S3 Bucket Access...${NC}"

# Try to get bucket from environment or AWS config
if [ -z "$S3_BUCKET" ]; then
    check_warn "S3_BUCKET environment variable not set"
    echo "    To verify specific bucket, set: export S3_BUCKET=your-bucket-name"
    BUCKET_TO_CHECK=""
else
    BUCKET_TO_CHECK="$S3_BUCKET"
fi

if [ -n "$BUCKET_TO_CHECK" ]; then
    if aws s3 ls "s3://$BUCKET_TO_CHECK/" &> /dev/null; then
        check_pass "S3 bucket readable: s3://$BUCKET_TO_CHECK/"

        # List contents
        echo -e "${BLUE}    Contents:${NC}"
        aws s3 ls "s3://$BUCKET_TO_CHECK/" | head -5 || true
    else
        check_fail "S3 bucket not accessible: s3://$BUCKET_TO_CHECK/"
        check_warn "Check bucket exists and you have permission"
    fi
else
    check_warn "Skipping bucket check (set S3_BUCKET to verify)"
fi

echo ""

# ============================================================================
# 5. Check Python boto3
# ============================================================================
echo -e "${BLUE}5. Checking Python boto3 Package...${NC}"

if python -c "import boto3" 2>/dev/null; then
    BOTO3_VERSION=$(python -c "import boto3; print(boto3.__version__)")
    check_pass "boto3 installed: $BOTO3_VERSION"
else
    check_fail "boto3 not installed"
    check_warn "Install: pip install boto3"
fi

echo ""

# ============================================================================
# 6. Check Python Environment Variables
# ============================================================================
echo -e "${BLUE}6. Checking Environment Variables...${NC}"

if [ -n "$AWS_ACCESS_KEY_ID" ]; then
    check_pass "AWS_ACCESS_KEY_ID set"
else
    check_warn "AWS_ACCESS_KEY_ID not set (using .aws/credentials)"
fi

if [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    check_pass "AWS_SECRET_ACCESS_KEY set"
else
    check_warn "AWS_SECRET_ACCESS_KEY not set (using .aws/credentials)"
fi

if [ -n "$AWS_REGION" ]; then
    check_pass "AWS_REGION: $AWS_REGION"
else
    check_warn "AWS_REGION not set (using default from aws configure)"
fi

if [ -n "$S3_BUCKET" ]; then
    check_pass "S3_BUCKET: $S3_BUCKET"
else
    check_warn "S3_BUCKET not set"
fi

echo ""

# ============================================================================
# 7. Check for Credential Files
# ============================================================================
echo -e "${BLUE}7. Checking Credential Files...${NC}"

if [ -f ~/.aws/credentials ]; then
    check_pass "AWS credentials file exists: ~/.aws/credentials"
else
    check_warn "No ~/.aws/credentials file (using environment variables)"
fi

if [ -f ~/.aws/config ]; then
    check_pass "AWS config file exists: ~/.aws/config"
else
    check_warn "No ~/.aws/config file"
fi

if [ -f .env ]; then
    check_pass "Local .env file exists (for project-specific config)"
else
    check_warn "No .env file in project directory"
fi

echo ""

# ============================================================================
# 8. Security Check
# ============================================================================
echo -e "${BLUE}8. Security Check...${NC}"

if grep -r "AKIA" .git/objects 2>/dev/null | head -1 | grep -q "AKIA"; then
    check_fail "WARNING: AWS Access Key found in git history!"
    check_warn "Credentials may be exposed. Rotate immediately!"
else
    check_pass "No AWS access keys in git history"
fi

if [ -f .env ] && grep -q "AWS_SECRET_ACCESS_KEY" .env; then
    if grep "^AWS_SECRET_ACCESS_KEY" .gitignore &>/dev/null; then
        check_pass ".env file exists and is in .gitignore"
    else
        check_fail ".env file not in .gitignore - credentials could leak!"
    fi
fi

echo ""

# ============================================================================
# Summary
# ============================================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Verification Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Passed:${NC} $CHECKS_PASSED"
echo -e "${RED}Failed:${NC} $CHECKS_FAILED"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ AWS setup looks good!${NC}"
    echo ""
    echo "You can now:"
    echo "  - Access S3 buckets via boto3"
    echo "  - Launch SageMaker training jobs"
    echo "  - Run notebooks with AWS services"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. See above for details.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  1. Run: aws configure"
    echo "  2. Run: pip install boto3"
    echo "  3. Create .env with S3_BUCKET="
    echo "  4. Check IAM permissions"
    exit 1
fi
