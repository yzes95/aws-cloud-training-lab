# AWS Learning Path (Applied to the 2-Endpoint App)

This guide tracks how I connect this 2-endpoint FastAPI app (`GET /health` and `POST/GET /items`) to PostgreSQL and AWS, and how every AWS topic applies to it.

---

## Part 1: What I Write in Code (`db.py`, `aws_services.py`, `main.py`)

### Step 1: Database Connection (`db.py`)
- [ ] Write the SQLAlchemy engine (`pool_pre_ping=True`), session maker, and `Item` model (`id`, `name`, `description`, `s3_file_url`).
- [ ] Implement `check_db_connection()` (`SELECT 1`) and wire it into `GET /health`.
- **Concept covered:** Stateless backend design (app containers hold zero state; all state lives in PostgreSQL/RDS) and handling DB connection drops during RDS Multi-AZ failover.

### Step 2: AWS Runtime Connections (`aws_services.py`)
- [ ] **`get_aws_identity()` (STS):** Call `boto3.client('sts').get_caller_identity()` and return it in `GET /health`.
  - **Concept covered:** Proving the app authenticates via an IAM Role / temporary STS credentials (`ASIA...`) with zero hardcoded keys.
- [ ] **`get_secret()` (Secrets Manager / SSM):** Fetch `DATABASE_URL` from SSM Parameter Store (`WithDecryption=True`) or Secrets Manager at startup.
  - **Concept covered:** Secrets management, KMS encryption, and why plain `.env` files are not used for production secrets.
- [ ] **`upload_to_s3()` (S3):** Upload the file from `POST /items` to S3 (`put_object`) and generate a presigned URL (`generate_presigned_url`).
  - **Concept covered:** Object storage for unstructured files vs relational DB for structured rows, plus temporary presigned access.
- [ ] **`record_cloudwatch_metric()` (CloudWatch):** Push a custom `ItemsCreated` metric on `POST /items`, while structured JSON logs flow to stdout.
  - **Concept covered:** Application observability, custom metrics, and structured logging.

### Step 3: Docker & Local Testing (`Dockerfile`, `docker-compose.yml`, `test_main.py`)
- [ ] Fill in `Dockerfile` (multi-stage build, `python:3.13-slim`, non-root `USER`, `EXPOSE 8000`, `uvicorn` bound to `0.0.0.0`).
- [ ] Fill in `docker-compose.yml` to run the FastAPI container alongside a local `postgres:16-alpine` container with a persistent volume.
- [ ] Write unit tests in `test_main.py` and verify with `pytest`.

---

## Part 2: What I Configure in AWS Around This App (Console / CLI)

Once the container works locally, I deploy and configure AWS around this exact 2-endpoint app:

### 1. IAM & Least Privilege (High Priority)
- [ ] Understand **Authentication (AuthN - 401)** vs **Authorization (AuthZ - 403)**.
- [ ] Create an **IAM Role** for EC2/ECS (Instance Profile / Task Role) instead of using an IAM User with permanent `AKIA...` keys.
- [ ] Attach a **Least Privilege Policy** scoped strictly to:
  - `s3:PutObject` and `s3:GetObject` on `arn:aws:s3:::my-training-s3-bucket/*`
  - `ssm:GetParameter` or `secretsmanager:GetSecretValue` on the single DB secret ARN
  - `cloudwatch:PutMetricData` and `logs:PutLogEvents`
- [ ] Call `GET /health` on the deployed server and confirm `get_caller_identity()` shows the assumed IAM Role ARN.

### 2. VPC & Networking Basics (Medium Priority)
- [ ] Inspect/create a VPC (`10.0.0.0/16`) with **Public Subnets** (for ALB) and **Private Subnets** (for EC2 and RDS).
- [ ] Verify the **5 reserved IPs per subnet** rule (`.0` network, `.1` VPC router, `.2` DNS, `.3` future, `.255` broadcast $\rightarrow$ `/24` = 251 usable IPs).
- [ ] Configure an **Internet Gateway (IGW)** for public subnets and understand when a **NAT Gateway** is needed for private subnets.
- [ ] Add a free **S3 VPC Gateway Endpoint** to the private route table so `upload_to_s3()` reaches S3 privately without NAT Gateway charges.

### 3. EC2, RDS & Chained Security Groups (High Priority)
- [ ] Create three **stateful Security Groups**:
  - `alb-sg`: Inbound `80/443` from `0.0.0.0/0`
  - `ec2-sg`: Inbound `8000` **only** from `alb-sg` (blocks direct internet access to EC2)
  - `rds-sg`: Inbound `5432` **only** from `ec2-sg` (seals the database from the internet)
- [ ] Verify **IMDSv2** on EC2: test fetching the session token via `PUT http://169.254.169.254/latest/api/token`.
- [ ] Provision an **RDS PostgreSQL** instance in the private subnet and connect the app to it.

### 4. High Availability (HA), Elasticity & Disaster Recovery (DR)
- [ ] **ALB (Application Load Balancer):** Point target group health checks to `GET /health`.
- [ ] **ASG (Auto Scaling Group):** Configure min/desired/max capacity across 2 Availability Zones with a CPU target-tracking policy (Horizontal Scaling & Elasticity).
- [ ] **RDS Multi-AZ vs Read Replicas:** Understand synchronous standby failover (~1–2 min RTO, zero committed data loss) vs asynchronous Read Replicas for read scaling/cross-Region DR.
- [ ] **BCP, RPO & RTO:** Map out the 4 DR tiers (*Backup & Restore $\rightarrow$ Pilot Light $\rightarrow$ Warm Standby $\rightarrow$ Multi-Site Active/Active*).

### 5. CI/CD Pipeline (`.github/workflows/ci.yml`)
- [ ] Configure **GitHub OIDC** with AWS IAM (`sts:AssumeRoleWithWebIdentity`) scoped to this repository's `main` branch.
- [ ] Complete `.github/workflows/ci.yml`: run `pytest test_main.py` as a test gate $\rightarrow$ build `Dockerfile` $\rightarrow$ push image to **Amazon ECR**.

---

## Cost & Cleanup Reminder
- Always tear down NAT Gateways, ALBs, EC2 instances, and RDS databases right after testing so they do not bill hourly.
- Keep an AWS Budgets / CloudWatch billing alarm set at $5.
