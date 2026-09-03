# Question 1

“Hi Sergio, thanks for joining. Could you start by telling me a little about yourself and your background?”

I'm an Infrastructure and DevOps Engineer with more than nine years of experience in IT, including around five years focused specifically on cloud infrastructure and DevOps.

In my current role at Globant, I work mainly with AWS infrastructure, including IAM, EC2, VPC networking, and Linux environments. I also work with Terraform, Python, Bash, Kubernetes, monitoring, and production support.

A significant part of my role involves troubleshooting infrastructure, networking, and access issues, supporting engineering teams, handling operational requests and incidents, and automating repetitive tasks.

Before Globant, I worked at Bancolombia, where I gained experience with Ansible, CI/CD, Docker, AWS, and infrastructure automation.

What interests me about this role is the combination of AWS infrastructure, troubleshooting, operational support, and automation, because those are all areas I’ve been working with directly.

# Question 2

“Can you tell me about a recent infrastructure issue you had to troubleshoot? What was the problem, and how did you approach it?”

We had an issue where the Terraform state became inconsistent with the actual infrastructure.

The first thing I did was stop any further Terraform applies to avoid making the situation worse. Then I reviewed the state and compared it with the resources that actually existed in AWS.

We identified that some resources were no longer correctly represented in the state. Before making any changes, we created a backup of the current state and reviewed the available recovery options.

We restored the correct state information and then ran a Terraform plan to validate that Terraform was no longer proposing unexpected changes or resource destruction.

After confirming that the plan was clean, we resumed the normal deployment process.

# Question 3

“How do you decide whether to resolve an infrastructure issue yourself or escalate it to another team?”

The first thing I do is assess the blast radius and impact of the issue to determine its priority.

Then I evaluate whether I can resolve it safely without creating downtime or affecting other services or customers.

I also check whether the affected resource is owned by my team or by another team.

If the issue is within my scope and I understand the remediation, I try to resolve it directly. If it involves a high-risk change, another team's ownership, or requires deeper expertise, I escalate it with clear context about the impact, what I already checked, and the evidence I collected.

# Question 4

“Imagine another engineering team reports that an EC2 instance cannot connect to a service in another VPC. How would you troubleshoot that?”

First, I would confirm which VPC the EC2 instance is in and which VPC hosts the destination service.

Then I would verify how both VPCs are connected, for example through VPC peering or a Transit Gateway.

After that, I would review the route tables on both sides to make sure the traffic has a valid route.

I would also check the security groups and network ACLs to verify that the required source, destination, and port are allowed.

If DNS is involved, I would also validate that the hostname resolves correctly.

Finally, I would confirm that the destination service is actually healthy and listening on the expected port.

# Question 5

“How would you handle an IAM access request from an engineer who says they need administrator permissions to troubleshoot an issue?”

I would not grant administrator permissions by default because that would violate the principle of least privilege.

First, I would understand exactly what the engineer needs to troubleshoot and which AWS services or resources are involved.

Then I would provide only the permissions required for that specific task, ideally using an existing role or a scoped policy rather than broad administrative access.

If elevated access is really necessary, I would follow the security and approval process and make sure the access is temporary and auditable.

# Question 6

“Can you describe your experience with Terraform and how you normally manage infrastructure changes?”

I have around three years of hands-on experience with Terraform. I've created and used different Terraform modules to provision infrastructure in AWS.

When managing infrastructure changes, I normally review the Terraform plan carefully before applying anything. I use the plan to understand exactly which resources will be created, modified, or destroyed, and to identify changes that could cause downtime or affect persistent data.

I also prefer to manage Terraform changes through Git and pull requests, so the changes can be reviewed before they are applied.

For higher-risk changes, I make sure we understand the impact and have a rollback or recovery strategy before proceeding.

# Question 7

“I see you have experience with Terraform. Have you worked with Spacelift before?”

I haven't worked with Spacelift directly yet. My experience is mainly with Terraform and Git-based infrastructure workflows, including reviewing plans and managing infrastructure changes through pull requests.

So while I would need to learn the Spacelift-specific workflow, the underlying Terraform and IaC concepts are already familiar to me.

# Question 8

“This role involves handling a queue of infrastructure requests and tickets. How do you prioritize several requests coming in at the same time?”
To prioritize requests, I first evaluate urgency and impact.

A production issue or a security-related request would normally have the highest priority. I also consider whether another engineering team is completely blocked and whether there is a workaround available.

For non-critical requests, I look at deadlines, business impact, and the complexity of the change.

My goal is to address the highest-impact issues first while keeping the other teams informed about the status of their requests.

# Question 9

“Can you give me an example of a repetitive operational task that you automated?”

One example was automating the creation of GitHub repositories using the GitHub CLI.

Before the automation, repository creation and permission assignment required manual steps.

I created a process using the GitHub CLI to create the repository and assign the required permissions to users automatically.

This reduced repetitive manual work and made the process more consistent.

# Question 10

“What are you looking for in your next role, and why are you considering a change?”

I'm looking for a new challenge where I can continue growing as an infrastructure engineer while staying hands-on.

I'm especially interested in roles where I can work with AWS, Terraform, troubleshooting, automation, and support other engineering teams.

What attracted me to this position is the infrastructure foundations focus and the opportunity to improve operational processes and reduce repetitive work through automation.

# Question 11

“What would you say is one area where you still want to improve technically?”

I would like to continue deepening my AWS knowledge, especially in more advanced architecture and infrastructure topics.

I already have the AWS Solutions Architect Associate certification, and one of my next goals is to prepare for a Professional-level AWS certification.

I see that as a way to strengthen both my theoretical knowledge and the decisions I make when designing and troubleshooting infrastructure.

# Question 12

“Do you have any questions for me about the role or the team?”

Yes, I have a couple of questions. First, how does the Infra Foundations team typically work day to day? Do you follow Scrum, Kanban, or another way of organizing operational and project work?

Second, I'd like to understand the scope of the platform a little better. Approximately how many engineering teams depend on the infrastructure and services managed by the Infra Foundations team?

# Question 13 

error tfstate

First, I would stop any Terraform applies to avoid making the state inconsistent while troubleshooting.

Then I would identify what actually happened: whether the state is corrupted, stale, locked, or simply out of sync with the real infrastructure.

I would pull a copy of the current remote state and make a backup before making any changes.

If the backend supports state versioning or snapshots, I would prefer restoring a known good version instead of manually editing the state.

If the infrastructure still exists but Terraform has lost the mapping, I would use Terraform state commands or import the resources back into the state rather than recreating them.

Only as a last resort would I use terraform state push, because it overwrites remote state and HashiCorp considers it a dangerous operation.

After recovery, I would run a Terraform plan and carefully verify that Terraform is not proposing unexpected resource destruction or recreation before allowing any apply.