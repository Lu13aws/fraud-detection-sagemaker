# AWS Credentials Management Skill

## Purpose

This skill guides safe, secure management of AWS credentials and IAM roles for machine learning projects.

Use this skill whenever:

* Setting up AWS access for local development
* Configuring SageMaker execution roles
* Working with environment variables and .env files
* Need to rotate or revoke credentials
* Collaborating on AWS projects with teams
* Deploying to production

---

## Core Principles

1. **Never commit credentials to git** — .env files should ALWAYS be in .gitignore
2. **Rotate credentials regularly** — At least quarterly, or after any breach
3. **Least privilege** — IAM roles should have minimum required permissions
4. **Audit access** — Know who has what credentials
5. **Use roles over keys when possible** — SageMaker execution roles > hardcoded keys

---

## The .env File Pattern

### ✅ Correct Setup

**`.env.example` (COMMITTED to git):**
```
# AWS Configuration
AWS_REGION=eu-central-1
S3_BUCKET=raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=eu-central-1

# SageMaker (optional)
SAGEMAKER_ROLE_ARN=arn:aws:iam::ACCOUNT_ID:role/SageMakerRole
SAGEMAKER_EXECUTION_ROLE=arn:aws:iam::ACCOUNT_ID:role/SageMakerRole
```

**`.env` (NOT COMMITTED, local only):**
```
# AWS Configuration
AWS_REGION=eu-central-1
S3_BUCKET=raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an
AWS_ACCESS_KEY_ID=AKIA1234567890ABCDEF
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_DEFAULT_REGION=eu-central-1

SAGEMAKER_ROLE_ARN=arn:aws:iam::759302162548:role/service-role/AmazonSageMakerAdminIAMExecutionRole
SAGEMAKER_EXECUTION_ROLE=arn:aws:iam::759302162548:role/service-role/AmazonSageMakerAdminIAMExecutionRole
```

### `.gitignore` Configuration

**MUST include:**
```
# .gitignore

.env                    # Your local credentials
.env.local
.env.*.local
.env.production.local

# Also exclude AWS credential files
~/.aws
.aws/

# Never commit API keys
*.pem
*.key
api_keys.txt
credentials.json
```

**Verify:**
```bash
# Check that .env is ignored
git status .env

# Should show: fatal: pathspec '.env' did not match any files
# This means git is NOT tracking it ✅
```

---

## Setting Up AWS Credentials

### Method 1: AWS CLI (Recommended)

**Most straightforward for local development:**

```bash
# Install AWS CLI (if needed)
pip install awscli

# Configure credentials interactively
aws configure

# Prompts for:
# AWS Access Key ID: [paste your access key]
# AWS Secret Access Key: [paste your secret key]
# Default region: eu-central-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity

# Output shows: Account ID, ARN, UserId (confirms it works)
```

**Credentials stored in:** `~/.aws/credentials` (automatically)

### Method 2: .env File (For Projects)

**Use when working with multiple projects with different credentials:**

```python
# In your code
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
aws_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
```

**Install required package:**
```bash
pip install python-dotenv
```

### Method 3: Environment Variables (CI/CD)

**For automated deployments (GitHub Actions, Jenkins, etc.):**

```bash
# Set environment variables directly
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=wJalr...
export AWS_REGION=eu-central-1

# Tools automatically read these
python train_model.py  # boto3 will use env vars
```

---

## Creating AWS Access Keys

### Step 1: Go to IAM Console

1. AWS Console → Services → IAM
2. Left menu → "Users"
3. Select your user (or create new)

### Step 2: Create Access Key

1. Tab: "Security credentials"
2. Scroll down: "Access keys"
3. Click: "Create access key"
4. Choose: "Application running outside AWS"
5. Copy: **Access Key ID** and **Secret Access Key**

⚠️ **IMPORTANT:** Save both immediately. Secret key shows only once!

### Step 3: Secure the Keys

```bash
# Create .env file locally
cat > .env << EOF
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJalr...
AWS_REGION=eu-central-1
EOF

# Verify .env not tracked
git status .env
# Should show: not in working tree ✅

# Keep .env in password manager or secure backup
# NEVER paste in Slack, email, or public forums
```

---

## Credential Rotation (Important!)

### When to Rotate

- [ ] Quarterly (every 3 months) — standard practice
- [ ] After suspected breach
- [ ] When someone leaves team
- [ ] After production incident
- [ ] On project completion

### How to Rotate

**Step 1: Create new access key**
```bash
# Go to AWS IAM console
# Users → Your User → Security Credentials
# Create a NEW access key
# Copy both ID and Secret
```

**Step 2: Update local .env**
```bash
# Edit .env with new credentials
AWS_ACCESS_KEY_ID=AKIA_NEW_KEY
AWS_SECRET_ACCESS_KEY=new_secret_key
```

**Step 3: Test new credentials**
```bash
# Verify access works
aws sts get-caller-identity

# Run test S3 command
aws s3 ls s3://your-bucket/
```

**Step 4: Delete old access key**
```bash
# AWS IAM console
# Users → Your User → Security Credentials
# Find old access key → "Delete"
# Confirm deletion
```

**Step 5: Document rotation**
```bash
# Update project documentation
# Example: "Credentials rotated 2025-06-04"

git log --oneline | head -5
# Confirm no credential commits in history
```

---

## SageMaker Execution Roles

### What is a SageMaker Role?

AWS requires an **IAM execution role** for SageMaker to:
- Access S3 buckets
- Write to CloudWatch
- Create endpoints
- Access other AWS services

### Creating a SageMaker Role

**AWS Console approach:**

1. AWS Console → IAM → Roles
2. "Create role"
3. Select: "SageMaker"
4. Attach policy: "AmazonSageMakerFullAccess" (or custom)
5. Name: `AmazonSageMakerAdminIAMExecutionRole`
6. Create

