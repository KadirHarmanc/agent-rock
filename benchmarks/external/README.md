# External Benchmark Sources

These sources are candidates for future agent-rock validation beyond the in-repo fixture suite.

## Best Fits

- **OWASP Benchmark**: strong for static-analysis evaluation, especially Java and Python web-style test cases
- **OpenSSF CVE Benchmark**: useful for replaying real historical vulnerable vs fixed cases
- **NIST SARD / Juliet**: good for broad CWE coverage, especially C/C++ and Java

## Training Apps, Not Clean Scoreboards

- **OWASP Juice Shop**
- **OWASP WebGoat**
- **DVWA**

These are useful for manual testing and scanner sanity checks, but they are not as clean for automated pass/fail scoring.

## Recommended Strategy

Use three layers:

1. in-repo fixture cases for daily regression testing
2. paired vulnerable/fixed replay cases for stronger proof
3. external benchmark imports for broader validation
