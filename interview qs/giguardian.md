My name is Sergio Hurtado. I'm an electronic engineer and I've been working in the IT area for about 10 years, in these years, I've gained experience in various IT roles, including software development, database administration, and DevOps.

I’m a DevOps Engineer with around 6 years of experience, mainly focused on cloud infrastructure, automation, and CI/CD.

I have hands-on experience with AWS and Azure, and I’ve worked with tools like Terraform, Ansible, Docker, Kubernetes, Jenkins, Azure DevOps, and GitHub Actions. I also have experience with monitoring tools such as Prometheus and Grafana, and I use Python and Bash for scripting and automation.

Regarding certifications, I’m AWS Solutions Architect – Associate, Microsoft Azure Fundamentals, and HashiCorp Terraform Associate certified.

Throughout my experience, I’ve been focused on automating infrastructure and deployments, improving CI/CD processes, and making environments more reliable and easier to manage.

________  
## DEVSECOPS

# 1
We had repositories and CI/CD pipelines where we needed to improve secret hygiene. We integrated secret detection into the development workflow using Gitleaks. When a potential secret was detected, we first validated whether it was an active credential and assessed its scope and exposure.

The priority was not simply removing the secret from the repository. If the credential was valid, the first action was revocation or rotation.

After that, we migrated the credential to an appropriate secrets-management solution, such as AWS Secrets Manager or protected CI/CD secrets, and updated the application or pipeline to consume the secret securely.

We also automated parts of the remediation workflow, including ticket creation and notifications, so the responsible teams could track remediation.
# 2 What do you do if you find an AWS access key committed to GitHub?

First, I treat the credential as compromised. I identify the credential owner, determine whether it's active, and understand its permissions and potential blast radius.

If it's active, the priority is to revoke or rotate it immediately.

Then I investigate whether the credential was used unexpectedly by reviewing the relevant audit logs, such as CloudTrail.

After containment, I remove the secret from the repository and, depending on the exposure, consider removing it from Git history.

Finally, I move the credential to a proper secrets-management mechanism such as AWS Secrets Manager or GitHub Actions secrets and implement controls to prevent the same issue from happening again.

# 3 If I delete the secret in a new commit, is the problem solved?

Removing the secret from the latest version doesn't remove it from Git history. More importantly, rewriting history doesn't invalidate the credential either. The credential must be considered compromised and rotated or revoked.

# 4 Have you worked with GitGuardian?
My direct hands-on experience has been primarily with Gitleaks and GitHub Enterprise rather than GitGuardian. However, the remediation lifecycle is very similar: detect a potential secret, validate it, determine ownership and exposure, revoke or rotate the credential, remediate the repository, and implement preventive controls

# 5 We have thousands of GitHub repositories and thousands of exposed secrets. How would you approach remediation?
At enterprise scale, I wouldn't treat every finding equally.

First, I would build an inventory of findings and enrich them with context: repository, secret type, credential provider, whether the secret is still valid, repository visibility, age, owner, and potential permissions.

Then I would prioritize remediation based on risk. An active production cloud credential with broad permissions should be handled before an expired token in an archived repository.

Once prioritized, I would map findings to repository or application owners and automate the remediation workflow through ServiceNow.

High-risk active credentials would trigger immediate escalation and rotation, while lower-risk findings could follow standard remediation SLAs.

Finally, I would track metrics such as active secrets discovered, mean time to remediation, recurrence rate, repositories with repeated violations, and percentage of findings remediated within SLA.

# 6 How would you integrate GitGuardian with ServiceNow?
I would avoid simply creating a ServiceNow ticket for every finding because that could generate a huge amount of noise.

I would put an automation layer between the scanner and ServiceNow. That layer could enrich the finding with repository ownership, secret type, validity and severity.

Based on those attributes, it could determine priority and SLA, identify the responsible team and create or update the appropriate ServiceNow ticket.

I would also implement deduplication so repeated detections of the same secret don't create multiple tickets.

# Integration and development

I designed an event-driven integration between GitGuardian and ServiceNow. GitGuardian sends security incident events through a webhook to an AWS API Gateway endpoint. A Lambda function validates and forwards the event to SQS, which decouples the integration and provides retry and DLQ capabilities.

A second Lambda processes the event, checks DynamoDB to avoid duplicate tickets, and creates or updates an incident in ServiceNow through its REST API. Sensitive credentials are stored in AWS Secrets Manager, and the integration only sends metadata about the detected secret, never the secret itself.

The whole infrastructure is deployed with Terraform, following least-privilege IAM and idempotency principles.

## For an interview, an even more natural short version would be:

I built an automated workflow where GitGuardian detects exposed secrets and automatically creates or updates ServiceNow incidents. I used API Gateway, Lambda, SQS, DynamoDB, and Secrets Manager, all deployed with Terraform. The main goals were reliability, deduplication, security, and making sure no actual secrets were copied into ServiceNow.

# A development team refuses to remediate a secret because rotating it might break production. What do you do?"

First I would understand the dependency and business impact. But if the credential is confirmed to be exposed and active, we need to treat it as compromised.

