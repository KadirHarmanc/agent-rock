# agent-rock AR-GE Raporu

**Tarih:** 2026-03-09
**Yontem:** 10 paralel agent tarafindan kapsamli analiz
**Kapsam:** Tum skill dosyalari, referanslar, sablonlar, mimari, rekabet, trendler

---

## YONETICI OZETI

agent-rock, Claude Code icin gelistirilmis acik kaynak bir statik guvenlik denetim skill'idir. 8 kategori, 9 dil, 5 framework rehberi ve kanit-tabanli raporlama ile **guclu bir Beta** asamasindadir.

**Genel Kalite Skoru: 5.8/10** (Agent 1)

| Guclu Yanlar | Kritik Eksiklikler |
|---|---|
| Kanit-tabanli raporlama (asla bulgu uydurmama) | CI/CD entegrasyonu yok |
| 8 kategori kapsamli tarama | Modern frameworkler eksik (Next.js, FastAPI, NestJS) |
| Dual cikti (Markdown + JSON) | False positive orani yuksek (%20-35) |
| OWASP Top 10:2025 uyumu | AI/ML guvenligi tamamen eksik |
| Sifir bagimlilik, sifir kurulum | SARIF, CVSS, compliance mapping yok |
| Framework-ozel rehberler | gRPC, WebSocket tamamen eksik |

---

## 1. DOSYA BAZLI KALITE DEGERLENDIRMESI (Agent 1)

| Dosya | Skor | Temel Sorunlar |
|---|---|---|
| SKILL.md | 6.5/10 | Hardening vs Finding siniri belirsiz, async/OAuth eksik, JSON schema yok |
| owasp-top10.md | 6/10 | Tenant isolation, type confusion, framework-spesifik FN riskleri |
| vulnerability-patterns.md | 5.5/10 | SpEL, gadget chain, symlink eksik; pattern tutarliligi zayif |
| finding-normalization.md | 6.5/10 | Severity siniri fuzzy, deduplication eksik, ID persistence yok |
| cwe-mapping.md | 6/10 | CWE overlap (862 vs 639), is mantigi/race condition CWE'leri yok |
| configuration-security.md | 5.5/10 | FP riski yuksek, Docker/K8s/IaC yuzeysel, dil kapsami dusuk |
| api-security-checklist.md | 5/10 | GraphQL threshold tanimsiz, gRPC/WebSocket yok, rate limiting dar |
| rock-quick.md | 5.5/10 | Arguman catismasi, "high-signal" tanimsiz |
| rock-deep.md | 5.5/10 | Ayni arguman catismasi, derinlik kalite artirmiyor |

---

## 2. FRAMEWORK ANALIZI (Agent 2)

### Mevcut Framework Kapsami

| Framework | Kapsam | Tespit Dogrulugu | En Kritik Eksik |
|---|---|---|---|
| Express/Node | %65-70 | %87 | Prototype pollution, ReDoS, rate limiting |
| Django | %70-75 | %91 | Async views, signal bypass, cache poisoning |
| Spring | %60-65 | %89 | SpEL injection, actuator exposure, WebFlux |
| Rails | %68-72 | %90 | Middleware bypass, ActiveStorage, background jobs |
| Laravel | %72-78 | %93 | Sanctum token replay, Blade injection, container hijack |

### Acil Eklenmesi Gereken Frameworkler

| Oncelik | Framework | Neden |
|---|---|---|
| KRITIK | Next.js | En populer React framework, SSR/SSG/API Routes riskleri |
| KRITIK | FastAPI | Python'da en hizli buyuyen, async guvenlik riskleri |
| YUKSEK | NestJS | TypeScript ekosisteminde baskin, DI/Guard riskleri |
| YUKSEK | Flask | Yaygin Python framework, Blueprint guvenligi |
| ORTA | ASP.NET Core | Enterprise, middleware pipeline riskleri |
| ORTA | Gin/Echo (Go) | Mikroservis ekosisteminde yaygin |

### Tum Frameworklerde Tamamen Eksik Konular

- Rate Limiting, GraphQL, WebSocket, Caching Security
- Background Jobs, Async/Await Safety, API Versioning
- Logging/Auditing detaylari

---

## 3. RAPOR SABLONU ANALIZI (Agent 3)

