# agent-rock Gelistirme Plani

**Repo:** https://github.com/akdenizemirhan/agent-rock
**Lokal kopya:** /tmp/agent-rock
**Kurulu skill dizini:** ~/.claude/skills/agent-rock, rock-quick, rock-deep

---

## Mevcut Yapi

```
.claude/skills/
├── agent-rock/
│   ├── SKILL.md                          # Ana skill (deep/quick mod)
│   ├── references/
│   │   ├── stack-detection.md            # Dil/framework algilama
│   │   ├── owasp-top10.md               # OWASP Top 10:2025 checklisti
│   │   ├── vulnerability-patterns.md     # Dil bazli zafiyet patternleri (9 dil)
│   │   ├── api-security-checklist.md     # 10 kategori API guvenlik
│   │   ├── configuration-security.md     # Env, secrets, headers, CORS, CI/CD
│   │   ├── cwe-mapping.md               # CWE referans tablosu
│   │   ├── finding-normalization.md      # Rapor tutarliligi kurallari
│   │   ├── express-node.md              # Express/Node odakli rehber
│   │   ├── django.md                    # Django/DRF odakli rehber
│   │   ├── spring.md                    # Spring Boot/Security rehber
│   │   ├── rails.md                     # Rails rehber
│   │   └── laravel.md                   # Laravel rehber
│   └── assets/
│       ├── report-template.md           # Markdown rapor sablonu
│       └── report-template.json         # JSON rapor sablonu
├── rock-quick/
│   └── SKILL.md                         # Quick mod wrapper
└── rock-deep/
    └── SKILL.md                         # Deep mod wrapper
```

---

## Guclu Yanlar (Dokunma)

- 8 kategori tarama (OWASP, Auth, Data, Deps, Config, API, Input, Crypto)
- 9 dil destegi (JS/TS, Python, Java, Go, Ruby, PHP, C#, Rust, C/C++)
- 5 framework rehberi (Express, Django, Spring, Rails, Laravel)
- Kanit-tabanli raporlama (dosya yolu + satir no + kod snippet)
- Dual output (Markdown + JSON)
- Sifir bagimlilik

---

## Gelistirme Alanlari

### 1. Yeni Framework Rehberleri (Oncelik: Yuksek)

Eksik olan populer frameworkler icin `references/` altina yeni rehberler ekle:

| Framework | Dosya | Odak |
|-----------|-------|------|
| **Next.js / Nuxt.js** | `nextjs.md` | SSR/SSG guvenligi, API routes, middleware, getServerSideProps, server actions |
| **FastAPI** | `fastapi.md` | Pydantic validation, dependency injection, CORS, OAuth2 |
| **NestJS** | `nestjs.md` | Guards, interceptors, pipes, decorators, TypeORM |
| **Flask** | `flask.md` | Blueprint guvenligi, Jinja2, session, CSRF |
| **ASP.NET Core** | `aspnet.md` | Middleware, Identity, authorization policies, model binding |
| **Gin / Echo (Go)** | `go-web.md` | Middleware chain, binding, template injection |

`stack-detection.md` dosyasini da bu frameworkleri algilayacak sekilde guncelle.

### 2. Frontend Guvenlik Modulu (Oncelik: Yuksek)

Yeni referans dosyasi: `references/frontend-security.md`

- CSP bypass patternleri
- postMessage origin dogrulama
- localStorage/sessionStorage hassas veri
- DOM-based XSS sinkleri (innerHTML, eval, vb.)
- iframe sandboxing
- Third-party script riskleri
- Service Worker guvenligi

### 3. Altyapi & IaC Guvenligi (Oncelik: Orta)

Yeni referans dosyasi: `references/infrastructure-security.md`

- **Dockerfile**: root kullanici, multi-stage, secret leak, base image
- **Kubernetes**: pod security, RBAC, secret yonetimi, network policy
- **Terraform/CloudFormation**: public S3, open security group, IAM over-permission
- **Serverless**: Lambda env vars, API Gateway auth, cold start race
- **docker-compose**: exposed ports, volume mounts, env_file

### 4. Concurrency & Race Condition Patternleri (Oncelik: Orta)

`vulnerability-patterns.md` dosyasina ekle:

- TOCTOU (Time of Check to Time of Use)
- Double-spend / double-submit
- Database race (SELECT sonra UPDATE, lock yok)
- File system race conditions
- Async handler siralanma sorunlari

### 5. GraphQL Derin Analiz (Oncelik: Orta)

`api-security-checklist.md` GraphQL bolumunu genislet:

- Query cost analizi / complexity limitleri
- Batch query istismari
- Nested fragment DoS
- Subscription auth
- Directive abuse
- Persisted queries vs dynamic queries

### 6. Supply Chain Derinlestirme (Oncelik: Orta)

`owasp-top10.md` A03 bolumunu genislet + yeni dosya `references/supply-chain.md`:

- Typosquatting algilama (benzer paket adlari)
- Post-install script riskleri
- Transitive dependency analizi
- .npmrc / .pypirc token leak
- GitHub Actions workflow injection
- Dependabot/Renovate yapilandirma kontrolu

### 7. Rapor Sablonu Iyilestirmeleri (Oncelik: Dusuk)

`assets/report-template.md` ve `report-template.json` guncelle:

- Trend/gecmis karsilastirma alani (onceki tarama ile diff)
- Remediation timeline onerileri (hemen / 1 hafta / 1 ay)
- False positive reasoning bolumu
- Compliance mapping (OWASP -> PCI-DSS, GDPR, SOC2 referanslari)
- Version bilgisi alani (agent-rock versiyonu)

### 8. Yeni Skill: rock-diff (Oncelik: Dusuk)

`rock-diff/SKILL.md` — Sadece git diff uzerinde calisan mod:

- `git diff` veya `git diff --staged` ciktisini tara
- PR/commit bazli guvenlik review
- CI/CD pipeline entegrasyonu icin ideal
- Sadece degisen satirlari analiz et

### 9. Yeni Skill: rock-deps (Oncelik: Dusuk)

`rock-deps/SKILL.md` — Sadece dependency audit:

- Tum ekosistemlerde dependency taramasi
- CVE eslemesi
- Lisans uyumluluk kontrolu
- End-of-life versiyon uyarilari

---

## Calisma Sirasi

```
Faz 1 (Yuksek Oncelik)
  ├── Yeni framework rehberleri (Next.js, FastAPI, NestJS, Flask)
  └── Frontend guvenlik modulu

Faz 2 (Orta Oncelik)
  ├── Altyapi & IaC guvenligi
  ├── Concurrency patternleri
  ├── GraphQL derin analiz
  └── Supply chain derinlestirme

Faz 3 (Dusuk Oncelik)
  ├── Rapor sablonu iyilestirmeleri
  ├── rock-diff skill
  └── rock-deps skill
```

---

## Notlar

- Her yeni referans dosyasi eklendiginde `SKILL.md` Phase 1 Discovery bolumune framework algilama eklenmeli
- `stack-detection.md` her yeni framework icin guncellenmeli
- `vulnerability-patterns.md` yeni dil/framework patternleri eklenebilir
- Test icin cesitli acik kaynak projeler uzerinde `/agent-rock` calistirilip rapor kalitesi olculebilir