I would work with the application owner to create a safe rotation plan—for example introducing the new credential first, validating the application, switching consumers, and then revoking the old credential.

For highly privileged credentials, the security risk may require immediate revocation and incident escalation.

The decision should be risk-based rather than simply security versus development.

# DevSecOps / Secrets Management Interview Questions

## 1. What happens when a secret is committed to Git? Why isn't deleting the secret enough?

**Interview answer:**

> Once a secret is committed to Git, I consider it compromised. Deleting it from the current version of the file is not enough because Git keeps previous commits, branches, tags, forks, clones, caches, and potentially CI artifacts. My first action would be to revoke or rotate the credential, then assess exposure and usage, and only after that clean the Git history if required.

**Key point:** Rotation is more important than history rewriting.

Cleaning Git history does not make an already exposed credential safe again.

---

## 2. How would you rotate an AWS access key?

**Interview answer:**

> If I suspect compromise, I would first create or activate a replacement credential where operationally necessary, update the application or secret manager, validate that the new credential works, and then deactivate and delete the old access key. If the key is actively compromised, containment takes priority and I may disable it immediately. I would also investigate CloudTrail for suspicious activity.

Typical flow:

```text
Create replacement → update workload → test → deactivate old key → monitor → delete
```

For a leaked key, containment may require disabling or revoking it immediately.

---

## 3. What is GitHub Secret Scanning?

**Interview answer:**

> GitHub Secret Scanning detects credentials such as API keys and tokens committed to repositories. It can scan Git history and generate alerts when supported secret patterns are detected. Combined with push protection, GitHub can also block supported secrets before they are pushed.

---

## 4. Gitleaks vs GitGuardian?

**Interview answer:**

> Gitleaks is primarily an open-source secret scanning engine that is easy to integrate into developer workflows and CI/CD. GitGuardian is a broader secrets-security platform providing centralized incident management, remediation workflows, integrations, analytics, validity checks, and enterprise visibility. I might use Gitleaks when I need a lightweight scanner, and GitGuardian when I need centralized governance and remediation at organization scale.

Do not say one is simply "better". They partially solve different problems.

---

## 5. What is a GitHub PAT?

**Interview answer:**

> A GitHub Personal Access Token, or PAT, is a credential that can be used instead of a password to authenticate to GitHub, for example through the API or command line. Because it is a bearer credential, it should be protected like a password and granted only the permissions required.

---

## 6. Classic PAT vs fine-grained PAT?

**Interview answer:**

> Classic PATs use broader scopes and can potentially provide access to many repositories. Fine-grained PATs let us restrict the token to specific resource owners, repositories, and permissions, so I prefer fine-grained tokens when the required GitHub functionality supports them.

For machine-to-machine automation, I would also evaluate a GitHub App instead of automatically using a PAT.

---

## 7. How do you prevent secrets from being committed?

**Interview answer:**

> I use defense in depth: secret managers instead of hardcoded credentials, short-lived identities where possible, developer education, pre-commit scanning, IDE or local scanning, GitHub push protection, CI scanning, and organization-level repository scanning.

Example strategy:

```text
Secret Manager → local detection → push protection → CI scanning → continuous scanning
```

---

## 8. Pre-commit scanning vs CI scanning?

**Interview answer:**

> I use both. Pre-commit scanning gives developers fast feedback and prevents many secrets from ever leaving the workstation. CI scanning provides centralized enforcement and cannot be avoided simply because a developer forgot to install a hook. Pre-commit improves developer experience; CI provides a stronger organizational control.

**Key point:** Local controls are preventive but not sufficient enforcement.

---

## 9. What would you do with false positives?

**Interview answer:**

> First I would validate that the finding is genuinely a false positive rather than assuming it is. Then I would suppress it as narrowly as possible using an allowlist, rule exception, fingerprint, path, or detector configuration, and document the reason. I would avoid globally disabling an entire detector because of a few false positives.

Good phrase:

> I optimize detection rules, not security away.

---

## 10. How do you prioritize thousands of findings?

**Interview answer:**

> I would use risk-based prioritization instead of FIFO. I would prioritize valid and active credentials, publicly exposed secrets, production credentials, cloud credentials with high privileges, secrets with evidence of usage, and repositories containing critical applications.

Example model:

```text
Risk = validity × exposure × privilege × environment × asset criticality × age/usage
```

Example priority:

- **P0:** Active AWS admin credential exposed publicly
- **P1:** Production credential in private repo
- **P2:** Non-production valid credential
- **P3:** Inactive/test credential or likely false positive

---

## 11. How do you determine repository ownership?

**Interview answer:**

> I would not rely on repository name alone. I would combine CODEOWNERS, repository teams, GitHub permissions, recent contributors, service catalogs such as Backstage or ServiceNow CMDB, deployment metadata, Terraform ownership, and organizational mappings. When those disagree, I would define an authoritative ownership source.

Good phrase:

> Ownership is a data-quality problem as much as a security problem.

---

## 12. How would you integrate a security scanner with ServiceNow?

**Interview answer:**

