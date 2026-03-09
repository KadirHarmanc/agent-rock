# Data Flow Verification Protocol

Use this reference during Phase 2 analysis to verify whether a grep hit represents
a true vulnerability. This protocol reduces false positives by requiring concrete
evidence of an exploitable data flow before reporting a finding.

---

## The 3-Pass Verification Process

### Pass 1: Source Identification

Identify where the potentially tainted data originates.

**User-controlled sources (external input):**
- HTTP Request Data: request.params, request.query, request.body, request.headers, cookies
- File/Upload Input: request.files, multipart form data
- WebSocket/Event Data: ws.receive(), event.data
- URL/Navigation: window.location, document.URL, document.referrer
- External Systems: API responses, message queue payloads

**Non-user-controlled (typically safe sources):**
- Hardcoded constants and config values
- Auto-generated IDs (UUIDs, auto-increment)
- System timestamps
- Framework-generated CSRF tokens
- Internally computed values with no user input chain

### Pass 2: Sink Verification

Confirm the data reaches a dangerous sink without adequate transformation.

**Dangerous sinks by category:**

| Category | Sinks |
|----------|-------|
| SQL Injection | Database query functions with string interpolation |
| Command Injection | Shell/process invocation with string-form arguments |
| XSS | DOM manipulation APIs that accept raw HTML (see frontend-security.md) |
| Path Traversal | File open/read/write functions with user-controlled path |
| SSRF | HTTP client functions with user-controlled URL |
| Deserialization | Unsafe deserializers on untrusted input (see ai-ml-security.md) |
| Template Injection | Template rendering functions with user input in template string |
| Code Injection | Dynamic code evaluation functions with user data |
| Redirect | Navigation/redirect functions with user-controlled URL |

### Pass 3: Sanitization Check

Verify whether the data is sanitized, validated, or transformed between source and sink.

**Check for these protections in order:**

1. **Framework auto-protection**
   - ORM parameterized queries (see safe-patterns.md)
   - Template engine auto-escaping
   - Framework middleware (CSRF, auth, input validation)

2. **Explicit validation**
   - Input validation (type checking, regex, allowlist)
   - Schema validation (Pydantic, Joi, Zod, JSON Schema)
   - Length/range limits

3. **Explicit sanitization**
   - Output encoding/escaping (HTML, URL, SQL, shell)
   - Sanitizer libraries (DOMPurify, bleach)
   - Path canonicalization + prefix checking

4. **Architectural protection**
   - Auth middleware on the route
   - Rate limiting
   - WAF/proxy-level filtering (note: external, lower confidence)

---

## Decision Matrix

After completing all 3 passes, classify the finding:

| Source | Reaches Sink? | Sanitized? | Classification |
|--------|--------------|-----------|---------------|
| User-controlled | Yes | No | **Confirmed Finding** (High confidence) |
| User-controlled | Yes | Partially | **Confirmed Finding** (Medium confidence) |
| User-controlled | Yes | Yes, properly | **Not a finding** (discard) |
| User-controlled | Unclear | No | **Confirmed Finding** (Low confidence) — note assumptions |
| Non-user-controlled | Yes | No | **Not a finding** unless source can be tainted indirectly |
| User-controlled | No | N/A | **Not a finding** (discard) |

---

## Verification Workflow Example

**Grep hit:** SQL query with f-string interpolation

**Pass 1 — Source:**
Read the function to find where the variable comes from.
Is it from request.args, request.body, URL parameter, or other user input?

**Pass 2 — Sink:**
Is it a database query, shell command, DOM manipulation, or other dangerous sink?

**Pass 3 — Sanitization:**
- Is the query parameterized?
- Is input validation applied?
- Is an ORM used?

**Result:** If user-controlled, reaches dangerous sink, and no sanitization → Confirmed finding.

---

## Multi-File Data Flow Tracing

When the source and sink are in different files:

1. **Start from the sink** (the grep hit)
2. **Trace the parameter** — what function argument feeds the sink?
3. **Find callers** — search for the function name to find who calls it
4. **Read caller context** — does the caller pass user input?
5. **Repeat** until you reach a source or confirm the chain is internal-only

**Limit:** Trace up to 3 hops (caller to caller to caller). Beyond 3 hops, confidence
drops to Low and the finding should note the assumption.

---

## Common Verification Shortcuts

### Quick Confirm (likely true positive)
- Dynamic code evaluation with request data
- OS command functions with user-controlled string arguments
- Deserializing untrusted uploaded files
- Hardcoded password/key in source code — no data flow needed

### Quick Reject (likely false positive)
- ORM query method with typed parameter — framework handles escaping
- React JSX expressions with user data — auto-escaped by React
- Subprocess with array-form arguments — no shell interpretation
- Test/mock files — not production code
- Comments containing dangerous patterns — not executed
- String constants defining error messages — not user input

---

## Important Notes

1. **Read enough context.** Minimum 20 lines around the grep hit.
2. **Do not assume safety.** A validator elsewhere does not mean it covers this flow.
3. **Check the framework version.** Some protections were added in specific versions.
4. **Note your assumptions.** If you cannot fully trace the flow, set confidence to Low or Medium.
