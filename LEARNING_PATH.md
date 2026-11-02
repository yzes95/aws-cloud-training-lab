# AWS Learning Path & Study Guide

This document is my personal roadmap for implementing and testing each service in `aws-cloud-training-lab`. 

---

## ⚠️ Cloud Safety & Cost Management
- **Never hardcode AWS keys** in code, git, or `.env` files committed to GitHub.
- **Use LocalStack** (`http://localhost:4566`) for initial offline testing where appropriate.
- When testing on a real AWS account:
  - Create an IAM User with only the specific permissions needed for the lab (never use your root user).
  - Set up an **AWS CloudWatch Billing Alarm** at $5 to catch unexpected usage.
  - Delete or clean up test buckets, parameter store entries, and security groups after running tests.

---

## Order of Work & Modules

### 1. IAM & Least Privilege (`modules/iam/`)
* **Core Concepts:**
  - **Authentication (AuthN - 401)**: Verifying identity (Who are you? e.g., API keys, Cognito tokens).
  - **Authorization (AuthZ - 403)**: Evaluating permissions (What are you allowed to do? e.g., IAM policies).
  - **IAM Users vs IAM Roles**: Permanent long-term credentials (`AKIA...`) vs dynamic short-lived STS credentials (`ASIA...`).
  - **AWS IAM Policy Evaluation**: Default Deny $\rightarrow$ Explicit Allow $\rightarrow$ Explicit Deny overrides all.
  - **Least Privilege**: Avoid wildcards (`Action: "*"` or `Resource: "*"`). Grant only the exact actions on specific ARNs.
* **Suggested boto3 calls:**
  - `sts = boto3.client('sts')` $\rightarrow$ `sts.assume_role(...)`
  - `iam = boto3.client('iam')` $\rightarrow$ `iam.simulate_principal_policy(...)`
* **Verification Check:**
  - Calling `/api/v1/iam/assume-role` returns a temporary session token with expiration.
  - Policy evaluator properly blocks `s3:DeleteObject` when only `s3:PutObject` is allowed.

---

### 2. Secrets & Environment Variables (`modules/secrets_config/`)
* **Core Concepts:**
  - Why plain `.env` files are insecure for production (git exposure risk, visible in server inspection).
  - **SSM Parameter Store**: Hierarchical paths (`/app/env/db/url`), free standard tier, KMS `SecureString` encryption.
  - **AWS Secrets Manager**: Automatic password rotation via Lambda, fine-grained access policies, KMS envelope encryption.
* **Suggested boto3 calls:**
  - `ssm = boto3.client('ssm')` $\rightarrow$ `ssm.get_parameter(Name=..., WithDecryption=True)`
  - `sm = boto3.client('secretsmanager')` $\rightarrow$ `sm.get_secret_value(SecretId=...)`
* **Verification Check:**
  - Successfully fetch and decrypt a database URL from SSM or Secrets Manager.
  - Confirm error handling works if the parameter or secret does not exist (`ParameterNotFound`, `ResourceNotFoundException`).

---

### 3. EC2 & Security Groups (`modules/ec2_security/`)
* **Core Concepts:**
  - **Stateful Security Groups vs Stateless NACLs**: SGs operate at the instance level. When inbound traffic is allowed, return traffic is automatically allowed. NACLs operate at the subnet level and require explicit outbound ephemeral port rules.
  - **Chained Security Groups**: ALB SG allows 443 from `0.0.0.0/0`. EC2 SG allows port 8000 *only* from the ALB SG ID (no hardcoded IPs!). RDS SG allows port 5432 *only* from the EC2 SG ID.
  - **IMDSv2**: Token-based session handshake (`PUT http://169.254.169.254/latest/api/token`) that prevents Server-Side Request Forgery (SSRF) attacks from stealing EC2 IAM role credentials.
  - **Pricing Models**: On-Demand vs Spot (up to 90% savings) vs Reserved Instances / Savings Plans.
* **Suggested boto3 calls:**
  - `ec2 = boto3.client('ec2')` $\rightarrow$ `ec2.describe_security_groups(...)`, `ec2.describe_instances(...)`
* **Verification Check:**
  - Traffic test confirms direct internet traffic to port 8000 is rejected, while traffic originating from the ALB security group is accepted.

---

### 4. Amazon S3 Object Storage (`modules/s3_storage/`)
* **Core Concepts:**
  - **Bucket Security Baseline**: S3 Block Public Access, Default SSE-S3 encryption (AES-256), and Versioning.
  - **Presigned URLs**: Why they are essential for platforms like Ataa. The browser uploads medical reports directly to S3 via an HTTP `PUT` to a signed URL, so large file payloads never travel through the FastAPI backend or consume server memory.
  - **Storage Classes**: Standard $\rightarrow$ Intelligent-Tiering $\rightarrow$ Standard-IA $\rightarrow$ Glacier Flexible $\rightarrow$ Glacier Deep Archive.
  - **Lifecycle Rules**: Automatically transitioning older case files to cheaper archive tiers after 90 or 365 days.
