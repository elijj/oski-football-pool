# 🔒 Security Guidelines

This document outlines security practices and pre-commit hooks for the Football Pool Domination System.

## 🛡️ Pre-commit Security Hooks

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Test all files (run once after setup)
pre-commit run --all-files
```

### Security Checks Included

#### 🔍 **Secret Detection**
- **detect-secrets**: Scans for API keys, passwords, tokens
- **trufflehog**: Advanced secret scanning with entropy detection
- **Custom hooks**: Check for hardcoded credentials in code

#### 🛡️ **Vulnerability Scanning**
- **bandit**: Python security linter
- **safety**: Dependency vulnerability scanning
- **Large file detection**: Prevents accidental commits of large files

#### 📝 **Code Quality**
- **black**: Code formatting
- **isort**: Import sorting
- **ruff**: Fast Python linting
- **flake8**: Additional code quality checks

#### 🚫 **File Protection**
- Database files (`.db`, `.sqlite*`)
- Environment files (`.env`)
- API cache files
- Log files and temporary data

## 🔧 Configuration Files

- `.pre-commit-config.yaml` - Main pre-commit configuration
- `.trufflehog.yaml` - Secret scanning configuration
- `.secrets.baseline` - Known safe patterns

## 🚨 Security Best Practices

### ✅ **DO:**
- Use environment variables for API keys
- Keep `.env` files in `.gitignore`
- Use `.env.example` for documentation
- Regular dependency updates
- Run security scans before commits

### ❌ **DON'T:**
- Commit API keys or secrets
- Commit database files
- Commit `.env` files
- Use hardcoded credentials
- Skip security checks

## 🔄 Updating Hooks

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Run hooks on all files
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

## 📊 Security Reports

- `bandit-report.json` - Security vulnerability report
- Pre-commit output shows real-time security issues

## 🆘 Troubleshooting

### Hook Failures
```bash
# Run specific hook
pre-commit run <hook-id>

# Skip specific hook
SKIP=<hook-id> git commit
```

### Common Issues
- **Large files**: Add to `.gitignore` or use Git LFS
- **False positives**: Update `.secrets.baseline`
- **Performance**: Hooks run in parallel by default

## 📞 Support

For security concerns or hook issues, check:
1. Pre-commit documentation
2. Individual tool documentation
3. Project README for setup instructions
