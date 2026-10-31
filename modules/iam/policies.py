"""IAM Policy Templates and Least Privilege Evaluation Helpers."""
import fnmatch
from typing import Any, Dict, List

# Example 1: Anti-Pattern - Overly permissive admin policy
OVERLY_PERMISSIVE_POLICY: Dict[str, Any] = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DangerousFullAdminAccess",
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }
    ]
}

# Example 2: Best Practice - Scoped Least-Privilege Policy for Ataa Donation Platform
# The EC2 instance can ONLY write case files to S3 and emit CloudWatch logs.
# It CANNOT delete files, CANNOT read other buckets, and CANNOT touch IAM/EC2.
ATAA_LEAST_PRIVILEGE_POLICY: Dict[str, Any] = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCaseDocumentUploadOnly",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::ataa-verification-documents/cases/*"
        },
        {
            "Sid": "AllowLoggingToCloudWatch",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:log-group:/aws/training-lab/*"
        },
        {
            "Sid": "DenyObjectDeletionExplicitly",
            "Effect": "Deny",
            "Action": [
                "s3:DeleteObject",
                "s3:DeleteObjectVersion"
            ],
            "Resource": "arn:aws:s3:::ataa-verification-documents/*"
        }
    ]
}


def evaluate_iam_policy(policy: Dict[str, Any], requested_action: str, requested_resource: str) -> Dict[str, Any]:
    """Simulates the official AWS IAM Policy Evaluation Logic:
    1. By default, all requests are DENIED (Default Deny).
    2. An explicit ALLOW in any policy overrides the default deny.
    3. An explicit DENY in any policy overrides ANY allow (Explicit Deny Wins).
    """
    statements: List[Dict[str, Any]] = policy.get("Statement", [])
    
    explicit_deny_found = False
    explicit_allow_found = False
    deny_reason = ""
    allow_reason = ""
    
    steps = [
        "1. AWS IAM starts with Default Deny: all actions are blocked unless an explicit Allow matches.",
    ]

    for stmt in statements:
        effect = stmt.get("Effect")
        actions = stmt.get("Action", [])
        if isinstance(actions, str):
            actions = [actions]
        resources = stmt.get("Resource", [])
        if isinstance(resources, str):
            resources = [resources]

        # Check action match (supports wildcards e.g. s3:*)
        action_matches = any(fnmatch.fnmatch(requested_action.lower(), a.lower()) for a in actions)
        
        # Check resource match (supports wildcards e.g. arn:aws:s3:::bucket/*)
        resource_matches = any(fnmatch.fnmatch(requested_resource.lower(), r.lower()) for r in resources)

        if action_matches and resource_matches:
            sid = stmt.get("Sid", "UnnamedStatement")
            if effect == "Deny":
                explicit_deny_found = True
                deny_reason = f"Explicit Deny in Statement '{sid}' for Action '{requested_action}' on '{requested_resource}'"
                steps.append(f"2. [MATCHED DENY] Statement '{sid}' explicitly DENIES '{requested_action}'.")
            elif effect == "Allow":
                explicit_allow_found = True
                allow_reason = f"Explicit Allow in Statement '{sid}'"
                steps.append(f"2. [MATCHED ALLOW] Statement '{sid}' explicitly ALLOWS '{requested_action}'.")

    if explicit_deny_found:
        steps.append("3. Final Rule: Explicit Deny ALWAYS overrides any Allow. Access is DENIED.")
        return {
            "allowed": False,
            "reason": deny_reason,
            "steps": steps
        }
    
    if explicit_allow_found:
        steps.append("3. Final Rule: Explicit Allow found and no Deny matched. Access is GRANTED.")
        return {
            "allowed": True,
            "reason": allow_reason,
            "steps": steps
        }

    steps.append("3. Final Rule: No Allow matched. The default deny remains in effect. Access is DENIED.")
    return {
        "allowed": False,
        "reason": "Default Deny: No statement explicitly allowed this action and resource combination.",
        "steps": steps
    }
