from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from schemas.member import MemberCreate
from services import organization as organization_svc
from schemas.organization import OrganizationCreatePayload, OrganizationCreate
from schemas.user import UserSchema
from dependencies.db import get_db
from dependencies.user import get_current_verified_user
from dependencies.permission import check_permission

router = APIRouter(
    prefix="/organizations",
    tags=["Organization"],
    dependencies=[Depends(get_current_verified_user)],
)


@router.get("")
def get_organizations(
    user: Annotated[UserSchema, Depends(get_current_verified_user)], db=Depends(get_db)
):
    try:
        return organization_svc.get_organizations_by_member(db, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("")
def create_organization(
    organization: OrganizationCreatePayload,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
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
def list_organization_members(
    organization_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "list_member")
        return organization_svc.list_organization_members(db, organization_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{organization_id}/members")
def add_member_to_organization(
    organization_id: str,
    member: MemberCreate,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "add_member")
        organization_svc.add_member_to_organization(db, organization_id, member.email)
        return {"detail": "Member added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{organization_id}/members/{member_id}")
def remove_member_from_organization(
    organization_id: str,
    member_id: str,
    user: Annotated[UserSchema, Depends(get_current_verified_user)],
    db=Depends(get_db),
):
    try:
        check_permission(db, user, organization_id, "remove_member")
        organization_svc.remove_member_from_organization(db, organization_id, member_id)
        return {"detail": "Member removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
