# Configuration Security Checklist

Treat configuration heuristics as leads, not automatic findings. When a control appears to be
missing, verify the effective application, web server, container, or CI configuration inside the
scanned project before reporting it.

## 1. Secrets in Source Code

Search for credentials, keys, and tokens committed to the repository.

**Grep patterns:**

```
# AWS credentials
"AKIA[0-9A-Z]{16}"
"aws_secret_access_key|aws_access_key_id"

# Generic API keys and tokens
"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9]"
"api[_-]?secret\s*[:=]\s*['\"]"
"auth[_-]?token\s*[:=]\s*['\"]"
"bearer\s+[A-Za-z0-9\-._~+/]+=*"

# Private keys
"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"

# Database connection strings with embedded credentials
"mongodb(\+srv)?://[^:]+:[^@]+@"
"postgres(ql)?://[^:]+:[^@]+@"
"mysql://[^:]+:[^@]+@"
"mssql://[^:]+:[^@]+@"
"redis://:[^@]+@"

# Password assignments
"password\s*[:=]\s*['\"][^'\"]{3,}"
"passwd\s*[:=]\s*['\"][^'\"]{3,}"
"pwd\s*[:=]\s*['\"][^'\"]{3,}"

# Webhook and signing secrets
"webhook[_-]?secret|signing[_-]?secret|client[_-]?secret"

# Stripe, SendGrid, Twilio, etc.
"sk_(live|test)_[A-Za-z0-9]{20,}"
"SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}"
"TWILIO|twilio.*sid|twilio.*token"

# Slack tokens
"xox[bporas]-[0-9]"

# GitHub tokens
"gh[pousr]_[A-Za-z0-9_]{36,}"
```

**Important:** Exclude test fixtures, example configs, and documentation from findings.
Only flag secrets that appear to be real. Ignore obvious placeholders and training values such as:
- `example`, `sample`, `dummy`, `fake`, `test`, `placeholder`
- `xxx`, `xxxx`, `changeme`, `replace-me`, `your-key-here`, `your-secret-here`
- docs, fixtures, seed data, mock servers, and tutorial snippets unless the repo actually loads them in production paths
- generated templates such as `.env.example`, `.env.sample`, `config.example.*`, or README snippets unless they contain what appears to be a real active credential

When in doubt, verify whether the value is referenced by live application config, CI, or deployment code before reporting it.

---

## 2. Environment File Exposure

**Checks:**
- Is `.env` listed in `.gitignore`? If not, it may be committed to the repo.
- Does `.env.example` or `.env.sample` contain real values instead of placeholders?
- Are there `.env.production`, `.env.staging` files with real secrets?
- Docker Compose files with secrets in `environment:` blocks instead of Docker secrets.
- Kubernetes manifests with secrets in plain YAML (should use Sealed Secrets or external secret managers).

**Grep patterns:**
```
# Check .gitignore for .env
Glob: **/.gitignore (then check if .env is listed)

# Env files that might be committed
Glob: **/.env, **/.env.production, **/.env.staging, **/.env.local

# Docker compose secrets in plaintext
"environment:" followed by lines with "PASSWORD|SECRET|KEY|TOKEN"

# K8s secrets in plain YAML
"kind:\s*Secret" with "stringData:|data:" (check if base64 encoded values are real secrets)
```

---

## 3. Debug Mode & Development Settings

**What to check:**
- Production configs with debug mode enabled
- Development-only middleware active in production
- Profiling or debugging tools exposed
- Verbose SQL query logging in production
- Source maps deployed to production

**Grep patterns:**
```
# Debug flags
"DEBUG\s*=\s*True|DEBUG\s*=\s*true|debug:\s*true|'debug'\s*:\s*true"
"NODE_ENV.*development|FLASK_ENV.*development|RAILS_ENV.*development"
"app\.debug\s*=\s*True|EnableDetailedErrors"

# Development middleware in production
"morgan\('dev'\)|django\.contrib\.admin|debug_toolbar|Debugbar|web-vitals"

# Source maps
Glob: **/*.map, **/sourceMappingURL
```

---

## 4. Security Headers

**Check whether the effective application or web server configuration sets these headers.**
Only report missing headers when neither the app nor the in-repo proxy/server config sets them
for the deployed surface you are auditing.

| Header | Purpose | Risk if Missing |
|--------|---------|-----------------|
| `Content-Security-Policy` | Prevents XSS and data injection | XSS attacks |
| `Strict-Transport-Security` | Forces HTTPS | Downgrade attacks |
| `X-Content-Type-Options: nosniff` | Prevents MIME sniffing | Content type attacks |
| `X-Frame-Options` | Prevents clickjacking | UI redressing |
| `Referrer-Policy` | Controls referrer information | Information leakage |
| `Permissions-Policy` | Controls browser features | Feature abuse |

**Where to search:**
- Middleware configuration (Express helmet, Django middleware, Spring Security)
- Web server config (nginx.conf, apache .htaccess, web.config)
- Response interceptors or global headers setup

---

## 5. CORS Configuration

**Grep patterns:**
```
# Overly permissive CORS
"Access-Control-Allow-Origin.*\*"
"cors\(\{.*origin.*true|cors\(\{.*origin.*\*"
"AllowAnyOrigin|allowedOrigins.*\*|CorsRegistry.*addMapping.*\*"

# Credentials with wildcard (dangerous combination)
"Access-Control-Allow-Credentials.*true" (combined with wildcard origin)
```

---

## 6. Cookie Security

**Check cookie settings:**
```
# Missing Secure flag
"cookie.*secure\s*[:=]\s*false|Secure\s*=\s*false"

# Missing HttpOnly flag
"cookie.*httpOnly\s*[:=]\s*false|httponly\s*[:=]\s*false|HttpOnly\s*=\s*false"

# Missing SameSite
"SameSite\s*=\s*None|sameSite\s*[:=]\s*'none'|sameSite\s*[:=]\s*\"none\""
(without `Secure` on an auth or session cookie this is a real vulnerability; verify cookie purpose before reporting)
```

---

## 7. CI/CD Pipeline Security

**Check for:**
- Secrets hardcoded in CI config files (.github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile)
- Overly permissive GitHub Actions permissions (permissions: write-all)
- Third-party actions using branch references instead of SHA pinning
- Auto-merge without review requirements
- Missing branch protection indicators

**Grep patterns:**
```
# Secrets in CI configs
Glob: **/.github/workflows/*.yml, **/.gitlab-ci.yml, **/Jenkinsfile, **/azure-pipelines.yml

# Overly permissive permissions
"permissions:.*write-all|permissions:.*contents:.*write"

# Unpinned actions
"uses:.*@(main|master|latest|v[0-9]+$)"
(should use SHA: uses: actions/checkout@a1b2c3d)
```

---

## 8. Infrastructure Configuration

**Docker security checks:**
```
# Running as root
"USER root|user:\s*root" in Dockerfiles
(absence of `USER` is evidence the image defaults to root; verify the Dockerfile is part of the deployed build before reporting)

# Exposing unnecessary ports
"EXPOSE" (check if all exposed ports are necessary)

# Using latest tag
"FROM.*:latest|FROM.*(?!.*:)" (missing specific version tag)
```

**Terraform/IaC checks:**
```
# Overly permissive security groups
"0\.0\.0\.0/0|::/0" in security group ingress rules

# Public S3 buckets
"acl.*public|block_public_access.*false"

# Unencrypted storage
"encrypted\s*=\s*false|storage_encrypted\s*=\s*false"
```
