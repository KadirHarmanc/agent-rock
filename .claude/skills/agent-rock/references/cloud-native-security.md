# Cloud-Native & Infrastructure Security Reference

Use this reference when the project contains Docker, Kubernetes, Terraform, CloudFormation,
serverless configurations, or other infrastructure-as-code. These files define deployment
security posture and are often overlooked in application-focused audits.

## Detection

Infrastructure code is present when you see:
- `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- `k8s/`, `kubernetes/`, `deploy/`, `helm/`, `charts/`
- `*.tf`, `*.tfvars`, `terraform.tfstate`
- `template.yaml` (SAM), `serverless.yml`, `cloudformation.json`
- `kustomization.yaml`, `skaffold.yaml`
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`

---

## Category 1: Dockerfile Security

```
Grep: ^FROM
Grep: ^USER
Grep: ^RUN.*apt-get|yum|apk
Grep: ^COPY|^ADD
Grep: ^ENV
Grep: ^EXPOSE
Grep: ^ARG
```

Check:
- **Running as root**: No `USER` directive or `USER root` → container runs as root
- **Unpinned base images**: `FROM node:latest` or `FROM python` → supply chain risk
- **Secrets in build**: `ARG PASSWORD`, `ENV API_KEY=...`, `COPY .env` → secrets in image layers
- **ADD with remote URL**: `ADD http://...` → untrusted content download
- **Missing .dockerignore**: `.env`, `.git`, `node_modules` copied into image
- **Package manager cache**: `RUN apt-get install` without `--no-install-recommends` and cleanup
- **Multi-stage leaks**: Secrets used in build stage without multi-stage separation
- **Unnecessary capabilities**: Missing `--cap-drop=ALL` in runtime config
- **HEALTHCHECK missing**: No health check defined (denial of service)

**Safe patterns:**
- `FROM image:tag@sha256:...` — pinned by digest
- `USER nonroot` or `USER 1000` — non-root execution
- Multi-stage build with secrets only in builder stage
- `COPY --from=builder` only copying artifacts

---

## Category 2: Docker Compose Security

```
Glob: **/docker-compose*.yml
Glob: **/compose*.yml
```

Check:
- **Privileged mode**: `privileged: true` → full host access
- **Host network**: `network_mode: host` → bypasses network isolation
- **Dangerous volumes**: Mounting `/`, `/etc`, `/var/run/docker.sock`
- **Exposed ports**: Ports bound to `0.0.0.0` instead of `127.0.0.1`
- **Env files committed**: `env_file: .env` with `.env` in git
- **No resource limits**: Missing `mem_limit`, `cpus` → resource exhaustion
- **Default bridge network**: No custom network isolation between services
- **Capability additions**: `cap_add` without `cap_drop: [ALL]`

---

## Category 3: Kubernetes Security

```
Grep: kind:\s*(Deployment|Pod|StatefulSet|DaemonSet|Job|CronJob)
Grep: securityContext
Grep: serviceAccountName
Grep: hostNetwork|hostPID|hostIPC
Grep: privileged
Grep: readOnlyRootFilesystem
Grep: runAsNonRoot
```

### Pod Security
Check:
- **Running as root**: Missing `runAsNonRoot: true` or `runAsUser: 0`
- **Privileged containers**: `privileged: true` in security context
- **Host namespaces**: `hostNetwork`, `hostPID`, or `hostIPC: true`
- **Writable root filesystem**: Missing `readOnlyRootFilesystem: true`
- **No resource limits**: Missing `resources.limits` (CPU, memory)
- **Default service account**: No `serviceAccountName` specified or using `default`
- **Capability escalation**: `allowPrivilegeEscalation: true` or not set to false
- **Missing security context**: No `securityContext` at pod or container level

### RBAC
```
Grep: kind:\s*(Role|ClusterRole|RoleBinding|ClusterRoleBinding)
Grep: verbs:.*\*
Grep: resources:.*\*
Grep: apiGroups:.*\*
```

Check:
- **Wildcard permissions**: `verbs: ["*"]` or `resources: ["*"]`
- **ClusterRole with excessive permissions**: Broad access across namespaces
- **Secrets access**: Roles granting `get`/`list` on secrets without need
- **Binding to default service account**: Elevated permissions on default SA

### Secrets Management
```
Grep: kind:\s*Secret
Grep: stringData|data:
Grep: valueFrom.*secretKeyRef
```

Check:
- **Secrets in plain YAML committed to git** → use external secrets manager
- **Secrets as environment variables** → prefer volume mounts (env vars leak in logs/debug)
- **No encryption at rest**: Check for `EncryptionConfiguration`