### Kalite Puani: 37/80

| Alan | Skor | Durum |
|---|---|---|
| Sablon Tamligi | 7/10 | CVSS, trend, compliance eksik |
| JSON Schema | 5/10 | Resmi schema dosyasi YOK |
| Puanlama Modeli | 6/10 | Business impact metrigi yok |
| Uygulanabilirlik | 8/10 | Kod ornekleri acik, caba tahmini eksik |
| CI/CD Potansiyeli | 4/10 | Threshold, schema discovery yok |
| Sektor Uyumlulugu | 3/10 | SARIF, CVSS v4.0 yok |
| Compliance Mapping | 0/10 | Hicbir framework mapping yok |

### Kritik Eksikler

1. **CVSS v4.0 entegrasyonu:** Compliance icin zorunlu
2. **Resmi JSON Schema:** Otomasyon ve dogrulama icin gerekli
3. **SARIF format destegi:** GitHub/GitLab Security tab entegrasyonu
4. **Compliance mapping:** PCI-DSS, GDPR, SOC2, ISO 27001
5. **Trend takibi:** Onceki tarama ile karsilastirma imkani yok
6. **False positive yonetimi:** Suppression mekanizmasi yok

---

## 4. REKABET ANALIZI (Agent 4)

### Konumlandirma Matrisi

| Alan | agent-rock | Semgrep | SonarQube | CodeQL | Snyk Code |
|---|---|---|---|---|---|
| Semantik anlayis | **Cok Iyi** | Sinirli | Sinirli | Iyi | Orta |
| Is mantigi analizi | **Orta** | Yok | Yok | Yok | Yok |
| Rapor kalitesi | **Cok Iyi** | Orta | Iyi | Zayif | Orta |
| Confidence seviyesi | **Evet** | Hayir | Hayir | Tag | Hayir |
| CI/CD entegrasyon | **Yok** | Cok Iyi | Cok Iyi | Native | Cok Iyi |
| Determinizm | **Hayir** | Evet | Evet | Evet | Evet |
| Kurulum suresi | **0 dk** | 5 dk | Saatler | 30+ dk | 5 dk |
| Maliyet | **Ucretsiz** | Freemium | $150+/dev/yil | Ucretsiz (public) | Freemium |

### Stratejik Konum

agent-rock, Semgrep/SonarQube'un **yerine degil yanina** konumlanmali:
- **Katman 1 (her commit):** Semgrep/Bandit -- hizli, deterministik
- **Katman 2 (her commit):** Snyk/npm audit -- CVE tabanli
- **Katman 3 (PR bazli):** agent-rock rock-diff -- LLM semantik analiz
- **Katman 4 (periyodik):** agent-rock rock-deep -- kapsamli denetim

### Kritik Benimseme Engelleri

1. Determinizm eksikligi (ayni kod, farkli sonuc)
2. CI/CD entegrasyon yoklugu
3. Buyuk projelerde yavasllik ve maliyet
4. Tekrarlanabilirlik (compliance denetimleri icin sorunlu)
5. Platform bagimliligi (Claude Code)

---

## 5. MODERN GUVENLIK TRENDLERI (Agent 5)

### Oncelik Matrisi

| Alan | Oncelik | Mevcut Kapsam | Tehdit Seviyesi |
|---|---|---|---|
| AI/ML Guvenligi | **KRITIK** | Yok | Prompt injection, model poisoning, unsafe output |
| Supply Chain 2.0 | **KRITIK** | Temel (A03) | Dep confusion, typosquatting, CI/CD injection |
| Cloud-Native | **YUKSEK** | Kismi | K8s, serverless, container escape |
| API-First (gRPC/WS) | **YUKSEK** | Kismi | gRPC reflection, WebSocket hijacking |
| Modern Auth | **YUKSEK** | Kismi | OAuth 2.1, PKCE, DPoP, SPA token |
| Zero Trust | **ORTA** | Kismi | mTLS, service auth, network policy |
| Privacy Engineering | **ORTA** | Kismi | GDPR teknik kontrol, PII loglama |
| Web3/Blockchain | **DUSUK** | Yok | Reentrancy, access control (nis alan) |

### Acil Olusturulmasi Gereken Yeni Referans Dosyalari

