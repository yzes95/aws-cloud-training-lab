from typing import Any, Dict, List
from .schemas import (
    IMDSRequest,
    IMDSResponse,
    TrafficTestRequest,
    TrafficTestResponse,
)


class EC2SecurityService:
    """Service providing hands-on training for EC2, Security Groups, and IMDSv2."""

    def test_security_group_traffic(self, req: TrafficTestRequest) -> TrafficTestResponse:
        """Simulates AWS Security Group stateful filtering rules across the architecture:
        - Ingress to ALB: Port 443 allowed from 0.0.0.0/0
        - Ingress to EC2: Port 8000 allowed ONLY from ALB-SG. Port 22 allowed ONLY from Admin Bastion IP.
        - Ingress to RDS: Port 5432 allowed ONLY from EC2-SG.
        """
        source = req.source.strip().lower()
        target = req.destination_target.strip().upper()
        port = req.destination_port
        protocol = req.protocol.strip().lower()

        allowed = False
        sg_name = ""
        rule = None
        explanation = ""
        arch_note = ""

        if target == "ALB":
            sg_name = "sg-alb-public-ingress"
            if port in [80, 443] and protocol == "tcp":
                allowed = True
                rule = f"Inbound Allow TCP {port} from 0.0.0.0/0"
                explanation = "ALB is public-facing. Port 443 is open to the internet for client HTTPS requests."
            else:
                allowed = False
                explanation = f"Port {port} is closed on ALB. ALB only accepts HTTP (80) or HTTPS (443)."
            arch_note = "ALB terminates SSL and offloads cryptographic load from the backend compute instances."

        elif target == "EC2":
            sg_name = "sg-ec2-app-tier"
            if port == 8000 and ("alb" in source or "sg-alb" in source):
                allowed = True
                rule = "Inbound Allow TCP 8000 from sg-alb-public-ingress"
                explanation = "Traffic from ALB Security Group is permitted on internal application port 8000."
            elif port == 22 and ("admin" in source or "bastion" in source or "10.0.0." in source):
                allowed = True
                rule = "Inbound Allow TCP 22 from Admin Bastion IP only"
                explanation = "SSH management port 22 is strictly restricted to internal Bastion/VPN."
            elif "internet" in source or "0.0.0.0" in source:
                allowed = False
                explanation = (
                    "BLOCKED: EC2 Security Group drops direct traffic from the internet! "
                    "All public traffic must go through the ALB first."
                )
            else:
                allowed = False
                explanation = f"Port {port} from source '{req.source}' has no matching inbound allow rule."
            arch_note = "Security Groups can reference OTHER Security Groups by ID (e.g. allow from sg-alb), avoiding hardcoded IP addresses!"

        elif target == "RDS":
            sg_name = "sg-rds-data-tier"
            if port == 5432 and ("ec2" in source or "sg-ec2" in source):
                allowed = True
                rule = "Inbound Allow TCP 5432 from sg-ec2-app-tier"
                explanation = "PostgreSQL port 5432 is whitelisted only for requests originating from the EC2 instance Security Group."
            else:
                allowed = False
                explanation = (
                    f"BLOCKED: RDS database port {port} is completely sealed from '{req.source}'. "
                    "Only EC2 backend instances can talk to RDS."
                )
            arch_note = "RDS instances should always be in private data subnets with a Security Group allowing ingress ONLY from the compute tier."

        else:
            sg_name = "unknown"
            explanation = f"Target '{target}' not recognized. Choose ALB, EC2, or RDS."

        return TrafficTestResponse(
            traffic_allowed=allowed,
            status_code="200 ALLOWED" if allowed else "403 BLOCKED BY SECURITY GROUP",
            security_group_applied=sg_name,
            rule_matched=rule,
            is_stateful_response_allowed=allowed,  # Because SGs are stateful, return traffic is automatically permitted!
            explanation=explanation,
            security_architecture_note=(
                f"{arch_note}\n\n"
                "KEY CONCEPT - Stateful Security Groups:\n"
                "Security Groups are STATEFUL. If an inbound packet is allowed, the response packet is "
                "AUTOMATICALLY allowed back out, regardless of outbound rules. In contrast, Network ACLs (NACLs) "
                "are STATELESS and require explicit outbound ephemeral port rules."
            )
        )

    def simulate_imds_v2(self, req: IMDSRequest) -> IMDSResponse:
        """Simulates AWS EC2 Instance Metadata Service v2 (IMDSv2)."""
        return IMDSResponse(
            imds_version="IMDSv2 (Session Token Enforced)",
            token_header_required="X-aws-ec2-metadata-token",
            endpoint="http://169.254.169.254/latest/meta-data/",
            role_name=req.role_name,
            credentials={
                "Code": "Success",
                "LastUpdated": "2026-10-31T12:00:00Z",
                "Type": "AWS-HMAC",
                "AccessKeyId": "ASIATRAININGROLEKEY99",
                "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                "Token": "IQoJb3JpZ2luX2VjEExampleIMDSv2SessionToken...",
                "Expiration": "2026-10-31T18:00:00Z"
            },
            security_explanation=(
                "Why IMDSv2 is critical for EC2 Security:\n"
                "1. IMDSv1 was vulnerable to Server-Side Request Forgery (SSRF) because simple GET requests "
                "could steal credentials from 169.254.169.254.\n"
                "2. IMDSv2 requires an HTTP PUT request with 'X-aws-ec2-metadata-token-ttl-seconds: 21600' "
                "to generate a secret session token first, completely neutralizing standard SSRF attacks.\n"
                "3. Your Python / boto3 code does NOT need to do this manually — the AWS SDK automatically "
                "uses IMDSv2 behind the scenes to fetch credentials for the attached IAM Role!"
            )
        )

    def get_ec2_and_pricing_guide(self) -> Dict[str, Any]:
        """Comprehensive guide on EC2 instance types and pricing models."""
        return {
            "instance_families": {
                "t4g / t3 / t2": "General Purpose (Burstable). Best for dev, test, and small apps like Ataa backend.",
                "m6i / m5": "General Purpose (Balanced). High memory & compute for production services.",
                "c6i / c5": "Compute Optimized. High CPU-to-memory ratio for video encoding, ML inference.",
                "r6i / r5": "Memory Optimized. For in-memory databases (Redis, PostgreSQL caching).",
            },
            "pricing_models": {
                "On-Demand": {
                    "commitment": "None (pay by the second).",
                    "best_for": "Unpredictable workloads, short-term dev/test.",
                    "discount": "0% (baseline price)."
                },
                "Spot Instances": {
                    "commitment": "None, but AWS can terminate instance with a 2-minute notice if capacity is needed.",
                    "best_for": "Batch processing, fault-tolerant workloads, CI/CD runners.",
                    "discount": "Up to 90% discount compared to On-Demand."
                },
                "Reserved Instances (RI)": {
                    "commitment": "1 or 3 year commitment for a specific instance family.",
                    "best_for": "Steady-state production databases and baseline compute.",
                    "discount": "Up to 72% discount."
                },
                "Savings Plans": {
                    "commitment": "Commit to a consistent amount of compute usage ($/hour) for 1 or 3 years.",
                    "best_for": "Modern flexibility across EC2, Fargate, and Lambda.",
                    "discount": "Up to 72% discount."
                }
            },
            "shared_responsibility_model_ec2": {
                "AWS_responsibility": "Physical data center security, host hardware, hypervisor, physical network.",
                "Customer_responsibility": "Guest OS installation/patching, Security Group configuration, application code, firewall rules, user access (SSH keys)."
            }
        }


ec2_service = EC2SecurityService()
