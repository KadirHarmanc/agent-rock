# Next.js / Nuxt.js Security Audit Guide

Use this guide when the project uses Next.js or Nuxt.js. These frameworks introduce
SSR/SSG-specific attack surfaces alongside standard React/Vue risks.

## Detection

Confirmed when you see:
- `next` or `nuxt` in package.json dependencies
- `next.config.js`, `next.config.mjs`, `next.config.ts`
- `nuxt.config.js`, `nuxt.config.ts`
- `app/` or `pages/` directory with route-based file structure
- `getServerSideProps`, `getStaticProps`, `useServer`, `server actions`

## Critical Areas

### 1. Server Actions & API Routes

**Next.js App Router (v13+):**
```
Grep: "use server"
Grep: export.*async.*function.*(formData|request)
Grep: app/api/.*/route\.(ts|js)
```

Check:
- Server actions accessible without authentication
- Missing input validation in server action parameters
- FormData parsed without sanitization
- API route handlers missing auth middleware
- `NextResponse.json()` returning sensitive internal data

**Next.js Pages Router:**
```
Grep: export.*getServerSideProps
Grep: export.*getStaticProps
Grep: pages/api/
```

Check:
- `getServerSideProps` fetching data without access control
- API routes without authentication checks
- Secrets leaked through `getStaticProps` into client bundle

**Nuxt.js:**
```
Grep: server/api/
Grep: defineEventHandler
Grep: server/middleware/
```

### 2. Server-Side Rendering (SSR) Injection

```
Grep: dangerouslySetInnerHTML
Grep: v-html
Grep: innerHTML
Grep: __html
```

Check:
- User input rendered via `dangerouslySetInnerHTML` in SSR context
- `v-html` with user-controlled content in Nuxt
- HTML content from database rendered without sanitization
- Server components rendering user input without escaping

### 3. Client/Server Boundary Leaks

```
Grep: "use client"
Grep: "use server"
Grep: NEXT_PUBLIC_
Grep: NUXT_PUBLIC_
Grep: runtimeConfig
```

Check:
- Secrets in `NEXT_PUBLIC_*` env vars (these are exposed to browser)
- Server-only secrets accidentally imported in client components
- `runtimeConfig.public` containing sensitive values in Nuxt
- API keys or tokens passed from server to client components via props
- Database connection strings or internal URLs in client-accessible config

### 4. Middleware Security

**Next.js middleware:**
```
Grep: middleware\.(ts|js)
Grep: NextRequest
Grep: NextResponse\.redirect
Grep: NextResponse\.rewrite
```

Check:
- Auth middleware can be bypassed via path manipulation
- Missing middleware on sensitive routes
- Middleware matching patterns too broad or too narrow
- Open redirect via unvalidated redirect targets in middleware
- Header manipulation without validation

**Nuxt.js middleware:**
```
Grep: defineNuxtRouteMiddleware
Grep: server/middleware/
```

### 5. Static Generation & ISR Risks

```
Grep: revalidate
Grep: getStaticPaths
Grep: generateStaticParams
Grep: fallback.*true
```

Check:
- `fallback: true` or `dynamicParams: true` allowing arbitrary path rendering
- ISR revalidation endpoints without authentication
- On-demand revalidation tokens hardcoded or leaked
- Cached pages containing user-specific sensitive data
- Static pages with stale security-critical content

### 6. Image & File Handling

```
Grep: next/image
Grep: remotePatterns
Grep: domains.*\[
Grep: unoptimized
```

Check:
- `remotePatterns` or `domains` too permissive (allows SSRF via image optimization)
- File upload handlers without type/size validation
- User-controlled image URLs proxied through Next.js image optimizer
- `unoptimized: true` bypassing image safety checks

### 7. Authentication Patterns

```
Grep: next-auth|NextAuth|authOptions
Grep: getServerSession
Grep: useSession
Grep: auth\(\)
```

Check:
- NextAuth.js `NEXTAUTH_SECRET` missing or weak
- Session callback leaking extra user data to client
- Missing `getServerSession` check in server actions
- JWT callback exposing internal IDs or roles without need
- OAuth callback URL not restricted
- CSRF protection disabled in NextAuth config

### 8. Headers & Security Configuration

```
Grep: headers.*async
Grep: Content-Security-Policy
Grep: X-Frame-Options
Grep: next.config
```

Check in `next.config.js`:
- Missing security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- `poweredBy: true` (leaks framework info)
- Permissive `rewrites` or `redirects` enabling open redirect
- `experimental` features enabled in production

## Common False Positive Filters

- `dangerouslySetInnerHTML` with DOMPurify or sanitized content → verify sanitizer is applied
- `NEXT_PUBLIC_` vars containing only non-secret config (site URL, feature flags) → not a finding
- Server actions in admin-only layouts with upstream auth → verify middleware coverage
- `getStaticProps` with public data only → not a data leak
