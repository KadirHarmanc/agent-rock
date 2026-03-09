# FastAPI Security Audit Guide

Use this guide when the project uses FastAPI or Starlette. FastAPI's dependency injection
system and Pydantic validation provide strong defaults, but misconfiguration and
missing guards remain common.

## Detection

Confirmed when you see:
- `fastapi` or `starlette` in requirements.txt / pyproject.toml
- `from fastapi import FastAPI`
- `uvicorn` in dependencies or startup scripts
- `@app.get`, `@app.post`, `@router.get` decorators

## Critical Areas

### 1. Dependency Injection & Authentication

```
Grep: Depends\(
Grep: def get_current_user
Grep: OAuth2PasswordBearer
Grep: HTTPBearer
Grep: Security\(
```

Check:
- Endpoints missing `Depends(get_current_user)` or equivalent auth dependency
- Auth dependency that returns `None` instead of raising `HTTPException` on failure
- Optional auth (`Optional[User]`) on sensitive endpoints allowing unauthenticated access
- Auth dependency checking token format but not validating claims or expiry
- Missing role/permission checks after user extraction
- `Depends()` with mutable default arguments (shared state)

### 2. Pydantic Validation Gaps

```
Grep: class.*BaseModel
Grep: Body\(
Grep: Query\(
Grep: Path\(
Grep: dict\[.*Any
Grep: request\.json\(\)
Grep: await request\.body\(\)
```

Check:
- Endpoints accepting raw `dict` or `Any` instead of typed Pydantic models
- Direct `request.json()` or `request.body()` bypassing Pydantic validation
- Missing field validators for business logic constraints
- `orm_mode = True` / `from_attributes = True` exposing all model fields
- Pydantic models without `Extra.forbid` allowing mass assignment
- Regex validators with ReDoS-vulnerable patterns

### 3. CORS Configuration

```
Grep: CORSMiddleware
Grep: allow_origins
Grep: allow_credentials
Grep: allow_methods
```

Check:
- `allow_origins=["*"]` — overly permissive CORS
- `allow_origins=["*"]` combined with `allow_credentials=True` — credential leak
- Dynamic origin reflection without validation
- `allow_methods=["*"]` when only specific methods are needed

### 4. SQL Injection & Database

```
Grep: execute\(.*f"
Grep: execute\(.*\.format
Grep: execute\(.*%.*%
Grep: text\(.*f"
Grep: raw_connection
Grep: session\.execute
```

Check:
- Raw SQL with f-strings or `.format()` — SQL injection
- SQLAlchemy `text()` with string interpolation
- Missing parameterized queries
- Database session not properly scoped (shared across requests)
- N+1 queries exposing timing side channels
- Alembic migrations with raw SQL containing user-derived values

### 5. File & Path Handling

```
Grep: UploadFile
Grep: FileResponse
Grep: StaticFiles
Grep: open\(.*request
Grep: Path\(
Grep: os\.path\.join
```

Check:
- File upload without type/size validation
- `FileResponse` with user-controlled path (path traversal)
- `StaticFiles` serving sensitive directories
- Missing filename sanitization on uploads
- Temporary files not cleaned up

### 6. Background Tasks & Async Safety

```
Grep: BackgroundTasks
Grep: background_tasks\.add_task
Grep: asyncio\.(create_task|gather|ensure_future)
Grep: async def
```

Check:
- Background tasks accessing request-scoped dependencies after response
- Shared mutable state across async handlers (race conditions)
- Missing error handling in background tasks (silent failures)
- Blocking I/O in async handlers without `run_in_executor`
- Database sessions shared across coroutines

### 7. Error Handling & Information Disclosure

```
Grep: HTTPException
Grep: exception_handler
Grep: debug=True
Grep: traceback
Grep: app = FastAPI\(
```

Check:
- `FastAPI(debug=True)` in production
- Exception handlers returning stack traces or internal details
- Generic `Exception` handlers swallowing security-relevant errors
- Missing custom exception handlers (default 500 may leak info)
- Detailed error messages revealing database schema or internal paths

### 8. WebSocket Security

```
Grep: @.*websocket
Grep: WebSocket
Grep: websocket\.accept
Grep: websocket\.receive
```

Check:
- WebSocket endpoints without authentication
- Missing origin validation on WebSocket connections
- User input from WebSocket messages not validated
- No rate limiting on WebSocket message frequency

### 9. Middleware & Security Headers

```
Grep: add_middleware
Grep: TrustedHostMiddleware
Grep: HTTPSRedirectMiddleware
Grep: @app\.middleware
```

Check:
- Missing `TrustedHostMiddleware` (host header injection)
- Missing `HTTPSRedirectMiddleware` in production
- Middleware ordering issues (auth after CORS, etc.)
- Custom middleware not handling exceptions properly
- Missing security headers (CSP, HSTS, X-Frame-Options)

### 10. OAuth2 & JWT

```
Grep: jwt\.decode
Grep: jwt\.encode
Grep: SECRET_KEY
Grep: ALGORITHM
Grep: jose\.|PyJWT\.|python-jose
```

Check:
- JWT secret hardcoded in source code
- Missing `algorithms` parameter in `jwt.decode()` (algorithm confusion)
- Missing token expiry validation
- Token not invalidated on password change or logout
- Symmetric signing with weak secrets

## Common False Positive Filters

- Pydantic models with `Extra.forbid` → mass assignment is mitigated
- `Depends(get_current_user)` verified on all routes → auth is present
- CORS with specific origin list → not overly permissive
- `debug=True` only in development config guarded by env check → not production risk
