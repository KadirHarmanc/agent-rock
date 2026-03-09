# Frontend Security Reference

Use this reference when the project includes frontend code (React, Vue, Angular, Svelte,
vanilla JS/TS, or any browser-targeted code). Frontend vulnerabilities are distinct from
server-side issues and require browser-specific threat modeling.

## Detection

Frontend code is present when you see:
- React: `react`, `react-dom` in package.json; `.jsx`/`.tsx` files
- Vue: `vue` in package.json; `.vue` files
- Angular: `@angular/core` in package.json
- Svelte: `svelte` in package.json; `.svelte` files
- Vanilla: HTML files with `<script>` tags, standalone JS/TS targeting browsers

---

## Category 1: DOM-Based XSS

### Dangerous Sinks
```
Grep: innerHTML
Grep: outerHTML
Grep: document\.write
Grep: insertAdjacentHTML
Grep: dangerouslySetInnerHTML
Grep: v-html
Grep: \[innerHTML\]
Grep: \{@html
```

### Dangerous Sources
```
Grep: location\.(hash|search|href|pathname)
Grep: document\.(URL|documentURI|referrer|cookie)
Grep: window\.(name|postMessage)
Grep: URLSearchParams
Grep: decodeURIComponent
```

Check:
- User-controlled values flowing from sources to sinks without sanitization
- URL parameters rendered directly into DOM
- `eval()`, `Function()`, `setTimeout(string)`, `setInterval(string)` with user input
- Dynamic script creation: `document.createElement('script')` with user-controlled `src`
- jQuery `.html()`, `.append()` with unsanitized user content
- Template literal injection in tagged templates

### Framework-Specific

**React:**
- `dangerouslySetInnerHTML` with user-controlled `__html`
- `ref.current.innerHTML = userInput`
- JSX expressions are auto-escaped, but `href="javascript:..."` is not

**Vue:**
- `v-html` with user-controlled content
- `:href` or `:src` with `javascript:` protocol
- Template compilation from user input (`Vue.compile()`)

**Angular:**
- `bypassSecurityTrustHtml()` with user input
- `[innerHTML]` binding (Angular sanitizes by default, but bypass is common)
- `ElementRef.nativeElement.innerHTML`

---

## Category 2: postMessage Security

```
Grep: postMessage\(
Grep: addEventListener.*message
Grep: onmessage
Grep: event\.origin
Grep: event\.data
```

Check:
- `postMessage` with `"*"` target origin (data sent to any window)
- Message event listeners without `event.origin` validation
- Trusting `event.data` without schema validation
- Executing code or navigating based on message content
- Cross-origin iframe communication without origin allowlist

---

## Category 3: Client-Side Storage

```
Grep: localStorage\.(set|get)Item
Grep: sessionStorage\.(set|get)Item
Grep: document\.cookie
Grep: IndexedDB|indexedDB\.open
```

Check:
- Tokens, passwords, PII stored in `localStorage` (accessible to XSS)
- Session tokens in `localStorage` instead of `httpOnly` cookies
- Sensitive data in `sessionStorage` (survives tab navigation)
- Missing encryption for sensitive cached data
- Cookies without `Secure`, `HttpOnly`, `SameSite` flags (set client-side)
- No storage cleanup on logout

---

## Category 4: Content Security Policy (CSP)

```
Grep: Content-Security-Policy
Grep: content="default-src
Grep: nonce=
Grep: unsafe-inline
Grep: unsafe-eval
```

Check:
- Missing CSP header entirely
- `unsafe-inline` in `script-src` (defeats XSS protection)
- `unsafe-eval` in `script-src` (allows `eval()`)
- Wildcard `*` in `script-src` or `default-src`
- Missing `frame-ancestors` (clickjacking)
- `data:` or `blob:` in `script-src` (bypass vectors)
- CSP report-only mode in production without enforcement
- Nonce reuse across requests

---

## Category 5: iframe & Embedding Security

```
Grep: <iframe
Grep: sandbox=
Grep: X-Frame-Options
Grep: frame-ancestors
Grep: allow=
```

Check:
- Iframes loading user-controlled URLs
- Missing `sandbox` attribute on third-party iframes
- `sandbox` with `allow-scripts allow-same-origin` (defeats sandboxing)
- Missing `X-Frame-Options` or `frame-ancestors` (allows clickjacking)
- `allow` attribute granting unnecessary permissions (camera, microphone, etc.)

---

## Category 6: Third-Party Script Risks

```
Grep: <script.*src=.*http
Grep: integrity=
Grep: crossorigin
Grep: cdn\.|unpkg\.|jsdelivr\.
Grep: gtag|analytics|segment|hotjar|intercom
```

Check:
- External scripts loaded without `integrity` (SRI) attribute
- Missing `crossorigin` attribute on cross-origin scripts
- CDN-loaded libraries that could be compromised
- Analytics/tracking scripts with excessive permissions
- Dynamic script injection from third-party SDKs
- No CSP restricting script sources

---

## Category 7: Service Worker & PWA Security

```
Grep: serviceWorker\.register
Grep: navigator\.serviceWorker
Grep: self\.addEventListener.*fetch
Grep: CacheStorage|caches\.open
Grep: importScripts
```

Check:
- Service worker registered from different origin
- `importScripts` loading unvalidated URLs
- Cache containing sensitive data (tokens, PII) without expiry
- Fetch event handler proxying requests without validation
- Missing scope restriction on service worker registration
- Service worker update mechanism not using HTTPS

---

## Category 8: Open Redirect & Navigation

```
Grep: window\.location\s*=
Grep: location\.href\s*=
Grep: location\.replace\(
Grep: window\.open\(
Grep: router\.(push|replace)\(
Grep: navigate\(
Grep: redirect.*=.*http
```

Check:
- Redirect target from URL parameter without validation
- `window.open()` with user-controlled URL
- Router navigation to user-controlled paths
- Missing URL scheme validation (allowing `javascript:` protocol)
- Relative path manipulation leading to open redirect

---

## Category 9: Sensitive Data in Client Code

```
Grep: (api[_-]?key|apikey|secret|password|token|credential).*[:=].*['"]
Grep: Authorization.*Bearer
Grep: REACT_APP_|NEXT_PUBLIC_|VITE_|VUE_APP_
```

Check:
- API keys or secrets in client-side JavaScript bundles
- Secrets in environment variables prefixed for client exposure
- Hardcoded tokens in source code
- Internal API URLs or admin endpoints in client code
- Source maps deployed to production (exposing source code)
- Comments containing sensitive information in production builds

---

## Category 10: Client-Side Access Control

Check:
- Security decisions made only on client side (hiding UI elements instead of server enforcement)
- Admin routes protected only by client-side route guards
- Feature flags controlling security-critical features stored client-side
- Role-based rendering without corresponding server-side authorization
- Client-side token validation without server verification
