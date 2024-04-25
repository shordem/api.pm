from sqlalchemy.orm import Session

from models.organization import Organization
from models.member import Member
from models.folder import Folder
from models.member import Member
from models.user import User
from schemas.organization import OrganizationCreate
from schemas.user import User as UserSchema
from services.user import get_user_by_email


def get_organization(db: Session, organization_id: str):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise Exception("Organization not found")
    return org


def find_by_member(db: Session, user_id: str, organization_id: str):
    return (
        db.query(Member)
        .filter(Member.user_id == user_id, Member.organization_id == organization_id)
        .first()
    )


def get_organizations_by_member(db: Session, user_id: str):

    return (
        db.query(Organization)
        .join(Member, Organization.id == Member.organization_id)
        .filter(Member.user_id == user_id)
        .all()
    )


def list_organization_members(db: Session, organization_id: str):
    results = (
        db.query(User)
        .join(Member, User.id == Member.user_id)
        .filter(Member.organization_id == organization_id)
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

    new_folder = Folder(name="all", organization_id=new_org.id)
    db.add(new_folder)

    new_member = Member(user_id=org.owner_id, organization_id=new_org.id)
    db.add(new_member)

    db.commit()


def add_member_to_organization(db: Session, organization_id: str, user_email: str):
    user = get_user_by_email(db, user_email)
    if not user.is_email_verified:
        raise Exception("User is not verified")

    get_organization(db, organization_id)

    member = find_by_member(db, user.id, organization_id)
    if member:
        raise Exception("User is already a member of the organization")

    new_member = Member(user_id=user.id, organization_id=organization_id)
    db.add(new_member)
    db.commit()
