1. Design a CI/CD pipeline
Use AI as an architect to sketch and refine your delivery pipeline before touching YAML.​

Prompt template

You are a senior DevOps engineer.
Design a CI/CD pipeline for a <stack> application hosted on <cloud/provider>.
Requirements: <tests, approvals, environments, canary/blue‑green, security checks>.
Output:

High-level pipeline stage.
Recommended tools or services (e.g., GitHub Actions, Argo CD, GitLab CI)
Example pipeline config (YAML) with comments
Use this when starting a new repo, migrating from Jenkins to GitHub Actions, or aligning multiple teams on a single pipeline pattern.​

2. Generate or refactor Terraform
Treat AI as a pair‑programmer for your IaC, especially for repetitive modules and tagging.​

Prompt template

Act as a Terraform and cloud architecture expert.
Goal: <provision X infra> on <AWS/Azure/GCP> following best practices.
Inputs:

Cloud account constraints: <org policies, naming conventions, regions>
Non‑functional: <HA, cost ceiling, compliance requirements>
Tasks:
Generate Terraform resources/modules to meet the goal.
Add standardized tags/labels for cost, owner, environment.
Explain any risky defaults and propose safer alternatives.
Combine this with a second prompt: “Review this Terraform for security, cost, and drift risks” to get an automated IaC review.​

3. Explain and summarize Terraform plans
Turn unreadable terraform plan output into something humans (and product managers) can understand.dev+1​

Prompt template

You are an expert DevOps engineer.
Given this Terraform plan output (JSON if available):

Summarize what will change by resource type and environment.
Highlight destructive actions and their blast radius.
Flag any surprising drift or console‑only changes.
Suggest a checklist to review before applying.
Paste the plan output or a trimmed JSON to get a crisp pre‑change review.​

4. Debug broken CI/CD pipelines
Move from “it failed” to systematic triage by treating AI as a senior SRE in your pocket.

Prompt template

Act as a senior SRE.
My pipeline tool: <Jenkins/GitHub Actions/GitLab CI/Azure DevOps>.
Problem description: <what’s failing>.
Include:

Relevant YAML or pipeline config
Error logs from the failing step
Recent changes (code/config/infrastructure)
Tasks:

Propose the top 3 likely root causes.
Give step‑by‑step debugging actions for each.
Suggest pipeline hardening and automated tests to prevent recurrence.
Use this right after a failure instead of randomly re‑running jobs.​

5. Design Kubernetes deployments and tune manifests
Let AI draft manifests and optimization suggestions, then you review and harden.​

Prompt template

You are a Kubernetes reliability engineer.
Goal: Deploy <service description> on <cluster details: version, CNI, cloud>.
Constraints: <SLOs, autoscaling needs, security baselines, resource limits>.
Tasks:

Propose a Deployment/StatefulSet, Service, HPA, and PodDisruptionBudget.
Recommend requests/limits and HPA targets based on the workload profile.
Add security best practices (runAsNonRoot, read‑only root FS, minimal capabilities).
Output all manifests as YAML with comments.
Pair this with live cluster data or GitOps configs for even better recommendations.​

6. GitOps and environment drift analysis
Use AI as a “GitOps auditor” to compare desired vs. actual state and suggest fixes.​

Prompt template

Act as a GitOps and Kubernetes operator.
Inputs:

Git manifests (desired state)
Cluster description or kubectl get/flux get outputs (actual state)
Tasks:

Identify drift between Git and cluster per resource.
Classify drift: manual console change, autoscaling behavior, or config mismatch.
Recommend remediation steps (revert in Git, import into IaC, or adjust policies).
Suggest alerts or policies to catch similar drift early.
This is powerful in multi‑cluster or multi‑env setups where “ClickOps chaos” creeps in.​

7. Incident triage and runbook drafting
Turn a wall of logs and alerts into a structured incident response and a reusable runbook.​

Prompt template

Act as an on‑call SRE during a production incident.
Context:

Symptoms: <alerts, user impact, error rates>
Logs/metrics traces: <paste key snippets>
Recent changes: <deploys, infra updates, feature flags>
Tasks:

List plausible root causes in order of likelihood.
Propose immediate mitigation steps and safe rollbacks.
Suggest additional diagnostics (queries, dashboards, traces).
Draft a lightweight runbook to handle this incident type in the future.
You can then refine the runbook and store it in your incident management system or wiki.​

8. Generate and refactor automation scripts
Offload boilerplate shell/Python/PowerShell, then have AI refactor and document it.​

Prompt template

You are a DevOps automation engineer.
Goal: Automate <task: log rotation, backups, health checks, etc.> on <OS/cloud>.
Requirements:

Idempotent behavior
Configurable via environment variables
Clear logging and safe error handling
Tasks:

Generate a script in <bash/Python/PowerShell>.
Add inline comments explaining each section.
Propose tests or dry‑run mode for safe verification.
Follow up with “Refactor this script for readability and security” to tighten it.​

9. Cloud cost and FinOps review
Use AI as a cost‑aware architect to scan for obvious waste and unsafe patterns.​

Prompt template

Act as a FinOps and cloud architecture specialist.
Inputs:

High‑level architecture of my environment
Optional: cost explorer export or billing summary
Tasks:

Identify likely cost hotspots (storage, data transfer, over‑provisioned compute).
Suggest right‑sizing, autoscaling, and reservation strategies.
Recommend tagging strategy and dashboards for ongoing cost visibility.
Propose automated policies (e.g., idle resource cleanup) I can implement via IaC.
Run this periodically or after major architecture changes to keep spend in check.

10. DevOps coaching and skills roadmap
Treat AI as your personal DevOps coach to design a pragmatic learning path or adoption plan.​

Prompt template

You are a DevOps coach and trainer.
My current context:

Role and experience: <e.g., backend dev, junior SRE>
Current tooling: <GitHub, Jenkins, Kubernetes, Terraform>
Goals for the next 6 months: <e.g., production‑grade CI/CD, GitOps, observability>
Tasks:

Design a learning roadmap with weekly milestones.
Include hands‑on projects tied to my tech stack.
Suggest how to use AI assistants in each step without creating unsafe shortcuts.
This works well for both individuals and teams planning their DevOps maturity journey.​

Use these as reusable patterns: paste real context (configs, plans, logs, costs) into the prompts, keep security-sensitive details out, and iterate until the output looks like something you would confidently review in a pull request.