* **Suggested boto3 calls:**
  - `s3 = boto3.client('s3')`
  - `s3.create_bucket(...)`, `s3.put_public_access_block(...)`, `s3.put_object(...)`
  - `s3.generate_presigned_url('put_object', Params={'Bucket': ..., 'Key': ...}, ExpiresIn=900)`
* **Verification Check:**
  - Generate a presigned PUT URL and use `curl` or Postman to upload a file directly to the URL.
  - Verify the object appears in S3 with the configured metadata.

---

### 5. Amazon CloudWatch & Telemetry (`modules/cloudwatch/`)
* **Core Concepts:**
  - **CloudWatch Logs**: Structured JSON log events. Allows querying with CloudWatch Logs Insights (e.g., `fields @timestamp, message | filter level = 'ERROR'`).
  - **Log Retention**: Always set an explicit retention period (e.g., 30 or 90 days) so logs don't accumulate indefinite storage costs.
  - **Custom Metrics & Dimensions**: Pushing business telemetry (`PledgeAmount`, `Category=Medical`) to graph on dashboards.
  - **Metric Alarms**: Monitoring thresholds (e.g., 5xx Error Rate > 5%) and triggering automated notifications via Amazon SNS.
* **Suggested boto3 calls:**
  - `logs = boto3.client('logs')` $\rightarrow$ `logs.put_log_events(...)`
  - `cw = boto3.client('cloudwatch')` $\rightarrow$ `cw.put_metric_data(...)`, `cw.put_metric_alarm(...)`
* **Verification Check:**
  - Stream a structured event and verify it appears in the CloudWatch Log Group.
  - Send custom metric data points and verify the metric name and namespace in CloudWatch.

---

### 6. VPC Basics & Networking (`modules/vpc_networking/`)
* **Core Concepts:**
  - **CIDR & Subnet Division**: e.g., `10.0.0.0/16` VPC divided into `10.0.1.0/24` (Public), `10.0.2.0/24` (Private Compute), `10.0.3.0/24` (Private Data).
  - **The 5 AWS Reserved IPs**: Every subnet reserves 5 addresses (.0 network, .1 router, .2 DNS, .3 future, .255 broadcast). A `/24` subnet provides 251 usable IPs (not 256).
  - **Internet Gateway (IGW) vs NAT Gateway**: IGW connects public subnets to the internet. NAT Gateway sits in a public subnet to allow private compute instances to initiate outbound connections (e.g., `apt-get`, `docker pull`) without accepting incoming internet connections.
  - **S3 VPC Gateway Endpoints**: Free route table entries that route internal VPC traffic directly to S3 over AWS private backbone without passing through a NAT Gateway or public internet.
* **Verification Check:**
  - CIDR calculator returns exactly 251 usable IPs for a `/24` block.
  - Packet route simulator correctly identifies when a NAT Gateway is required vs when an S3 VPC endpoint handles the route for free.

---

### 7. Docker Fundamentals (`modules/docker_lab/`, `Dockerfile`, `docker-compose.yml`)
* **Core Concepts:**
  - **Images vs Containers**: Immutable read-only template vs running isolated process instance.
  - **Multi-Stage Builds**: Build tools in Stage 1; copy only runtime artifacts into Stage 2.
  - **Non-Root Execution**: Adding `USER appuser` to prevent container breakout exploits.
  - **Port Mapping (`-p host:container`)**: Packet routing from host interface to container namespace. Binding to `0.0.0.0` inside container (never `127.0.0.1`).
  - **Persistent Storage**: Docker Volumes vs Bind Mounts vs Ephemeral container layer.
* **Action Items:**
  - [ ] Write `Dockerfile` using Python 3.13-slim and multi-stage build.
  - [ ] Write `docker-compose.yml` to launch FastAPI and optional LocalStack.
  - [ ] Build and test the container: `docker build -t aws-training-api .`
  - [ ] Run container: `docker run -p 8000:8000 aws-training-api`

---

### 8. Advanced Compute & Orchestration (`modules/advanced_compute/`)
* **Core Concepts:**
  - **Compute Decision Matrix**: EC2 (IaaS, full OS control) vs ECS on EC2 (managed container placement) vs ECS Fargate (serverless containers, no server management) vs EKS (enterprise Kubernetes).
  - **ECS Task Definitions**: Defining container images, resource limits (vCPU, RAM), port mappings, and logging drivers.
  - **Task Role vs Execution Role**:
    - `executionRoleArn`: Used by the ECS agent (pull image from ECR, create CloudWatch log streams).
    - `taskRoleArn`: Used by your application code inside the container (call S3, SSM, etc.).
  - **Docker to Kubernetes Analogy**: Container $\rightarrow$ Pod $\rightarrow$ ReplicaSet $\rightarrow$ Deployment $\rightarrow$ Service $\rightarrow$ Ingress.
