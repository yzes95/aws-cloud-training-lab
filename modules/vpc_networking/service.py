import ipaddress
from typing import Any, Dict, List
from .schemas import (
    PacketRouteRequest,
    PacketRouteResponse,
    SubnetCalculationRequest,
    SubnetCalculationResponse,
    VpcEndpointsGuideResponse,
)


class VPCNetworkingService:
    """Service providing hands-on training for AWS VPC, Subnets, Routing, Gateways, and CIDR."""

    def calculate_subnet_ips(self, req: SubnetCalculationRequest) -> SubnetCalculationResponse:
        """Calculates total, reserved, and usable IPs in an AWS Subnet CIDR block."""
        try:
            net = ipaddress.ip_network(req.cidr_block.strip(), strict=False)
            total = net.num_addresses
        except ValueError as e:
            total = 256
            req.cidr_block = "10.0.1.0/24"

        # AWS ALWAYS reserves 5 IP addresses in every subnet!
        # Standard networking reserves 2 (.0 network and .255 broadcast).
        # AWS reserves 3 additional IPs (.1 VPC router, .2 AWS DNS, .3 future AWS reservation).
        usable = max(0, total - 5)

        base_ip = str(net.network_address)
        octets = base_ip.split(".")
        prefix = f"{octets[0]}.{octets[1]}.{octets[2]}"

        breakdown = {
            f"{prefix}.0": "Network Address (Always reserved in standard IP networking)",
            f"{prefix}.1": "Reserved by AWS for the VPC Default Router",
            f"{prefix}.2": "Reserved by AWS for AmazonProvidedDNS (Route 53 Resolver)",
            f"{prefix}.3": "Reserved by AWS for future use",
            f"{prefix}.255": "Network Broadcast Address (AWS does not support broadcast, but reserves it)"
        }

        return SubnetCalculationResponse(
            cidr_block=req.cidr_block,
            total_ips=total,
            aws_reserved_ips=5,
            usable_ips=usable,
            reserved_breakdown=breakdown,
            aws_exam_tip=(
                "CRITICAL AWS CCP & Solutions Architect Exam Fact:\n"
                "In AWS, an IP subnet always has (2^(32-prefix)) - 5 usable IP addresses.\n"
                "For a /24 subnet (256 addresses), AWS provides exactly 251 usable IPs!\n"
                "For a /28 subnet (16 addresses), AWS provides exactly 11 usable IPs!"
            )
        )

    def trace_packet_route(self, req: PacketRouteRequest) -> PacketRouteResponse:
        """Traces how packets travel between subnets, Internet Gateways, NAT Gateways, and S3 VPC Endpoints."""
        src = req.source_subnet_type.lower()
        dst = req.destination.lower()

        path: List[str] = []
        gateways: List[str] = []
        success = True
        needs_nat = False
        uses_vpce = False
        explanation = ""
        cost_tip = ""

        if "private" in src and "internet" in dst:
            path = [
                "1. EC2 Instance initiates outbound TCP connection (e.g. `docker pull` or `apt-get update`)",
                "2. Route Table checks target 0.0.0.0/0 -> points to NAT Gateway in the Public Subnet (10.0.1.x)",
                "3. NAT Gateway translates private IP (10.0.2.x) to an Elastic Public IP (EIP)",
                "4. Public Subnet Route Table checks 0.0.0.0/0 -> points to Internet Gateway (IGW)",
                "5. Traffic leaves VPC boundary to external package repository / Docker Hub",
                "6. Response packets return through IGW -> NAT Gateway -> mapped back to private EC2!"
            ]
            gateways = ["NAT Gateway (nat-xxx)", "Internet Gateway (igw-xxx)"]
            needs_nat = True
            explanation = (
                "A NAT Gateway enables outbound internet traffic for instances in a private subnet, "
                "while preventing the outside internet from initiating an inbound connection to those instances!"
            )
            cost_tip = "NAT Gateways cost ~$0.045/hour + $0.045/GB data processed. For dev environments, shutting down NAT Gateways saves ~$32/month!"

        elif "private" in src and "s3" in dst:
            path = [
                "1. EC2 Instance makes boto3 call: `s3.put_object(Bucket='ataa-docs')`",
                "2. VPC Route Table matches S3 Prefix List (pl-63a5400a) -> routed directly to S3 Gateway Endpoint (vpce-xxx)",
                "3. Packets travel entirely over AWS private network backbone directly to S3 storage servers",
                "4. ZERO internet traversal, ZERO NAT Gateway fees!"
            ]
            gateways = ["S3 VPC Gateway Endpoint (vpce-s3)"]
            uses_vpce = True
            explanation = (
                "VPC Gateway Endpoints for Amazon S3 allow private compute instances to access S3 "
                "without needing a NAT Gateway or internet connection. Traffic never leaves the private AWS network!"
            )
            cost_tip = "VPC Gateway Endpoints for S3 and DynamoDB are 100% FREE! Always use them to avoid paying NAT Gateway data transfer charges."

        elif "public" in src and ("internet" in dst or "inbound" in dst):
            path = [
                "1. Browser / Client sends HTTPS request to domain ataa.org",
                "2. Route 53 resolves DNS to Application Load Balancer (ALB)",
                "3. Traffic enters VPC via Internet Gateway (IGW)",
                "4. Public Subnet Route Table delivers packet to ALB listener on port 443"
            ]
            gateways = ["Internet Gateway (igw-xxx)"]
            explanation = "Public subnets are directly connected to the Internet Gateway with public IP routing."

        elif "ec2" in src and "rds" in dst:
            path = [
                "1. FastAPI on EC2 initiates PostgreSQL connection on port 5432",
                "2. Traffic is routed locally inside the VPC network (10.0.0.0/16 route)",
                "3. Reaches Private Data Subnet (10.0.3.x)",
                "4. Evaluated by RDS Security Group (verifies source is EC2 Security Group)",
                "5. Connection accepted!"
            ]
            explanation = "Internal VPC traffic uses high-speed, private, low-latency AWS routing without touching any gateways."
            cost_tip = "Traffic within the same Availability Zone in a VPC is free."

        else:
            path = [f"Source: {req.source_subnet_type}", f"Destination: {req.destination}"]
            explanation = "Standard VPC routing."

        return PacketRouteResponse(
            route_path=path,
            gateways_crossed=gateways,
            can_traffic_succeed=success,
            requires_nat_gateway=needs_nat,
            uses_vpc_endpoint=uses_vpce,
            explanation=explanation,
            cost_optimization_tip=cost_tip or "Keep high-volume inter-service communication within the same AZ to minimize data transfer fees."
        )

    def get_vpc_endpoints_guide(self) -> VpcEndpointsGuideResponse:
        """Comprehensive comparison of Gateway Endpoints vs Interface Endpoints (AWS PrivateLink)."""
        return VpcEndpointsGuideResponse(
            gateway_endpoints={
                "Supported Services": "ONLY Amazon S3 and Amazon DynamoDB",
                "How it Works": "Adds a target entry directly to your VPC Route Tables pointing to the service prefix list.",
                "Cost": "100% FREE (No hourly charge, no data processing fees).",
                "Security": "Supports Endpoint Policies to restrict access to specific buckets or tables."
            },
            interface_endpoints={
                "Supported Services": "Most other AWS services (Secrets Manager, SSM, CloudWatch, SQS, SNS, ECS, and third-party SaaS)",
                "How it Works": "Provisions an Elastic Network Interface (ENI) with a private IP address inside your subnet.",
                "Cost": "Paid (~$0.01/hour per AZ + $0.01 per GB processed).",
                "Security": "Secured with standard Security Groups attached to the endpoint ENI."
            },
            cost_comparison="Always prefer Gateway Endpoints for S3 and DynamoDB because they are completely free and require zero ENI management."
        )


vpc_service = VPCNetworkingService()
