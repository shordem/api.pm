from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserSchema
from models.organization import Organization
from models.user_organization import UserOrganization
from models.permission import Permission
from models.role_permission import RolePermission


def check_permission(
    db: Session, user: UserSchema, organization_id: str, required_permission: str
):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    organization = (
        db.query(Organization).filter(Organization.id == organization_id).first()
    )
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")

    user_organization = (
        db.query(UserOrganization)
        .filter(UserOrganization.user_id == user.id)
        .filter(UserOrganization.organization_id == organization.id)
        .first()
    )

    if user_organization is None:
        raise HTTPException(
            status_code=404, detail="User is not a member of the organization"
        )

    permission = (
        db.query(Permission).filter(Permission.name == required_permission).first()
    )

    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    role_permission = (
        db.query(RolePermission)
        .filter(RolePermission.role_id == user_organization.role_id)
        .filter(RolePermission.permission_id == permission.id)
        .first()
    )

    if role_permission is None:
        raise HTTPException(
            status_code=403, detail="User does not have the required permission"
        )
