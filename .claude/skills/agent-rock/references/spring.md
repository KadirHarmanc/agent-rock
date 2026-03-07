# Spring Guide

Use this guide when the target app uses Spring MVC, Spring Boot, Spring Security, or Spring Data.

## Confirm the Stack

Look for:
- `spring-boot-starter-web`, `spring-security`, `spring-data-*`
- `@RestController`, `@Controller`, `@RequestMapping`
- `SecurityFilterChain`, `HttpSecurity`, `application.yml`, `application.properties`

## High-Signal Files

- security config classes
- controller packages
- service and repository layers handling privileged state changes
- serialization, deserialization, XML, and file upload code
- application config and profile-specific properties

## What to Verify

### Security Configuration

- Confirm request matchers do not overuse `permitAll`.
- Verify sensitive endpoints are covered by authz annotations or central policy.
- Confirm CSRF, CORS, and session policy decisions match the actual app type.

**Useful patterns:**
```
"permitAll\(|authenticated\(|hasRole\(|hasAuthority\("
"@PreAuthorize|@Secured|@RolesAllowed"
"csrf\(\)\.disable|cors\(|sessionCreationPolicy"
```

### Controllers and Binding

- Trace request DTOs and model binding into privileged operations.
- Verify `@ModelAttribute`, flexible JSON binding, or update endpoints do not over-post sensitive fields.
- Confirm IDs from the request are re-scoped to the caller where needed.

**Useful patterns:**
```
"@RequestBody|@ModelAttribute|BindingResult"
"setAllowedFields|BeanUtils\.copyProperties|ModelMapper"
"@PathVariable|@RequestParam|repository\.findById|service\.findById"
```

### Injection, Deserialization, and XML

- Trace concatenated SQL, JPQL, native queries, shell calls, and templating.
- Review XML parsers for XXE-safe configuration.
- Review Jackson polymorphic settings and Java deserialization.

**Useful patterns:**
```
"JdbcTemplate|createNativeQuery|createQuery|Statement\."
"ObjectInputStream|readObject|XmlMapper|XMLInputFactory|DocumentBuilderFactory"
"@JsonTypeInfo|enableDefaultTyping|Runtime\.getRuntime\(\)\.exec"
```

## Severity Notes

- `permitAll` on a sensitive controller is only a finding after you confirm the route is actually reachable and privileged.
- XXE and unsafe deserialization on user-controlled inputs are often `High`.
- Missing fine-grained method auth may be `Medium` or `High` depending on exposure and reachable actions.
