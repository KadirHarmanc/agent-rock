# Safe Patterns & Sanitizer Catalog

Use this reference during verification (Phase 2) to identify framework-provided
safety mechanisms. When a grep hit matches a dangerous pattern but the surrounding
code uses a recognized safe pattern, it is likely a false positive.

**Purpose:** Reduce false positive rate by documenting known-safe coding patterns
and built-in framework protections.

---

## General Principle

A pattern is "safe" when:
1. The framework guarantees the protection by default (opt-out, not opt-in)
2. The sanitizer/escaper is applied at the correct point in the data flow
3. The protection cannot be trivially bypassed by the developer

Always verify that the safe pattern is **actually applied** to the specific data flow
you are investigating, not just present elsewhere in the codebase.

---

## SQL Injection Safe Patterns

### Parameterized Queries (All Languages)
```
# Safe — parameterized
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
db.query("SELECT * FROM users WHERE id = $1", [userId])
stmt.setString(1, userId)

# Unsafe — string interpolation
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### ORM Safe-by-Default
| Framework | Safe Pattern | Still Verify |
|-----------|-------------|-------------|
| SQLAlchemy | `session.query(User).filter(User.id == uid)` | `.filter(text(f"..."))` is NOT safe |
| Django ORM | `User.objects.filter(id=uid)` | `.raw()` and `.extra()` are NOT safe |
| ActiveRecord | `User.where(id: uid)` | `.where("id = #{uid}")` is NOT safe |
| Prisma | `prisma.user.findUnique({ where: { id } })` | `$queryRaw` is NOT safe |
| Sequelize | `User.findOne({ where: { id } })` | `sequelize.query()` with replacements needs verification |
| TypeORM | `repo.findOne({ where: { id } })` | `.query()` is NOT safe |
| Eloquent | `User::where('id', $id)->first()` | `DB::raw()` and `whereRaw()` are NOT safe |
| Entity Framework | `context.Users.Where(u => u.Id == id)` | `FromSqlRaw()` needs parameterization check |

---

## XSS Safe Patterns

### Framework Auto-Escaping
| Framework | Default Behavior | Bypass to Watch For |
|-----------|-----------------|-------------------|
| React JSX | Auto-escapes `{}` expressions | `dangerouslySetInnerHTML` |
| Vue templates | Auto-escapes `{{ }}` | `v-html` |
| Angular | Auto-sanitizes bindings | `bypassSecurityTrustHtml()` |
| Svelte | Auto-escapes `{}` | `{@html}` |
| Django templates | Auto-escapes `{{ }}` | `{{ var\|safe }}`, `{% autoescape off %}` |
| Jinja2 | Auto-escapes if enabled | `{{ var\|safe }}`, `Markup()` |
| ERB | `<%= %>` escapes by default | `<%== %>` or `raw()` |
| Go html/template | Auto-escapes | `template.HTML()` type cast |
| Blade (Laravel) | `{{ }}` escapes | `{!! !!}` |
| Thymeleaf | `th:text` escapes | `th:utext` |

### Sanitizer Libraries
| Library | Language | Safe When |
|---------|----------|-----------|
| DOMPurify | JS | `.sanitize(input)` before DOM insertion |
| bleach | Python | `bleach.clean(input)` with allowed tags |
| sanitize-html | JS | Applied before rendering |
| Rails ActionView | Ruby | `sanitize()` helper |
| HtmlSanitizer | C# | `.Sanitize(input)` |

---

## CSRF Safe Patterns

| Framework | Built-in Protection | Verify |
|-----------|-------------------|--------|
| Django | `{% csrf_token %}` + `CsrfViewMiddleware` | Not disabled via `@csrf_exempt` |
| Rails | `protect_from_forgery` in ApplicationController | Not skipped via `skip_before_action` |
| Laravel | `@csrf` in forms + `VerifyCsrfToken` middleware | Route not in `$except` array |
| Spring | CSRF enabled by default in Spring Security | Not `.csrf().disable()` |
| Express | `csurf` or `csrf-csrf` middleware | Applied to state-changing routes |
| Next.js | Server Actions have built-in CSRF | API Routes need manual protection |
| FastAPI | No built-in — needs manual implementation | Check for custom CSRF middleware |

---

## Authentication Safe Patterns

### Password Hashing
| Algorithm | Status | Notes |
|-----------|--------|-------|
| bcrypt | Safe | Industry standard, work factor >= 10 |
| scrypt | Safe | Memory-hard |
| Argon2id | Safe | Preferred, memory + time hard |
| PBKDF2 (>= 600K iterations) | Acceptable | NIST recommended minimum |
| SHA-256/512 with salt | Weak | Not suitable for passwords |
| MD5, SHA-1 | Unsafe | Never use for passwords |

### Session Management
| Pattern | Safe When |
|---------|-----------|
| `httpOnly: true` | Cookie not accessible via JS |
| `secure: true` | Cookie only sent over HTTPS |
| `sameSite: 'strict'` or `'lax'` | CSRF protection via cookies |
| Session rotation on login | Prevents session fixation |
| Absolute + idle timeout | Limits session lifetime |

---

## Command Injection Safe Patterns

| Pattern | Language | Why Safe |
|---------|----------|----------|
| `subprocess.run([cmd, arg1])` | Python | Array form prevents shell injection |
| `execFile(cmd, [args])` | Node.js | No shell interpretation |
| `ProcessBuilder` | Java | Array form, no shell |
| `exec.Command(name, args...)` | Go | No shell by default |
| `system(cmd, arg1)` (array form) | Ruby | Array form bypasses shell |
| `escapeshellarg()` + `escapeshellcmd()` | PHP | Escaping, but array form preferred |

**Still unsafe even with array form:**
- User input as the command name itself (not just arguments)
- `shell=True` in Python's subprocess
- `child_process.exec()` in Node.js (always uses shell)

---

## Path Traversal Safe Patterns

| Pattern | Language | Why Safe |
|---------|----------|----------|
| `os.path.basename(user_input)` | Python | Strips directory components |
| `path.basename(userInput)` | Node.js | Strips directory components |
| `realpath()` + prefix check | All | Resolves symlinks, then validates |
| `send_file` with `safe_join` | Flask | Validates path is within root |
| `ActiveStorage` | Rails | Managed file storage |
| `Storage::disk()->path()` | Laravel | Managed path resolution |

**Verification needed:**
- `os.path.join(base, user_input)` is NOT safe (allows `../`)
- `path.join(base, userInput)` is NOT safe
- Always check: resolve → canonicalize → verify prefix

---

## Deserialization Safe Patterns

| Instead Of | Use | Language |
|-----------|-----|----------|
| `pickle.load` | `json.loads`, `safetensors` | Python |
| `yaml.load(Loader=Loader)` | `yaml.safe_load()` | Python |
| `ObjectInputStream` | JSON, Protocol Buffers | Java |
| `unserialize()` | `json_decode()` | PHP |
| `Marshal.load` | `JSON.parse` | Ruby |
| `BinaryFormatter` | `System.Text.Json` | C# |

---

## How to Use This Reference

When you find a grep hit for a dangerous pattern:

1. **Check surrounding context** — Is a safe pattern applied?
2. **Verify the safe pattern covers this specific data flow** — not just present in the file
3. **Check for bypasses** — Is the developer using the framework's escape hatch?
4. **If safe pattern confirmed** → discard as false positive
5. **If safe pattern partially applied or bypassed** → report with reduced confidence
6. **If no safe pattern** → report as finding
