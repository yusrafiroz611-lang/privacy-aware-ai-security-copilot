"""Small role-based access control (RBAC) helper.

This is a demo policy module, not a complete authentication system.
The calling application must authenticate users securely first.
"""
from typing import Iterable

ROLE_PERMISSIONS = {
    "employee": {"submit_activity", "view_own_result"},
    "analyst": {"submit_activity", "view_own_result", "view_alerts"},
    "security_admin": {
        "submit_activity", "view_own_result", "view_alerts",
        "view_audit_logs", "manage_policies",
    },
}


def has_permission(role: str, permission: str) -> bool:
    """Return whether a known role has a specific permission."""
    return permission in ROLE_PERMISSIONS.get(role, set())


def require_permission(role: str, permission: str) -> None:
    """Raise PermissionError if the role is not allowed to perform an action."""
    if not has_permission(role, permission):
        raise PermissionError(f"Role {role!r} is not allowed to: {permission}")


def permissions_for(role: str) -> list[str]:
    """List permissions granted to a role."""
    return sorted(ROLE_PERMISSIONS.get(role, set()))
