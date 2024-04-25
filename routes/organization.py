from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.member import MemberCreate
from services import organization as organization_svc
from schemas.organization import OrganizationCreatePayload, OrganizationCreate
from schemas.user import User
from dependencies.db import get_db
from dependencies.user import get_current_verified_user


router = APIRouter(
    prefix="/organizations",
    tags=["Organization"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("")
def get_organizations(
    user: Annotated[User, Depends(get_current_verified_user)], db=Depends(get_db)
):
    try:
        return organization_svc.get_organizations_by_member(db, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("")
def create_organization(
    organization: OrganizationCreatePayload,
    user: Annotated[User, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        org = OrganizationCreate(name=organization.name, owner_id=str(user.id))

        organization_svc.create_organization(db, org)
        return {"detail": "Organization created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{organization_id}")
def get_organization(organization_id: str, db=Depends(get_db)):
    try:
        return organization_svc.get_organization(db, organization_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{organization_id}/members")
def list_organization_members(organization_id: str, db=Depends(get_db)):
    try:
        return organization_svc.list_organization_members(db, organization_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{organization_id}/members")
def add_member_to_organization(
    organization_id: str,
    member: MemberCreate,
    db=Depends(get_db),
):
    try:
        organization_svc.add_member_to_organization(db, organization_id, member.email)
        return {"detail": "Member added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