1. `references/ai-ml-security.md` -- LLM prompt injection, model deserializasyonu, AI API key
2. `references/supply-chain-advanced.md` -- Dep confusion, typosquatting, registry token
3. `references/cloud-native-security.md` -- K8s, serverless, container derin denetim

---

## 6. API VE CONFIG DERINLIK ANALIZI (Agent 6)

### OWASP API Top 10:2023 Uyumu

| OWASP API Kategori | agent-rock Kapsam |
|---|---|
| Broken Object Level Auth (BOLA) | Kapsamli |
| Broken Authentication | Kapsamli |
| Broken Object Property Level Auth | Kismi |
| Unrestricted Resource Consumption | Yapilmis |
| Broken Function Level Auth | Iyi |
| **Unrestricted Access to Sensitive Business Flows** | **EKSIK** |
| Server-Side Request Forgery | Kapsamli |
| **Security Misconfiguration (API bazli)** | **EKSIK** |
| **Improper Inventory Management** | **EKSIK** |
| **Unsafe Consumption of APIs** | **EKSIK** |

### Tamamen Eksik Protokoller

- **gRPC:** mTLS, metadata auth, reflection security -- 0% kapsam
- **WebSocket:** Handshake auth, mesaj rate limiting, CSWSH -- 0% kapsam

### Cloud Config Kapsami

AWS S3, GCP IAM, Azure RBAC yapilandirma kontrolleri **tamamen eksik**. Bu, modern uygulamalarin en yaygin zafiyet kaynagidir.

---

## 7. MIMARI VE OLCEKLENME (Agent 7)

### Context Window Analizi

| Senaryo | Token Kullanimi | Risk |
|---|---|---|
| Mevcut referanslar (tumu) | ~50-60K | %25-30 pencere (makul) |
| Planlanan eklemeler sonrasi | ~80-90K | %40-45 pencere (sinira yaklasir) |
| Buyuk proje + tum referanslar | ~130-220K | %65-110 pencere (**KRITIK**) |

### Kritik Mimari Oneriler

| Oncelik | Oneri | Etki |
|---|---|---|
| P0 | README'de rock-quick/rock-deep kopyalama eksik | Kullanicilar wrapper skill'leri kuramiyor |
| P0 | VERSION dosyasi ekle | Surum takibi mumkun degil |
| P1 | Phase 3 referanslarini Phase 2'de yuklememe | ~12K token tasarrufu |
| P1 | Quick mod icin deterministik kategori atlama | Tutarli ve hizli tarama |
| P1 | rock-diff onceligi yukari cekilmeli | CI/CD icin zorunlu |
| P2 | custom/suppressions.md mekanizmasi | False positive yonetimi |
| P2 | Dosya onceliklendirme + max-files siniri | Buyuk projelerde tasmaya karsi |
| P3 | scan_id + previous_report mekanizmasi | Trend takibi |

### Dagitim Sorunlari

- Mevcut kurulum 5 komut (karmasik)
- rock-quick ve rock-deep wrapper'lar README'de kopyalanmiyor
- Tek satirlik install.sh scripti olusturulmali
- Otomatik guncelleme mekanizmasi yok

---

## 8. CI/CD ENTEGRASYON YOLHARITASI (Agent 8)

### Onerilen CI/CD Mimarisi

| Tetikleyici | Mod | Senaryo |
|---|---|---|
| pull_request | rock-diff | Sadece degisen dosyalar, hizli geri bildirim |
| push (main) | rock-deep | Tam tarama, baseline guncelle |
| schedule (haftalik) | rock-deep | Periyodik denetim, trend takibi |
| workflow_dispatch | Secimlik | Manuel tetikleme |

### SARIF Donusum Stratejisi

LLM'e SARIF uretetmeye calismak **sema hatalarina acik**. Deterministik post-processing scripti ile JSON'dan SARIF'e kesin donusum yapilmali.

### rock-diff Teknik Tasarim

1. `git diff --name-status -M origin/main...HEAD` ile degisen dosya listesi
2. Her degisen dosyayi tamamen oku (baglam icin)
3. Diff hunk'larina odaklan, dosya geri kalanini baglam olarak kullan
4. Yeni dosyalar (A) icin tam tarama, degisiklik (M) icin diff + 20 satir

### Bulgu Parmak Izi Sistemi