### Network Policy
```
Grep: kind:\s*NetworkPolicy
Grep: ingress:|egress:
```

Check:
- **No NetworkPolicies defined** → all pod-to-pod traffic allowed
- **Overly permissive policies**: Allowing all ingress or all egress
- **Missing egress restrictions**: Pods can reach internet and internal services

---

## Category 4: Terraform Security

```
Glob: **/*.tf
Glob: **/*.tfvars
```

### Cloud Storage
```
Grep: aws_s3_bucket|azurerm_storage_account|google_storage_bucket
Grep: acl.*public|public_access
Grep: block_public
```

Check:
- **Public S3 buckets**: `acl = "public-read"` or missing `block_public_acls`
- **Missing encryption**: No `server_side_encryption_configuration`
- **No versioning**: Missing `versioning { enabled = true }`
- **No access logging**: Missing `logging` configuration

### Security Groups / Firewall
```
Grep: aws_security_group|azurerm_network_security_group|google_compute_firewall
Grep: 0\.0\.0\.0/0|::/0
Grep: from_port.*0.*to_port.*65535
```

Check:
- **Open to world**: Ingress from `0.0.0.0/0` on sensitive ports (SSH, DB, admin)
- **All ports open**: Port range `0-65535` on any ingress rule
- **Missing egress restrictions**: Default allow-all outbound

### IAM
```
Grep: aws_iam_policy|aws_iam_role|azurerm_role_assignment|google_project_iam
Grep: \*.*Action|actions.*\*
Grep: arn:aws:iam::.*:policy/Admin
```

Check:
- **Wildcard actions**: `"Action": "*"` or `"Action": "s3:*"`
- **Admin policy attachment**: Using `AdministratorAccess` instead of least privilege
- **Missing conditions**: No IP restriction or MFA condition on sensitive operations
- **Cross-account access**: Overly broad trust relationships

### State Management
```
Grep: terraform\.tfstate
Grep: backend.*s3|backend.*gcs|backend.*azurerm
```

Check:
- **State file in git**: `terraform.tfstate` committed (contains secrets)
- **Unencrypted state backend**: Remote state without encryption
- **No state locking**: Missing DynamoDB table or equivalent for lock

### Secrets in Terraform
```
Grep: password.*=.*"
Grep: secret.*=.*"
Grep: api_key.*=.*"
Grep: \.tfvars
```

Check:
- **Hardcoded secrets in `.tf` files**: Passwords, API keys as string literals
- **Secrets in `.tfvars` committed to git**
- **Sensitive variables without `sensitive = true`**: Values appear in plan output

---

## Category 5: Serverless Security

```
Glob: **/serverless.yml
Glob: **/template.yaml
Glob: **/sam.yaml
```

Check:
- **Overly permissive IAM**: Lambda role with `*` resource or `*` action
- **Secrets in environment**: API keys in `environment:` section of config
- **No function timeout**: Missing timeout allows runaway execution costs
- **Public API without auth**: API Gateway endpoints without authorizer
- **Missing VPC**: Lambda accessing internal resources without VPC placement
- **Event injection**: Untrusted event data (SNS, SQS, S3) used without validation
- **Dependency layer risks**: Lambda layers from untrusted sources

---

## Category 6: CI/CD Pipeline Security

```
Glob: **/.github/workflows/*.yml
Glob: **/.gitlab-ci.yml
Glob: **/Jenkinsfile
Glob: **/bitbucket-pipelines.yml
Grep: pull_request_target
Grep: workflow_dispatch
```

### GitHub Actions
Check:
- **`pull_request_target` with checkout of PR code**: Code execution from fork PRs
- **Script injection**: `${{ github.event.*.title }}` or similar in `run:` steps
- **Excessive permissions**: `permissions: write-all` or missing restrictions
- **Secrets in logs**: `echo ${{ secrets.* }}` or debug mode enabled
- **Unpinned actions**: `uses: action@main` instead of `action@sha256`
- **Self-hosted runners**: Accepting PRs from forks on self-hosted runners

### General CI/CD
Check:
- **Secrets as environment variables**: Visible in build logs
- **No branch protection**: Deployment from any branch
- **Missing approval gates**: Auto-deploy to production
- **Build cache poisoning**: Cache shared across untrusted branches

---

## Common False Positive Filters

- Development-only docker-compose with privileged mode → check if separate from production
- Terraform modules in `examples/` directory → not deployed
- Kubernetes manifests with comments indicating TODO → note but don't inflate severity
- CI/CD secrets accessed via `${{ secrets.* }}` (GitHub) → properly managed, not hardcoded
- Terraform state backend already configured with encryption → safe
