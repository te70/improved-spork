# 🔐 DevSecOps Security Pipeline

A GitHub Actions CI/CD pipeline that runs automated security checks
at every code commit — SAST, dependency scanning, container image
scanning, and secrets detection.

## Pipeline Overview

Every push to `main` or `develop`, and every pull request to `main`,
triggers the full security pipeline:

| Stage | Tool | What it checks |
|---|---|---|
| 🔑 Secrets Detection | Gitleaks | Hardcoded API keys, passwords, tokens in code history |
| 🔍 SAST | Bandit | Python source code vulnerabilities (injection, weak crypto, etc.) |
| 📦 Dependency Scan | Safety + pip-audit | Known CVEs in Python packages |
| 🐳 Container Scan | Trivy | OS and library vulnerabilities in the Docker image |
| 🧪 Unit Tests | pytest | Functional correctness |

## Security Gates

The pipeline blocks merges on:
- Any leaked secret detected by Gitleaks
- HIGH severity Bandit findings in application code
- CRITICAL vulnerabilities in the container image
- Failing unit tests

## Viewing Results

All security findings are available in three places:

1. **GitHub Security tab** → Code scanning alerts
   (uploaded as SARIF from every tool)

2. **Pipeline summary** → Each run shows a pass/fail table
   for all security gates

3. **Artifacts** → Full JSON/SARIF reports downloadable
   from each pipeline run

## Running Locally

```bash
# Install tools
pip install bandit safety pip-audit

# SAST scan
bandit --recursive app/ --severity-level medium

# Dependency scan
safety check --file requirements.txt
pip-audit --requirement requirements.txt

# Secrets scan (requires gitleaks installed)
gitleaks detect --config .gitleaks.toml --verbose

# Container scan (requires trivy and Docker)
docker build -t myapp:local .
trivy image myapp:local