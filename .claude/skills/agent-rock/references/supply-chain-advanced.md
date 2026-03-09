# Advanced Supply Chain Security Reference

Use this reference to supplement the OWASP Top 10 A03 (Supply Chain) checks with
deeper analysis of dependency confusion, typosquatting, CI/CD attacks, and
transitive dependency risks.

---

## Category 1: Dependency Confusion & Typosquatting

### Package Name Analysis
```
Grep: "name".*:.*"@
Grep: "dependencies"|"devDependencies"
```

Check for packages with names that:
- **Typosquat popular packages**: One character difference from well-known packages
  - Examples: `lodahs` vs `lodash`, `reqeusts` vs `requests`, `collor` vs `color`
- **Use different separators**: `python-dateutil` vs `python_dateutil`
- **Internal package naming**: Private packages without organization scope (`@org/pkg`)
- **Dependency confusion**: Internal package name exists on public registry

### Namespace/Scope Verification
```
Grep: "@[a-z].*/"
```

Check:
- Scoped packages (`@org/package`) → verify the org is correct
- Unscoped packages for internal code → vulnerability to public registry substitution
- Mixed scoped/unscoped packages from same organization → inconsistency risk

### Registry Configuration
```
Glob: **/.npmrc
Glob: **/.yarnrc
Glob: **/.yarnrc.yml
Glob: **/pip.conf
Glob: **/.pypirc
Glob: **/nuget.config
```

Check:
- **Registry tokens committed**: `.npmrc` with `//registry.npmjs.org/:_authToken=`
- **PyPI tokens committed**: `.pypirc` with passwords
- **Missing registry scoping**: Internal packages not configured to use private registry
- **Mixed registries**: Some packages from private, some from public without explicit mapping
- **No registry lock**: No configuration preventing installation from unauthorized registries

---

## Category 2: Post-Install Script Risks

### npm/yarn
```
Grep: "preinstall"|"postinstall"|"preuninstall"|"install"
```

Check in package.json `scripts`:
- **postinstall scripts**: Running arbitrary code during installation
- **preinstall scripts**: May execute before developer reviews package
- Verify: Are install scripts downloading/executing external code?
- Check if `.npmrc` has `ignore-scripts=true` for CI

### Python
```
Grep: setup\(.*cmdclass
Grep: setup\.py.*import os|subprocess
```

Check in `setup.py`:
- Custom `cmdclass` overriding `install` or `develop` commands
- `setup.py` executing system commands during installation
- `__init__.py` in packages running code at import time

### Ruby
```
Grep: spec\.extensions
Grep: Gem::Ext
```

Check:
- Gems with native extensions executing build scripts
- `extconf.rb` or `Rakefile` with suspicious commands

---

## Category 3: Lockfile Integrity

### Lockfile Presence
```
Glob: **/package-lock.json
Glob: **/yarn.lock
Glob: **/pnpm-lock.yaml
Glob: **/Pipfile.lock
Glob: **/poetry.lock
Glob: **/Gemfile.lock
Glob: **/composer.lock
Glob: **/go.sum
Glob: **/Cargo.lock
```

Check:
- **Missing lockfile**: Builds are non-deterministic, vulnerable to version injection
- **Lockfile not in git**: Same risk as missing
- **Lockfile/manifest mismatch**: Lockfile outdated compared to manifest
- **Integrity hashes**: npm lockfile should have `integrity` fields with SHA hashes

### Lockfile Tampering Indicators
```
Grep: resolved.*http://
Grep: integrity.*sha1
```

Check:
- **HTTP registry URLs**: `resolved` pointing to `http://` instead of `https://`
- **Weak integrity hashes**: Using SHA-1 instead of SHA-512
- **Changed registry**: Lockfile resolved URLs pointing to unexpected registry
- **Version downgrades**: Package version lower in lockfile than manifest minimum

---

## Category 4: Transitive Dependency Analysis

