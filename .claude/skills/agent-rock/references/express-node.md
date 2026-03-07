# Express / Node Guide

Use this guide when the target app exposes Express-style middleware chains, routers, sessions,
JWT auth, uploads, or typical Node API handlers.

## Confirm the Stack

Look for:
- `express`, `express-session`, `cookie-session`, `passport`, `jsonwebtoken`
- `router.get`, `router.post`, `app.use`, `app.METHOD`
- middleware directories, `server.js`, `app.js`, `src/app.ts`, `src/server.ts`

## High-Signal Files

- Main app bootstrap and middleware registration
- Route files under `routes/`, `api/`, `controllers/`
- Auth/session code
- ORM/database wrappers
- Upload handlers and background job consumers

## What to Verify

### Authentication and Authorization

- Sensitive routes should have auth middleware in the actual router chain, not only helper imports.
- Admin or privileged routes should enforce role checks near the handler or in verified middleware.
- Resource access should verify ownership or tenant scope, not just `req.params.id`.

**Useful patterns:**
```
"app\.use\(|router\.(get|post|put|patch|delete)\("
"isAuthenticated|requireAuth|authorize|requireRole|requireAdmin|ensureLoggedIn"
"findById|findOne\(|findByPk|req\.params\.id|req\.user"
```

### Sessions, JWT, and Cookies

- Verify secure cookie settings for session-backed apps.
- Confirm JWT verification pins algorithms and rejects unsigned or weakly configured tokens.
- Confirm password reset and login flows enforce expiry, rotation, and brute-force resistance where needed.

**Useful patterns:**
```
"express-session|cookie-session|session\("
"jsonwebtoken|jwt\.sign|jwt\.verify"
"cookie.*secure|httpOnly|sameSite|SESSION_SECRET|JWT_SECRET"
```

### Input Validation and Mass Assignment

- Verify request validation happens before handler logic for create/update routes.
- Trace `req.body`, `req.query`, and `req.params` into ORM and raw query calls.
- Watch for object spreads or `Object.assign` into models.

**Useful patterns:**
```
"req\.(body|query|params)"
"\.create\(req\.body|\.update\(req\.body|findByIdAndUpdate\(.*req\.body"
"\.\.\.req\.body|Object\.assign\(.*req\.body"
"joi|zod|yup|express-validator"
```

### SSRF, File Upload, and Command Execution

- Trace user-controlled URLs into `fetch`, `axios`, or SDK calls.
- Verify uploads enforce content type, size, storage path, and post-processing safety.
- Trace user input into `child_process`, shell commands, or filesystem paths.

**Useful patterns:**
```
"multer|busboy|formidable|upload"
"axios|fetch|request\(|got\("
"child_process|exec\(|execSync|spawn|spawnSync"
"path\.join|path\.resolve|fs\.(readFile|writeFile|unlink)"
```

## Severity Notes

- Missing auth on a reachable privileged route is often `High` or `Critical` depending on impact.
- Session misconfiguration without a clear exploit path is often `Medium`.
- Missing generic validation libraries is not a finding by itself; prove the unsafe data flow.
