# OWASP Top 10:2025 Security Checklist

For each category, search the codebase using the grep patterns listed. When a pattern matches,
read the surrounding code (10-20+ lines) to determine if it is a true positive.

---

## A01:2025 — Broken Access Control

**What to look for:**
- Missing authorization checks on sensitive endpoints or routes
- Direct object references without ownership validation (IDOR)
- Path traversal in file operations (../ sequences)
- CORS misconfiguration (wildcard origins)
- Missing function-level access control (regular user accessing admin routes)
- Metadata/parameter manipulation to bypass access checks

**Grep patterns:**
```
# Missing auth middleware on routes
"app.get\(|app.post\(|app.put\(|app.delete\(|app.patch\("  (then check for missing auth middleware)
"@app.route|@router" (Python — check for missing @login_required)
"Route\(|MapRoute|endpoints.Map" (.NET — check for missing [Authorize])

# IDOR — direct DB lookup by user-supplied ID without ownership check
"findById|find_by_id|FindByID|.get\(.*id|.find\(.*params"

# Path traversal
"\.\./|\.\.\\\\|path\.join.*req\.|os\.path\.join.*request"

# CORS wildcard
"Access-Control-Allow-Origin.*\*|cors\(\{.*origin.*true|AllowAnyOrigin"
```

---

## A02:2025 — Security Misconfiguration

**What to look for:**
- Debug mode enabled in production configuration
- Default credentials or accounts still active
- Unnecessary features/services enabled
- Missing security headers
- Overly permissive error handling exposing internals
- Directory listing enabled
- Unnecessary HTTP methods enabled

**Grep patterns:**
```
# Debug mode
"DEBUG\s*=\s*True|debug:\s*true|NODE_ENV.*development|app\.debug|EnableDetailedErrors"

# Default credentials
"admin:admin|password123|default.*password|test.*password|changeme|P@ssw0rd"

# Missing security headers (check if these are set somewhere)
"X-Content-Type-Options|X-Frame-Options|Strict-Transport-Security|Content-Security-Policy"

# Verbose error exposure
"stack.*trace|stackTrace|showDetailedErrors|app\.use.*errorHandler"
```

---

## A03:2025 — Software Supply Chain Failures

**What to look for:**
- Missing lock files (package-lock.json, yarn.lock, Pipfile.lock, Cargo.lock, Gemfile.lock)
- Unpinned dependency versions (using *, latest, or very broad ranges)
- Dependencies from untrusted or unusual sources
- Build scripts that download and run external code without verification
- Missing subresource integrity (SRI) on CDN includes
- CI/CD pipeline without integrity verification steps

**Grep patterns:**
```
# Unpinned versions in package.json
'"\\*"|"latest"|">=|">\\d'

# Downloading and running scripts without verification
"curl.*\|.*sh|curl.*\|.*bash|wget.*\|.*sh|wget.*\|.*bash"

# Missing SRI on external scripts/stylesheets
(check for external CDN resources without integrity attribute)

# Post-install scripts (potential supply chain vector)
'"preinstall"|"postinstall"|"prepare"'
```

---

## A04:2025 — Cryptographic Failures

**What to look for:**
- Sensitive data transmitted in cleartext (HTTP instead of HTTPS)
- Weak hashing algorithms for passwords or security tokens
- Hardcoded cryptographic keys or secrets
- Missing encryption for sensitive data at rest
- Deprecated or weak TLS versions
- Insufficient key lengths

**Grep patterns:**
```
# Weak hashing
"md5\(|MD5\.|sha1\(|SHA1\.|hashlib\.md5|hashlib\.sha1|DigestUtils\.md5"

# Hardcoded keys/secrets
'secret.*=.*"|key.*=.*"|password.*=.*"|token.*=.*"'
"PRIVATE.KEY|BEGIN RSA|BEGIN EC|BEGIN DSA"

# HTTP URLs for sensitive operations (excluding localhost)
'http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)'

# Weak TLS
"SSLv2|SSLv3|TLSv1\.0|TLSv1\.1"
```

---

## A05:2025 — Injection

**What to look for:**
- SQL queries built with string concatenation or interpolation
- NoSQL query construction with user input
- OS command construction with user input
- LDAP query construction with user input
- Template injection (user input in template strings)
- Cross-site scripting (user input rendered without encoding)
- Header injection