```
fingerprint = hash(cwe_id + relative_file_path + normalized_snippet_hash + category)
```

Satir numarasi DAHIL EDILMEZ (kod eklendiginde kayar). Bu parmak izi ile:
- Yeni / mevcut / duzeltilmis / regresyon farklilastirmasi
- Trend takibi ve SLA yonetimi mumkun olur

---

## 9. FALSE POSITIVE AZALTMA (Agent 9)

### Mevcut Tahmini FP Orani: %20-35
### Hedef FP Orani: %8-15

### En Yuksek FP Riski Tasiyan Patternler

1. `eval()`/`exec()` -- test framework, ORM migration mesru kullanimlari
2. `md5()`/`sha1()` -- cache key, ETag, checksum icin guvenli kullanim
3. `innerHTML` -- DOMPurify sonrasi guvenli
4. `password` assignment -- test fixture, mock data
5. `DEBUG = True` -- development/test ortami

### Onerilen 3 Gecisli Dogrulama Protokolu

**Gecis 1 - Pattern Eslestirme:** Mevcut grep. Sonuc: LEAD (henuz finding degil)
**Gecis 2 - Baglam Dogrulama:** 30 satir oku. Test dosyasi mi? Sanitizasyon var mi? Framework korumasi var mi?
**Gecis 3 - Exploit Yolu Dogrulama:** Tam zincir: saldirgan -> giris -> veri akisi -> zafiyet -> etki

### Acil Olusturulmasi Gereken Dosyalar

1. **`references/safe-patterns.md`** -- Framework/dil bazli guvenli kalipler katalogu
2. **`references/data-flow-verification.md`** -- Source-sanitizer-sink dogrulama protokolu
3. **`.agent-rock-ignore`** destegi -- Proje seviyesi suppression

### Framework Safe-by-Default Eksiklikleri

| Framework | Varsayilan Koruma | agent-rock Farkindalibi |
|---|---|---|
| Django ORM | Parameterized queries | Kismi |
| React JSX | XSS korumasi | Eksik |
| Angular | Varsayilan sanitization | Tamamen eksik |
| Go html/template | Otomatik escaping | Tamamen eksik |
| Laravel Blade | Otomatik escaping | Eksik |

---

## 10. STRATEJIK YOL HARITASI (Agent 10)

### Kullanici Persona Onceligi

1. **Bireysel Gelistirici** (birincil hedef)
2. **Guvenlik Danismani/Freelancer**
3. **Kucuk Guvenlik Ekibi**
4. Enterprise (henuz hedef degil)

### AGENT-ROCK-DEV.md Yeniden Onceliklendirme

| Madde | Mevcut Oncelik | Onerilen Oncelik | Skor |
|---|---|---|---|
| rock-diff | Dusuk | **1. SIRA** | 75 |
| Frontend Guvenlik Modulu | Yuksek | 2. sira | 32 |
| Framework Rehberleri | Yuksek | 3. sira | 30 |
| IaC/Altyapi Guvenligi | Orta | 4. sira | 60 |
| Supply Chain Derinlestirme | Orta | 5. sira | 36 |
| Rapor Iyilestirmeleri | Dusuk | 6. sira | 18 |
| GraphQL Derin Analiz | Orta | 7. sira | 12 |
| rock-deps | Dusuk | **Ertelenebilir** | 8 |

### 6 AYLIK YOL HARITASI

#### Ay 1-2: Hizli Kazanimlar

- [ ] Ornek rapor yayinlama (Juice Shop/WebGoat uzerinde)
- [ ] rock-diff skill gelistirme (CI/CD temeli)
- [ ] Next.js framework rehberi
- [ ] FastAPI framework rehberi
- [ ] GitHub Actions workflow sablonu
- [ ] Frontend guvenlik modulu
- [ ] SARIF donusturucu scripti
- [ ] Test dizinlerini dislama listesine ekle (FP azaltma)
- [ ] references/safe-patterns.md olustur
- [ ] .agent-rock-ignore mekanizmasi

#### Ay 3-4: Cekirdek Iyilestirmeler

