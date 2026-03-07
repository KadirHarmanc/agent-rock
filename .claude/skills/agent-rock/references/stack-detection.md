# Stack Detection Heuristics

Use this file after identifying package manifests. The goal is to convert manifest clues into a
focused audit plan so you only load the framework references that matter.

## General Process

1. Read the primary manifests inside the target root.
2. Identify the dominant language and runtime.
3. Map direct dependencies and config files to likely frameworks.
4. Confirm the framework by reading one or two entry-point files before loading deeper guidance.
5. Load only the relevant framework reference files from this directory.

## JavaScript / TypeScript

**Manifest clues:**
- `express`, `koa`, `fastify`, `hapi`, `nestjs`, `next`, `nuxt`, `sails`
- ORM and API clues: `mongoose`, `prisma`, `sequelize`, `typeorm`, `apollo-server`

**Config and file clues:**
- `server.js`, `app.js`, `src/server.ts`, `src/app.ts`
- `next.config.js`, `next.config.mjs`, `app/`, `pages/`
- `nest-cli.json`, `main.ts`, `app.module.ts`

**When to load focused guidance:**
- Load [express-node.md](express-node.md) for Express-style routers, middleware chains, session auth, file upload flows, and common Node API patterns.

## Python

**Manifest clues:**
- `django`, `djangorestframework`, `channels`
- `flask`, `flask-login`, `flask-wtf`
- `fastapi`, `starlette`, `uvicorn`, `pydantic`

**Config and file clues:**
- `manage.py`, `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
- `app.py`, `wsgi.py`, `blueprints/`
- `main.py`, `routers/`, `dependencies.py`

**When to load focused guidance:**
- Load [django.md](django.md) when you see Django settings, URLconf, ORM models, serializers, or DRF views.

## Java / JVM

**Manifest clues:**
- `spring-boot`, `spring-security`, `spring-web`, `spring-data`
- `quarkus`, `micronaut`

**Config and file clues:**
- `application.yml`, `application.properties`
- `@RestController`, `@Controller`, `@Configuration`, `@EnableWebSecurity`
- `SecurityFilterChain`, `WebSecurityConfigurerAdapter`

**When to load focused guidance:**
- Load [spring.md](spring.md) when you see Spring MVC, Spring Security, or Spring Data patterns.

## Ruby

**Manifest clues:**
- `rails`, `devise`, `pundit`, `cancancan`, `sidekiq`

**Config and file clues:**
- `config/routes.rb`, `app/controllers/`, `app/models/`, `config/initializers/`
- `ApplicationController`, `ActiveRecord`, `strong_parameters`

**When to load focused guidance:**
- Load [rails.md](rails.md) when the app follows standard Rails routing, controller, and model conventions.

## PHP

**Manifest clues:**
- `laravel/framework`, `sanctum`, `passport`, `spatie/laravel-permission`
- `symfony/framework-bundle`

**Config and file clues:**
- `routes/web.php`, `routes/api.php`, `app/Http/Controllers/`, `app/Models/`
- `config/app.php`, `config/auth.php`, middleware classes

**When to load focused guidance:**
- Load [laravel.md](laravel.md) when the app uses Laravel routing, middleware, Eloquent, or request validation.

## C / C++

**Build clues:**
- `CMakeLists.txt`, `Makefile`, `meson.build`, `compile_commands.json`
- source trees such as `src/`, `include/`, `lib/`

**Focus points:**
- Distinguish server/network code, CLI utilities, parsers, and privileged helpers.
- Prioritize memory safety issues on externally reachable parsing, network, file, or IPC paths.

## Ambiguous Repos

If multiple frameworks appear:
- Prioritize the code that serves external traffic or privileged operations.
- Load only the guides relevant to the reachable application surface.
- Treat tooling, examples, and old migrations as secondary unless they are still executed.
