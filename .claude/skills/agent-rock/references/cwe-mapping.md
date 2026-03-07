# CWE Quick Mapping

Use this file to assign a reasonable CWE when the issue family is clear. Prefer the most specific
verified CWE you can support from the code and report. If multiple CWEs might apply, choose the
one that best matches the demonstrated root cause.

## Access Control

- Missing function-level authorization, missing admin check: `CWE-862` Missing Authorization
- IDOR / BOLA / object ownership failure: `CWE-639` Authorization Bypass Through User-Controlled Key
- Path traversal to unauthorized files: `CWE-22` Path Traversal

## Injection and Code Execution

- SQL injection: `CWE-89` Improper Neutralization of Special Elements used in an SQL Command
- NoSQL injection: `CWE-943` Improper Neutralization of Special Elements in Data Query Logic
- OS command injection: `CWE-78` OS Command Injection
- LDAP injection: `CWE-90` LDAP Injection
- Server-side template injection: `CWE-1336` Template Engine Injection
- Unsafe dynamic evaluation: `CWE-95` Eval Injection

## Cross-Site Scripting and Output Handling

- Stored or reflected XSS: `CWE-79` Cross-Site Scripting
- DOM-based XSS sink: `CWE-79` Cross-Site Scripting
- Output encoding gap in templates: `CWE-116` Improper Encoding or Escaping of Output

## Authentication and Session

- Weak or missing auth on reachable endpoints: `CWE-306` Missing Authentication for Critical Function
- Weak password policy or insecure password recovery: `CWE-521` Weak Password Requirements
- Hardcoded password, token, or secret in source: `CWE-798` Use of Hard-coded Credentials
- Session fixation or weak session management: `CWE-384` Session Fixation
- Sensitive token in URL: `CWE-598` Information Exposure Through Query Strings in GET Request

## Sensitive Data and Cryptography

- Sensitive data exposure in logs or responses: `CWE-200` Exposure of Sensitive Information
- Missing encryption or cleartext transport: `CWE-319` Cleartext Transmission of Sensitive Information
- Weak hashing or weak crypto algorithm: `CWE-327` Broken or Risky Cryptographic Algorithm
- Hardcoded key or IV: `CWE-321` Use of Hard-coded Cryptographic Key
- Predictable randomness for security token: `CWE-338` Use of Cryptographically Weak PRNG

## Deserialization and Integrity

- Unsafe deserialization: `CWE-502` Deserialization of Untrusted Data
- Unsigned or unverified update/integrity path: `CWE-494` Download of Code Without Integrity Check

## API and Request Handling

- Mass assignment / over-posting: `CWE-915` Improperly Controlled Modification of Dynamically-Determined Object Attributes
- Missing request size limits leading to DoS risk: `CWE-770` Allocation of Resources Without Limits or Throttling
- Missing rate limiting on reachable critical flow: `CWE-307` Improper Restriction of Excessive Authentication Attempts or `CWE-770` depending on the demonstrated effect
- SSRF: `CWE-918` Server-Side Request Forgery
- Open redirect: `CWE-601` Open Redirect

## Error Handling and Configuration

- Verbose error leakage: `CWE-209` Information Exposure Through an Error Message
- Debug mode in production: `CWE-489` Active Debug Code
- Overly permissive CORS: `CWE-942` Permissive Cross-domain Policy with Untrusted Domains
- Missing security headers with a demonstrated browser risk: `CWE-693` Protection Mechanism Failure

## Supply Chain and CI/CD

- Unpinned third-party GitHub Action or external dependency execution path: `CWE-829` Inclusion of Functionality from Untrusted Control Sphere
- Download-and-execute bootstrap script without verification: `CWE-494` Download of Code Without Integrity Check

## When to Omit CWE

It is acceptable to omit the CWE if:
- the issue is real but spans multiple weaknesses and a confident primary CWE is unclear
- the report would otherwise guess
- the observed problem is best described as an architectural observation instead of a concrete weakness
