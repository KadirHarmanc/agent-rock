# Laravel Guide

Use this guide when the repo uses Laravel routing, middleware, request validation, and Eloquent.

## Confirm the Stack

Look for:
- `laravel/framework`, `sanctum`, `passport`, `spatie/laravel-permission`
- `routes/web.php`, `routes/api.php`, `app/Http/Controllers/`
- middleware aliases, form requests, Eloquent models

## High-Signal Files

- API and web route definitions
- auth middleware, guards, policies, gates
- controllers performing updates, uploads, exports, or admin actions
- request validation classes and models with guarded/fillable configuration
- queue jobs and webhook handlers

## What to Verify

### Auth, Policies, and IDOR

- Confirm sensitive routes use the intended middleware and guard.
- Verify policies or gates enforce object-level ownership.
- Review implicit route model binding for tenant or owner scoping issues.

**Useful patterns:**
```
"Route::|middleware\(|auth:|can:|Gate::|Policy"
"authorize\(|\$this->authorize|FormRequest"
"routeModelBinding|findOrFail|firstOrFail|request\(\)->user"
```

### Validation and Mass Assignment

- Confirm request validation runs before model writes.
- Review `$fillable`, `$guarded`, `forceFill`, `update`, and `create` calls.
- Verify privileged flags are not accepted from request payloads.

**Useful patterns:**
```
"\\$fillable|\\$guarded|forceFill|fill\(|create\(|update\("
"validate\(|FormRequest|rules\("
"request\(\)->all|\\$request->all|only\(|validated\("
```

### File Uploads, Redirects, and SSRF

- Review storage paths, file naming, extension checks, and public exposure.
- Trace user-controlled URLs into HTTP clients, webhooks, or callback handlers.
- Review redirect parameters and signed URL assumptions.

**Useful patterns:**
```
"storeAs|putFile|putFileAs|Storage::"
"Http::|GuzzleHttp|curl|webhook|callback"
"redirect\(|away\(|to_route|signedRoute"
```

## Severity Notes

- Empty `$guarded` is only a lead until you show a reachable write path to sensitive fields.
- Missing validation libraries are not findings by themselves; prove the unsafe write or unsafe read.
- Policy gaps on reachable privileged routes are often `High`.