**Grep patterns:**
```
# SQL injection
'query\(.*\+|query\(.*\$\{|query\(.*%s|query\(.*format\('
"SELECT.*\+.*req\.|INSERT.*\+.*req\.|UPDATE.*\+.*req\.|DELETE.*\+.*req\."
'\.raw\(|\.extra\(|\.rawQuery\(|RawSQL'

# Command injection
"os\.system\(|subprocess\.call\(|Runtime\.getRuntime\(\)"
"popen\(|system\(|passthru\(|shell_exec\("

# Cross-site scripting sinks
"innerHTML|outerHTML|document\.write|v-html|ng-bind-html"
Search for React's dangerously-set-inner-HTML prop usage
Search for template engines rendering raw/unescaped output (|safe, |raw, {!! !!})

# Template injection
"render_template_string|Template\(.*request|Jinja2.*from_string"
```

---

## A06:2025 — Insecure Design

**What to look for:**
- Missing rate limiting on critical flows (login, registration, password reset)
- No abuse case handling (e.g., unlimited account creation)
- Missing CAPTCHA on public forms
- Business logic flaws (e.g., negative quantities, race conditions)
- Missing transaction isolation for concurrent operations
- No limit on failed authentication attempts

**Grep patterns:**
```
# Missing rate limiting indicators
"login|signin|sign_in|authenticate|reset.*password|forgot.*password|register|signup|sign_up"
(then check if rate limiting middleware/decorator is applied)

# Race condition indicators
"balance|credit|stock|inventory|quantity|amount|transfer|withdraw"
(then check if proper locking/transactions are used)
```

---

## A07:2025 — Authentication Failures

**What to look for:**
- Weak password policies (no minimum length, complexity requirements)
- Credential stuffing exposure (no account lockout, no rate limiting)
- Default or weak session configuration
- Insecure password recovery mechanisms
- Missing multi-factor authentication on sensitive operations
- Plaintext password storage or transmission
- Session tokens in URLs

**Grep patterns:**
```
# Weak password validation
"password.*length.*[1-5][^0-9]|minlength.*[1-5][^0-9]|min_length.*[1-5]"

# Plaintext password handling
"password.*==|password.*===|password.*\.equals\("
(should be using bcrypt/argon2/scrypt comparison, not direct equality)

# Session issues
"session.*secret.*=|SESSION_SECRET.*=|cookie.*secure.*false|httpOnly.*false"
```

---

## A08:2025 — Software and Data Integrity Failures

**What to look for:**
- Insecure deserialization of untrusted data
- CI/CD pipeline without integrity verification
- Auto-update mechanisms without signature validation
- Unsigned or unverified data from external sources used in critical operations

**Grep patterns:**
```
# Insecure deserialization
"yaml\.load\((?!.*Loader)|yaml\.unsafe_load|ObjectInputStream|readObject\(\)|unserialize\("
"Marshal\.load|Marshal\.restore"

# Unverified external data used in critical operations
"fetch\(.*\.then.*JSON|axios.*\.then|requests\.get.*\.json\(\)"
(check if response data is validated before use in security-critical logic)
```

---

## A09:2025 — Security Logging and Alerting Failures

**What to look for:**
- Missing audit logs for security events (login, access denied, data changes)
- Sensitive data written to logs (passwords, tokens, PII)
- Missing alerting on suspicious activity
- Log injection vulnerabilities
- Insufficient logging of authentication events

**Grep patterns:**
```
# Sensitive data in logs
"log.*password|log.*token|log.*secret|log.*key|log.*credit|log.*ssn|log.*api_key"
"console\.log.*password|console\.log.*token|console\.log.*secret"
"logger.*password|logger.*token|logger.*secret|logging.*password"

# Missing security event logging (check if login/auth functions have logging)
"login|authenticate|authorize|access.denied|permission.denied|forbidden"
```

---

## A10:2025 — Mishandling of Exceptional Conditions

**What to look for:**
- Empty catch blocks that swallow errors silently
- Generic exception handling that hides specific error types
- Fail-open patterns (defaulting to allow on error)
- Unhandled promise rejections
- Missing error boundaries in frontend applications
- Error handling that exposes sensitive information

**Grep patterns:**
```
# Empty catch blocks
"catch\s*\([^)]*\)\s*\{\s*\}|except:\s*pass|except\s+Exception.*:\s*pass|rescue\s*=>\s*nil"

# Fail-open patterns
"catch.*return true|catch.*allow|catch.*grant|rescue.*return true"

# Overly broad exception handling
"catch\s*\(Exception|catch\s*\(Error|except Exception|except:\s*$|rescue\s*$"
```