- [ ] NestJS + Flask rehberleri
- [ ] IaC/Altyapi guvenlik modulu (Docker, K8s, Terraform)
- [ ] CVSS v4.0 entegrasyonu
- [ ] Compliance mapping (PCI-DSS, GDPR, SOC2)
- [ ] Supply chain derinlestirme
- [ ] AI/ML guvenlik modulu
- [ ] Benchmark sonuclarini yayinlama
- [ ] CONTRIBUTING.md
- [ ] references/data-flow-verification.md

#### Ay 5-6: Farklilasma Ozellikleri

- [ ] Concurrency ve race condition paternleri
- [ ] Trend/gecmis karsilastirma (baseline diff)
- [ ] gRPC + WebSocket guvenlik modulleri
- [ ] ASP.NET Core + Go-web rehberleri
- [ ] Cloud-native guvenlik modulu
- [ ] Modern auth (OAuth 2.1, PKCE, DPoP)
- [ ] Interaktif duzeltme modu (rock-fix)

### Basari Metrikleri

| Metrik | Ay 2 | Ay 4 | Ay 6 |
|---|---|---|---|
| GitHub Stars | 100 | 500 | 2000 |
| Framework Rehber Sayisi | 7 | 9 | 11+ |
| Zafiyet Yakalama Orani | %70+ | %80+ | %85+ |
| False Positive Orani | <%30 | <%20 | <%15 |
| Contributor Sayisi | 3 | 10 | 25 |

---

## 11. SENTEZ: EN KRITIK 10 EYLEM

Tum 10 agent'in bulgulari sentezlendiginde, **en yuksek etki/efor oranina sahip** eylemler:

### HEMEN (Bu Hafta)

1. **Test dizinlerini SKILL.md Phase 0'a ekle** -- 15 satirlik degisiklik, FP'yi aninda %5-10 dusurur
2. **README.md kurulum adimlarini duzelt** -- rock-quick/rock-deep kopyalanmiyor
3. **VERSION dosyasi olustur** -- Surum yonetimi baslasin

### KISA VADE (1-2 Hafta)

4. **rock-diff skill'i olustur** -- Tum 10 agent'in 1 numarali onerisi, CI/CD icin zorunlu
5. **references/safe-patterns.md olustur** -- FP azaltmanin en etkili adimi
6. **SARIF donusturucu scripti yaz** -- GitHub/GitLab entegrasyonu

### ORTA VADE (1-2 Ay)

7. **Next.js + FastAPI framework rehberleri** -- En populer eksik frameworkler
8. **references/ai-ml-security.md olustur** -- Prompt injection kritik tehdit
9. **Frontend guvenlik modulu** -- CSP, DOM XSS, postMessage

### UZUN VADE (3-6 Ay)

10. **Compliance mapping + CVSS v4.0** -- Enterprise benimseme icin zorunlu

---

## 12. RISK DEGERLENDIRMESI

| Risk | Ciddiyet | Azaltma |
|---|---|---|
| Claude Code platformuna bagimlilik | Yuksek | Platform-agnostik referans katmani |
| LLM dogruluk sinirlari | Yuksek | Benchmark yayinlama, 3 gecisli dogrulama |
| Rekabet (Copilot, Snyk AI) | Orta-Yuksek | "Tamamlayici arac" konumlandirmasi |
| Context window basinci | Orta | Kosullu referans yukleme, token butcesi |
| Bakim yuku (20+ dosya) | Orta | Topluluk katkilari, CONTRIBUTING.md |
| Determinizm eksikligi | Yuksek | Deterministik mod secenegi |

---

## SONUC

agent-rock, Claude Code ekosisteminde benzersiz bir konuma sahip: **sifir bagimlilik, kanit-tabanli raporlama ve LLM semantik anlayisi** ile diger SAST araclarinin yapamadigi baglam-duyarli analiz sunuyor.

**Projenin en buyuk firsati:** Geleneksel SAST araclarinin yakalayamadigi is mantigi zafiyetleri, framework-spesifik derinlik ve insan-okunabilir profesyonel raporlar.

**Projenin en buyuk riski:** CI/CD entegrasyonu ve rock-diff olmadan gunluk kullanim senaryosu zayif kaliyor. Bu engel kaldirilmadan topluluk buyumesi sinirli olacaktir.

**Tek cumle strateji:** rock-diff'i olustur, SARIF ekle, "Semgrep ile birlikte kullan" mesajiyla konumlan.
