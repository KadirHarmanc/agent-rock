# Rails Guide

Use this guide when the target app follows standard Rails routing, controller, model, and
initializer patterns.

## Confirm the Stack

Look for:
- `rails`, `devise`, `pundit`, `cancancan`
- `config/routes.rb`, `app/controllers/`, `app/models/`, `config/initializers/`
- Active Record models and strong parameters

## High-Signal Files

- `config/routes.rb`
- base controllers and auth helpers
- controllers handling account, billing, admin, or file operations
- models with callbacks or dynamic scopes
- initializers for session, cookies, CORS, and serialization

## What to Verify

### Authentication and Authorization

- Confirm `before_action` hooks actually cover the sensitive actions.
- Verify admin and tenant boundaries at the controller or policy level.
- Review `skip_before_action`, permissive policy methods, and background job entry points.

**Useful patterns:**
```
"before_action|skip_before_action|authenticate_user!"
"authorize|policy_scope|Pundit|CanCan|load_and_authorize_resource"
"params\[:id\]|current_user|current_account"
```

### Strong Parameters and Mass Assignment

- Treat `permit!` or unsafe parameter conversion as high-signal leads.
- Verify models do not accept privileged fields through nested params.
- Check JSON APIs and admin panels separately; they often diverge from web controllers.

**Useful patterns:**
```
"permit!|to_unsafe_h|to_unsafe_hash"
"params\.require|params\.fetch"
"update\(|update_attributes|assign_attributes|create\("
```

### XSS, Redirects, and Dynamic Behavior

- Review `html_safe`, raw rendering, open redirects, dynamic constantization, and file handling.
- Verify uploads and background jobs do not trust user-controlled paths or URLs.

**Useful patterns:**
```
"html_safe|raw\(|sanitize\("
"redirect_to|url_for|params\[:redirect"
"constantize|safe_constantize|send\(|public_send\("
```

## Severity Notes

- `permit!` is not automatically a finding; show how privileged fields become writable.
- Broken policy coverage on sensitive actions is often `High`.
- Raw rendering without attacker-controlled input may not be a finding.
