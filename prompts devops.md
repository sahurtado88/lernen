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

# Prompt

1. Prompting Without Role or Context

"You are a senior DevOps engineer working with AWS EKS, GitHub Actions, 
and ArgoCD for GitOps. Help me create a deployment pipeline for a 
Node.js microservice that needs..."

2. Overloading the Prompt with Too Many Tasks

Prompt 1: “Create GitHub Actions CI pipeline for Node.js app”
Prompt 2: “Write Jest unit tests for authentication module”
Prompt 3: “Set up Prometheus monitoring for Express API”
One focused task = one useful output.


3. Using Vague Language

Therefore: I started including “slim Docker base”, “must include livenessProbe”, “memory limits specified” in the prompt explicitly.

Now I’m surgical with requirements:

"Optimize this Dockerfile for production by:
- Using alpine base image
- Multi-stage build
- Must include livenessProbe and readinessProbe
- Memory limit: 512Mi max
- Keep these critical dependencies: [specific list]"



5. Ignoring Security / Permissions Requirements

My security-first prompts:

"Create IAM policy for Lambda function with these constraints:
- Least privilege principle only
- NO wildcard (*) permissions
- Read-only access to specific S3 bucket: my-uploads-bucket
- CloudWatch Logs write permissions only"


# 25 prompts

1. The “Explain My CI/CD Pipeline Like I’m a New Hire” Prompt
When your Jenkinsfile has more stages than The Lord of the Rings, this prompt gives you clarity:

“Explain this Jenkinsfile in plain English. Summarize what each stage does, what dependencies it uses, and where potential bottlenecks or redundant steps might be.”

Result: You get a human-readable overview that’s perfect for onboarding or sanity-checking.

2. The “YAML Whisperer”
I’ve lost count of how many hours I’ve wasted debugging whitespace. Now I just drop this in:

“Validate this YAML file. Fix indentation, syntax, and formatting issues while keeping the original logic intact.”

Bonus: Ask it to “reformat to 2-space indentation and alphabetize keys.” The AI will do what linters should’ve done years ago.

3. The “Terraform Doctor”
Terraform can be elegant — or a dumpster fire of duplicated resources. This one cleans it up:

“Review this Terraform code and suggest improvements for DRY principles, modularization, and naming conventions.”

Reality check: It won’t fix your AWS bill, but it’ll stop you from repeating aws_s3_bucket 12 times.

4. The “Incident Translator”
When monitoring tools vomit logs like it’s alphabet soup:

“Summarize this incident log into key causes, affected services, and next steps. Use bullet points.”

It’s like having an ops intern who’s actually helpful.

5. The “Postmortem Summarizer”
No one wants to write postmortems. I get it. So I cheat:

“Turn this incident Slack thread into a structured postmortem with summary, timeline, root cause, and prevention steps.”

The AI makes it readable. You make it sound heroic. Win-win.

6. The “Pipeline Debugger”
When your CI/CD breaks for no reason (which is always):

“Analyze this CI/CD pipeline log. Identify where the failure occurs and suggest possible fixes.”

I’ve used this to spot missing environment variables faster than I could blink.

7. The “Dockerfile Auditor”
AI doesn’t get tired of reading Dockerfiles. You do.

“Review this Dockerfile for security, caching optimization, and image size reduction opportunities.”

It’ll even tell you that using latest tags is lazy—and it’s right.

8. The “Regex Exorcist”
You know that one regex you copied from Stack Overflow in 2018 and never touched again? Let the AI deal with it.

“Explain what this regex does, rewrite it for readability, and provide a test example.”

Result: You finally understand what your own code does.

9. The “Prometheus Alert Whisperer”
Alert rules that scream at 2 AM? Not anymore.

“Review these Prometheus alert rules and suggest threshold improvements to reduce false positives.”

Less noise. More sleep. You’re welcome.

10. The “SRE Therapist”
You can literally paste your rant and get perspective:

“Here’s my current DevOps process. What’s making it inefficient? Suggest automation or process changes.”

Half therapy, half consulting. 100% worth it.

11. The “Ansible Auditor”
Tired of debugging when: conditions that don’t trigger?

“Check this Ansible playbook for logic errors, unnecessary tasks, and better variable usage.”

AI spots the inefficiencies you subconsciously ignore.

12. The “Git Commit Autopsy”
When you inherit a repo full of “fixed stuff” commits:

“Summarize the main changes, risks, and intent of these Git commits.”

Now you actually know what your predecessor did. Or didn’t.

13. The “Security Sanity Check”
Before you deploy that Frankenstein cluster:

“Review this Kubernetes manifest for potential security risks or misconfigurations.”

You’ll be shocked how often it catches public IP exposures you missed.

14. The “CI/CD Optimization Prompt”
AI can literally tune your pipelines:

“Analyze this GitHub Actions workflow and suggest steps to reduce build time and improve caching.”

I’ve shaved minutes off builds using this.

15. The “Kubernetes Oracle”
K8s errors are cryptic. AI isn’t (most of the time):

“Here’s a Kubernetes error log. Explain what it means and how to fix it.”

Because deciphering CrashLoopBackOff at 3 a.m. is not a skill—it's a punishment.

16. The “Bash Beautifier”
For when your shell scripts look like ancient runes:

“Refactor this Bash script for readability, safety, and maintainability.”

It’ll add error handling, comments, and even sanity.

17. The “IaC Refactor Request”
Infrastructure drift happens. AI helps reset:

“Refactor this Terraform or CloudFormation to follow least privilege and best-practice resource naming.”

It’s like having a second pair of eyes — ones that don’t get bored.

18. The “Onboarding Manual Generator”
New teammate joining? Let AI help:

“Generate a step-by-step onboarding guide for a new DevOps engineer based on our CI/CD setup and infra docs.”

Now you don’t have to explain the same thing for the fifth time this month.

19. The “Log Summarizer”
Dump logs in. Get answers out.

“Summarize these application logs by frequency of error and affected endpoints.”

It’s like grep, sort, and awk had a smarter baby.

20. The “Release Notes Assistant”
Stop manually writing release notes:

“Generate a developer-friendly changelog from these commit messages and PR descriptions.”

You’ll sound professional and consistent.

21. The “Alert to Action Translator”
“Convert this alert message into a clear runbook instruction: what to check, where to look, and what likely caused it.”

Perfect for teams that want self-healing systems but aren’t there yet.

22. The “Documentation Generator”
Docs shouldn’t suck. And they don’t have to.

“Generate detailed documentation for this Terraform module or CI/CD pipeline including purpose, variables, and outputs.”

Because no one reads docs — unless they’re good.

23. The “Compliance Checker”
“Review this infrastructure code for compliance gaps (IAM policies, encryption, audit logging). Suggest remediations.”

Your future self will thank you when auditors show up.

24. The “Cost Analyzer”
Cloud bills out of control?

“Estimate cost implications of this Terraform code and suggest optimizations to reduce resource waste.”

It’s not perfect — but it’s a solid sanity check before finance hunts you down.

25. The “Retrospective Prompt”
At the end of a sprint:

“Summarize the wins, blockers, and process improvements from these Slack messages and Jira updates.”

Boom. Retrospective done in 10 minutes.        

#
eres un experto de clase mundial de [TEMA] entrename como si fuera tu aprendiz, desde principiante hasta maestria. Dividelo en etapas, tareas, recursos poco comunes y atajos. Incluye simulaciones o practicas en la vida real para interiorizar verdaderamente cada nivel