**Terraform approach (recommended):**

```hcl
resource "aws_iam_role" "sagemaker_role" {
  name = "AmazonSageMakerAdminIAMExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "sagemaker.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_policy" {
  role       = aws_iam_role.sagemaker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
```

### Using Role in Code

```python
import sagemaker

# Get execution role
role = sagemaker.get_execution_role()
print(f"Using role: {role}")

# Use in SageMaker estimator
from sagemaker.sklearn.estimator import SKLearn

estimator = SKLearn(
    entry_point='train.py',
    role=role,  # Uses SageMaker execution role
    instance_type='ml.m5.large',
)
```

---

## Security Best Practices

### ✅ DO

- [x] Store credentials in .env (local only)
- [x] Use environment variables in production
- [x] Rotate credentials quarterly
- [x] Use SageMaker roles instead of hardcoded keys
- [x] Grant least privilege (only needed permissions)
- [x] Audit who has access (IAM policy analyzer)
- [x] Use MFA for AWS console access
- [x] Version control project code, NOT credentials
- [x] Use AWS Secrets Manager for production
- [x] Monitor CloudTrail for suspicious activity

### ❌ DON'T

- [ ] Commit .env file to git
- [ ] Hardcode credentials in code
- [ ] Share credentials via email/Slack
- [ ] Use same credentials across projects
- [ ] Leave credentials in git history (even if deleted)
- [ ] Give "admin" access when limited access works
- [ ] Share AWS console password
- [ ] Post screenshots with credentials visible
- [ ] Keep old credentials "just in case"
- [ ] Use root account credentials

---

## Checking for Credential Leaks

### Scenario: Credentials Accidentally Committed

```bash
# Search git history for credentials
git log -p --all -S "AWS_SECRET" | head -20

# Search for access key pattern
git log -p --all | grep -i "AKIA" | head -5

# If found:
# 1. IMMEDIATELY rotate credentials (create new ones)
# 2. Delete old access keys in IAM console
# 3. Use git filter-branch to remove from history (if private repo)
# 4. Document incident
```

### Public Repository Exposure

**If credentials leaked to public repo:**

1. **IMMEDIATELY:**
   - Delete access keys in AWS IAM
   - Create new access keys
   - Update .env locally

2. **Then:**
   - Contact AWS security (support ticket)
   - Review CloudTrail for unauthorized access
   - Rotate all secrets

3. **Prevention:**
   - Use `git secrets` pre-commit hook:
     ```bash
     git clone https://github.com/awslabs/git-secrets.git
     cd git-secrets
     ./install.sh
     
     # Setup for repo
     cd your-repo
     git secrets --install
     git secrets --register-aws
     ```

---

## Environment-Specific Configuration

### Development (Local)

```python
# .env (local, NOT committed)
AWS_REGION=eu-central-1
S3_BUCKET=dev-bucket-id
AWS_ACCESS_KEY_ID=AKIA_DEV_KEY
AWS_SECRET_ACCESS_KEY=dev_secret
```

### Production (CI/CD)

```yaml
# GitHub Actions example
env:
  AWS_REGION: eu-central-1
  S3_BUCKET: ${{ secrets.PROD_BUCKET }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Key difference:** Secrets stored in GitHub Secrets, not .env file.

---

## Verification Checklist

Before starting development:

- [ ] .env file exists locally (NOT committed)
- [ ] .env contains all required keys:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_REGION
  - S3_BUCKET
  - (Optional) SAGEMAKER_ROLE_ARN
- [ ] `.gitignore` includes `.env`
- [ ] Can run: `aws sts get-caller-identity` (confirms access)
- [ ] Can run: `aws s3 ls s3://your-bucket/` (confirms S3 access)
- [ ] No hardcoded credentials in code
- [ ] No credentials in git history: `git log --all | grep -i "AKIA"`
- [ ] Credentials are < 3 months old
- [ ] Team knows about credential storage approach
- [ ] Backup of credentials in secure location (password manager)

---

## Troubleshooting

### "NoCredentialsError"

**Cause:** AWS can't find credentials.  
**Fix:**
```bash
# Check .env exists and is loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('AWS_ACCESS_KEY_ID'))"

# Check AWS CLI credentials
cat ~/.aws/credentials

# Check environment variables
env | grep AWS
```

### "AccessDenied: User is not authorized"

**Cause:** Credentials are valid but don't have permission.  
**Fix:**
1. Check IAM role has required policy
2. Check S3 bucket policy allows access
3. Run: `aws sts get-caller-identity` to see who you are
4. Check IAM policy: `aws iam get-user-policy --user-name <name> --policy-name <policy>`

### "Invalid credentials"

**Cause:** Access key or secret is wrong or expired.  
**Fix:**
1. Verify copy-paste (no extra spaces)
2. Check AWS IAM console — key still exists?
3. Create new access key if old one deleted
4. Rotate credentials (create new key, delete old)

### "Signature does not match"

**Cause:** Credentials swapped or corrupted.  
**Fix:**
```python
# Verify order
import os
print(f"KEY ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
print(f"SECRET: {os.getenv('AWS_SECRET_ACCESS_KEY')[:10]}...")  # Don't print full secret

# Ensure you didn't swap them
# Access Key ID: AKIA...
# Secret Key: wJalr...
```

---

## Summary

| Task | Method | Security |
|------|--------|----------|
| Local dev | .env + aws configure | High (credentials local only) |
| SageMaker | IAM execution role | Highest (no hardcoded keys) |
| Production | GitHub Secrets | Very high (encrypted) |
| Shared credentials | Temporary STS tokens | High (time-limited) |

**Golden Rule:** Credentials are secrets. Treat them like passwords. Never commit, never share, always rotate.