### Broad Version Ranges
```
Grep: "\*"|"latest"|">=.*<"
Grep: "\^0\."
```

Check:
- **Wildcard versions**: `"*"` or `"latest"` → any version accepted
- **Pre-1.0 caret ranges**: `"^0.x"` allows breaking changes (npm treats 0.x specially)
- **Missing upper bounds**: `">=2.0"` without `"<3.0"` → major version jumps accepted
- **Git dependencies**: `"package": "github:user/repo"` → no version pinning

### Known Vulnerability Patterns
Check dependencies for patterns associated with known supply chain attacks:
- Packages with very recent publish dates and high download counts (impossible organically)
- Packages with single maintainer and no repository link
- Packages that have been deprecated and replaced

---

## Category 5: CI/CD Supply Chain

### GitHub Actions
```
Grep: uses:.*@
Grep: uses:.*@(main|master|latest|v\d+$)
```

Check:
- **Unpinned actions**: `uses: action/name@main` → vulnerable to tag/branch mutation
- **Tag-only pinning**: `uses: action@v3` → tags can be moved
- **Safe pattern**: `uses: action@sha256hash` — pinned by commit SHA
- **Third-party actions**: Using actions from unknown organizations
- **Self-hosted runner exposure**: Untrusted workflows running on self-hosted runners

### Build Pipeline
```
Grep: curl.*\|.*sh
Grep: wget.*\|.*sh
Grep: pip install.*--index-url
Grep: npm install.*--registry
```

Check:
- **Pipe to shell**: `curl URL | sh` — executing unverified remote code
- **Custom registries in CI**: Pointing to non-standard registries without verification
- **Build-time downloads**: Fetching binaries during build without checksum verification
- **Cached dependencies**: Using shared cache across untrusted builds

### Dependency Update Bots
```
Glob: **/.github/dependabot.yml
Glob: **/renovate.json
Glob: **/.renovaterc
```

Check:
- **Missing dependency update bot**: No automated vulnerability patching
- **Overly permissive auto-merge**: Auto-merging all dependency updates without review
- **Missing security-only mode**: Not prioritizing security patches
- **Ignored packages**: Security-relevant packages in ignore list

---

## Category 6: Build Artifact Integrity

### Package Publishing
```
Glob: **/.npmignore
Glob: **/MANIFEST.in
Glob: **/setup.cfg
Grep: "files"|"main"|"exports"
```

Check:
- **Missing .npmignore / .gitignore**: Source files, tests, configs published to registry
- **Sensitive files in package**: `.env`, `credentials`, private keys in published package
- **No provenance**: Published packages without build provenance or signing
- **Missing `files` field in package.json**: Everything published by default

### Binary/Artifact Verification
```
Grep: checksum|sha256|sha512|gpg|signature
Grep: SHASUMS|checksums\.txt
```

Check:
- **Downloaded binaries without checksum verification**
- **Missing signature verification on artifacts**
- **Checksums from same source as binary**: Both compromised if source is compromised

---

## Severity Guidelines for Supply Chain Findings

| Finding | Typical Severity |
|---------|-----------------|
| Registry token committed to git | Critical |
| Pipe-to-shell in CI/CD | High |
| Missing lockfile (production dependency) | High |
| Dependency confusion risk (internal packages on public registry) | High |
| Unpinned GitHub Actions | Medium |
| Missing dependency update bot | Medium |
| Broad version ranges on security-critical packages | Medium |
| Pre-1.0 caret ranges | Low |
| Missing SRI/integrity on CDN scripts | Medium |
| No provenance on published packages | Low |

---

## Common False Positive Filters

- `postinstall` scripts running `husky install` or `patch-package` → common safe patterns
- Dev-only dependencies with broad ranges → lower risk than production deps
- Lockfile with HTTP URLs pointing to private registry on internal network → may be intentional
- `curl | sh` in development setup scripts (not CI/CD) → lower risk, note as observation