> I would consume scanner events through a webhook or API, normalize them into an internal finding schema, enrich them with repository owner, application, environment, severity and credential metadata, and then use the ServiceNow API to create or update the appropriate incident or vulnerability record.

Example architecture:

```text
Scanner → webhook/event → enrichment service → deduplication → ServiceNow API
```

At scale, I would avoid tightly coupling the scanner directly to ServiceNow.

---

## 13. How would you prevent duplicate ServiceNow tickets?

**Interview answer:**

> I would create a deterministic fingerprint for each security incident and store the relationship between that fingerprint and the ServiceNow record. Before creating a ticket, the integration checks whether an open ticket already exists and updates it instead.

Example:

```text
fingerprint =
hash(
  organization +
  repository +
  detector_type +
  secret_fingerprint
)
```

Do not use the real secret value inside the fingerprint or logs.

---

## 14. How would you define remediation SLAs?

**Interview answer:**

> I would define SLAs based on risk rather than having one SLA for every finding. A publicly exposed active production credential should be revoked immediately, while an inactive credential in a private development repository can have a longer remediation window.

Example:

| Risk | Example | Target |
|---|---|---|
| Critical | Public + active + production/admin | Immediate / hours |
| High | Active production secret | <24h |
| Medium | Active non-prod/private | Few days |
| Low | Inactive/test/low-risk | Planned backlog |

Important distinction:

**Containment SLA ≠ full remediation SLA**

---

## 15. What metrics would you present to security leadership?

**Interview answer:**

> I would avoid focusing only on the number of detected secrets because that can be misleading. I would present exposure, remediation performance, recurrence and prevention metrics.

Useful metrics:

- Active secrets exposed
- Critical/high findings
- Mean/median time to revoke
- Mean time to remediate
- SLA compliance
- Findings by business unit
- Repeat offenders / recurrence rate
- New leaks per week
- Percentage blocked before commit/push
- Secret age
- Number of publicly exposed credentials
- Percentage using temporary credentials versus long-lived credentials

Strong leadership metric:

> How many valid high-risk credentials remain exposed, and for how long?

---

## 16. How do you handle a secret found in Git history?

**Interview answer:**

> First I assume the secret may have been copied and rotate or revoke it. Then I determine its validity, scope and exposure, investigate usage, and update all dependent applications. If required, I rewrite the Git history and coordinate force pushes or repository cleanup, but history rewriting is secondary because it cannot invalidate copies that already exist.

Correct order:

```text
Revoke → investigate → replace → clean history
```

Not:

```text
Delete commit → assume safe
```

---

## 17. How would you investigate whether an exposed AWS credential was abused?

**Interview answer:**

> I would identify the AccessKeyId and investigate AWS CloudTrail for API activity associated with that credential. I would establish when the credential became exposed and compare that against CloudTrail events, looking at API calls, source IPs, regions, user agents, services, resources accessed, failed authorization attempts, and unusual behavior.

Then I would check whether new IAM users, roles, policies, access keys, persistence mechanisms or resources were created, and investigate potential data access or exfiltration.

Strong incident-response sequence:

```text
Disable credential → preserve evidence → CloudTrail investigation → scope blast radius → remediate persistence
```

---

## 18. How do you implement least privilege?

**Interview answer:**

> I start with no access and grant only the actions, resources and conditions required by the workload. In AWS I prefer IAM roles and temporary credentials over long-lived IAM user access keys. I continuously review actual usage and remove permissions that are no longer needed.

Useful concepts:

- IAM roles
- Resource-level permissions
- IAM conditions
- Permission boundaries
- SCPs as guardrails
- Temporary STS credentials
- IAM Access Analyzer
- Separation between human and workload identities

---

## 19. How would you secure the credentials used by your remediation automation itself?

**Interview answer:**

> Ideally, the remediation automation should not have long-lived static credentials at all. I would use workload identity and short-lived credentials—for example an AWS IAM role through OIDC or the native identity mechanism of the platform running the automation.

Then:

> The automation would receive narrowly scoped permissions, with separation between detection and destructive remediation actions, auditable API calls, approval gates for high-impact operations, and credentials stored in a managed secrets system only when unavoidable.

Example architecture:

```text
GitHub Actions
      │
      │ OIDC
      ▼
AWS STS
      │
      ▼
Temporary role credentials
      │
      ▼
Limited remediation actions
```

Avoid permanent credentials such as:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

inside the same system responsible for remediating leaked secrets.

---

# Reusable Interview Framework

When discussing a secrets incident, structure the answer as:

## 1. Contain

Revoke or disable the credential.

## 2. Assess

Determine whether it is valid, whether it is production, whether exposure was public, and what permissions it has.

## 3. Investigate

Review logs, CloudTrail, Git history, and actual usage.

## 4. Remediate

Replace the credential, update applications, and clean Git history if required.

## 5. Prevent recurrence

Use secret managers, short-lived identities, pre-commit scanning, push protection, CI scanning, and continuous monitoring.

A strong closing phrase:

> A leaked credential is an identity incident, not just a code-quality finding. My priority is invalidating the identity and determining the blast radius, not simply removing the string from Git.
