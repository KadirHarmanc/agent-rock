# Django Guide

Use this guide when the target repo contains Django or Django REST Framework settings, URLconf,
ORM models, serializers, or class-based views.

## Confirm the Stack

Look for:
- `django`, `djangorestframework`, `channels`
- `manage.py`, `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
- `APIView`, `ViewSet`, serializers, middleware settings

## High-Signal Files

- `settings.py` and environment-specific settings modules
- `urls.py`, router registration, DRF viewsets
- auth backends, custom permissions, middleware
- models, serializers, forms, and file upload handlers

## What to Verify

### Authentication, Permissions, and IDOR

- Confirm DRF views use the intended `authentication_classes` and `permission_classes`.
- Check object-level permissions, not only class-level auth.
- Trace `pk` and queryset filters to ensure tenant or owner scoping.

**Useful patterns:**
```
"permission_classes|authentication_classes|IsAuthenticated|AllowAny"
"get_queryset|queryset =|get_object\("
"request\.user|filter\(.*user=|filter\(.*tenant="
```

### Settings and Middleware

- Verify `DEBUG`, `ALLOWED_HOSTS`, cookie flags, CSRF, and security middleware.
- Confirm production settings do not inherit unsafe defaults from local settings.
- Confirm proxy and HTTPS settings are appropriate when the app is deployed behind a load balancer.

**Useful patterns:**
```
"DEBUG\s*=|ALLOWED_HOSTS|CSRF_TRUSTED_ORIGINS"
"SecurityMiddleware|CsrfViewMiddleware|SessionMiddleware"
"SESSION_COOKIE_SECURE|CSRF_COOKIE_SECURE|SECURE_PROXY_SSL_HEADER"
```

### Serializers, Forms, and Mass Assignment

- Treat `fields = "__all__"` as a lead and inspect what fields become writable or exposed.
- Verify serializers and forms restrict privileged fields.
- Confirm model save hooks do not trust user-supplied privileged values.

**Useful patterns:**
```
"fields\s*=\s*\"__all__\"|fields\s*=\s*'__all__'"
"read_only_fields|extra_kwargs|ModelForm|ModelSerializer"
"serializer\.save\(|form\.save\("
```

### Templates, Uploads, and Deserialization

- Verify uploaded files have size, extension, and content-type checks.
- Trace any direct file handling to storage path validation.
- Check dangerous template rendering and unsafe deserialization helpers.

**Useful patterns:**
```
"FileField|ImageField|UploadedFile|request\.FILES"
"mark_safe|safe|format_html|render_to_string"
"yaml\.load|pickle\.loads|subprocess|os\.system"
```

## Severity Notes

- `DEBUG=True` in effective production config is a verified misconfiguration, not merely a code smell.
- Serializer overexposure is often `Medium` unless it exposes secrets or privileged state transitions.
- Object-level auth failures on reachable endpoints are often `High`.
