from sqlalchemy.orm import Session

from models.organization import Organization
from models.folder import Folder
from models.user import User
from models.user_organization import UserOrganization
from models.role import Role
from schemas.organization import OrganizationCreate
from schemas.user import UserSchema
from schemas.organization import OrganizationSchema
from services.user import get_user_by_email


def get_organization(db: Session, organization_id: str):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise Exception("Organization not found")
    return org


def find_by_member(db: Session, user_id: str, organization_id: str):
    return (
        db.query(UserOrganization)
        .filter(UserOrganization.user_id == user_id)
        .filter(UserOrganization.organization_id == organization_id)
        .first()
    )


def get_organizations_by_member(db: Session, user_id: str):
    results = (
        db.query(Organization)
        .join(UserOrganization, Organization.id == UserOrganization.organization_id)
        .filter(UserOrganization.user_id == user_id)
        .all()
    )

    resultDto = []
    for org in results:
        resultDto.append(OrganizationSchema.model_validate(org))

    return resultDto


def list_organization_members(db: Session, organization_id: str):
    results = (
        db.query(User)
        .join(UserOrganization, User.id == UserOrganization.user_id)
        .filter(UserOrganization.organization_id == organization_id)
        .all()
    )

    resultDto = []
    for user in results:
        resultDto.append(UserSchema.model_validate(user))

    return resultDto


def create_organization(db: Session, org: OrganizationCreate):
    new_org = Organization(**org.model_dump())
    db.add(new_org)
    db.commit()

    new_folder = Folder(name="all", organization_id=new_org.id, is_default=True)
    db.add(new_folder)

    owner_role = db.query(Role).filter(Role.name == "owner").first()

    if owner_role is None:
        db.rollback()
        raise Exception("Role not found")

    new_user_org = UserOrganization(
        user_id=org.owner_id, organization_id=new_org.id, role_id=owner_role.id
    )

    db.add(new_user_org)

    db.commit()


def add_member_to_organization(db: Session, organization_id: str, user_email: str):
    user = get_user_by_email(db, user_email)
    if not user.is_email_verified:
        raise Exception("User is not verified")

    get_organization(db, organization_id)

    member = find_by_member(db, user.id, organization_id)
    if member:
        raise Exception("User is already a member of the organization")

    member_role = db.query(Role).filter(Role.name == "member").first()
    new_member = UserOrganization(
        user_id=user.id, organization_id=organization_id, role=member_role.id
    )
    db.add(new_member)
    db.commit()


def remove_member_from_organization(db: Session, organization_id: str, user_id: str):
    member = find_by_member(db, user_id, organization_id)
    if not member:
        raise Exception("User is not a member of the organization")

    org = get_organization(db, organization_id)

    if str(org.owner_id) == user_id:
        raise Exception("Owner cannot be removed from the organization")

    db.delete(member)
    db.commit()
