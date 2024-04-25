from sqlalchemy.orm import Session

from models.organization import Organization
from models.member import Member
from models.folder import Folder
from models.member import Member
from schemas.organization import OrganizationCreate


def get_organization(db: Session, organization_id: str):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def get_organizations_by_member(db: Session, user_id: str):

    return (
        db.query(Organization)
        .join(Member, Organization.id == Member.organization_id)
        .filter(Member.user_id == user_id)
        .all()
    )


def list_organization_members(db: Session, organization_id: str):
    return db.query(Member).filter(Member.organization_id == organization_id).all()


def create_organization(db: Session, org: OrganizationCreate):
    new_org = Organization(**org.model_dump())
    db.add(new_org)
    db.commit()

    new_folder = Folder(name="all", organization_id=new_org.id)
    db.add(new_folder)

    new_member = Member(user_id=org.owner_id, organization_id=new_org.id)
    db.add(new_member)

    db.commit()
