# AWS Secrets Manager Activation Day Workshop

### AWS Secrets Manager Overview

- Managed service for storing, retrieving, and rotating database credentials, API keys, and other secrets
- Built on secure S3 storage with fine-grained access control
- Automatic rotation via service integration (RDS/Redshift) or Lambda functions
- API/SDK access eliminates human password lookups
- Strong auditing through CloudWatch and CloudTrail
- Multi-region replication for high availability

### Primary Use Cases

- Enterprise Java applications
  - Service credentials stored in Secrets Manager
  - Runtime retrieval via get_secret_value API
  - No hardcoded credentials in applications
- API key management
  - Client ID + client secret storage
  - Prevents accidental commits to source control
  - Zero application redeployment for key changes
- SSH private keys
  - Lambda functions accessing external services via SCP
  - Keys retrieved at runtime, not bundled
  - Full audit trail via CloudTrail

### Secret Lifecycle Management

- Classification priorities: IAM keys → SSH keys → database credentials
- Recommended approaches:
  1. IAM access keys: Replace with IAM roles
  2. SSH keys: Move to immutable infrastructure or SSM sessions
  3. Database credentials: Use Secrets Manager with rotation
- Encryption via AWS KMS with unique data keys per secret version
- VPC endpoints for private network access only
- Resource policies restrict access to specific VPC endpoints

### Rotation Strategies

- Single user rotation
  - One credential set, brief downtime risk during rotation
  - Schedule during maintenance windows
  - Include retry logic in applications
- Multi-credential rotation
  - Clone user created automatically
  - Alternating password updates (e.g., every 45 days for 90-day policy)
  - Zero downtime approach
- Rate-based or cron-based scheduling options
- Up to 100 versions maintained per secret

### Access Control Best Practices

- Principle of least privilege with separated permissions:
  - Admin: Create/store secrets, configure rotation
  - Application: Retrieve secrets only
- Use tags for ABAC (Attribute-Based Access Control)
- Hierarchical naming: environment/application/database
- Meaningful descriptions with ownership details
- Resource-based policies for cross-account access in centralized models

### Multi-Account Architecture

- AWS recommends decentralized approach
  - Secrets stored in same account as applications
  - Reduces blast radius if account compromised
  - Distributes API call costs across accounts
  - Eliminates complex cross-account IAM policies
- Multi-region replication maintains common names
- Automatic propagation of updates to replica regions
- Supports disaster recovery scenarios

### Recent Features & Enhancements

- Fully managed database admin secrets
  - Direct RDS/Redshift integration (no Lambda required)
  - Faster response times, guaranteed success
- Batch secret retrieval
  - Get up to 10 secrets in single API call
  - Reduces costs (charged per 10,000 API calls)
- IAM Roles Anywhere for on-premises integration
  - LEAF certificates for temporary authentication
  - Extends AWS IAM to non-AWS workloads

### Workshop Details

- 72-hour access to hands-on labs
- Pre-provisioned sandbox environment
- Architecture: Web app → Secrets Manager Agent → MySQL RDS
- Performance comparison with/without caching agent
- Self-paced modules covering all discussed topics
- Principle of least privilege enforced in lab environment