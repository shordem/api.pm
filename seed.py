from sqlalchemy.orm import Session

from models.role import Role
from models.permission import Permission
from models.role_permission import RolePermission
from config.database import SessionLocal


def seed(db: Session):

    roles = [
        Role(name="owner"),  # 0
        Role(name="admin"),  # 1
        Role(name="member"),  # 2
    ]
    db.add_all(roles)
    db.commit()

    permissions = [
        Permission(name="delete_organization"),  # 0
        Permission(name="update_organization"),  # 1
        Permission(name="add_member"),  # 2
        Permission(name="remove_member"),  # 3
        Permission(name="list_member"),  # 4
        Permission(name="create_folder"),  # 5
        Permission(name="delete_folder"),  # 6
        Permission(name="update_folder"),  # 7
        Permission(name="list_folder"),  # 8
        Permission(name="create_task"),  # 9
        Permission(name="delete_task"),  # 10
        Permission(name="delete_any_task"),  # 11
        Permission(name="update_task"),  # 12
        Permission(name="list_task"),  # 13
        Permission(name="update_member"),  # 14
    ]
    db.add_all(permissions)
    db.commit()

    role_permissions = [
        {"role_id": roles[0].id, "permission_id": permissions[0].id},
        {"role_id": roles[0].id, "permission_id": permissions[1].id},
        {"role_id": roles[0].id, "permission_id": permissions[2].id},
        {"role_id": roles[0].id, "permission_id": permissions[3].id},
        {"role_id": roles[0].id, "permission_id": permissions[4].id},
        {"role_id": roles[0].id, "permission_id": permissions[5].id},
        {"role_id": roles[0].id, "permission_id": permissions[6].id},
        {"role_id": roles[0].id, "permission_id": permissions[7].id},
        {"role_id": roles[0].id, "permission_id": permissions[8].id},
        {"role_id": roles[0].id, "permission_id": permissions[9].id},
        {"role_id": roles[0].id, "permission_id": permissions[10].id},
        {"role_id": roles[0].id, "permission_id": permissions[11].id},
        {"role_id": roles[0].id, "permission_id": permissions[12].id},
        {"role_id": roles[0].id, "permission_id": permissions[13].id},
        {"role_id": roles[0].id, "permission_id": permissions[14].id},
        {"role_id": roles[1].id, "permission_id": permissions[2].id},
        {"role_id": roles[1].id, "permission_id": permissions[3].id},
        {"role_id": roles[1].id, "permission_id": permissions[4].id},
        {"role_id": roles[1].id, "permission_id": permissions[5].id},
        {"role_id": roles[1].id, "permission_id": permissions[6].id},
        {"role_id": roles[1].id, "permission_id": permissions[7].id},
        {"role_id": roles[1].id, "permission_id": permissions[8].id},
        {"role_id": roles[1].id, "permission_id": permissions[9].id},
        {"role_id": roles[1].id, "permission_id": permissions[10].id},
        {"role_id": roles[1].id, "permission_id": permissions[11].id},
        {"role_id": roles[1].id, "permission_id": permissions[12].id},
        {"role_id": roles[1].id, "permission_id": permissions[13].id},
        {"role_id": roles[1].id, "permission_id": permissions[14].id},
        {"role_id": roles[2].id, "permission_id": permissions[4].id},
        {"role_id": roles[2].id, "permission_id": permissions[8].id},
        {"role_id": roles[2].id, "permission_id": permissions[9].id},
        {"role_id": roles[2].id, "permission_id": permissions[10].id},
        {"role_id": roles[2].id, "permission_id": permissions[12].id},
        {"role_id": roles[2].id, "permission_id": permissions[13].id},
    ]

    db.add_all(
        [
            RolePermission(
                role_id=role_permission["role_id"],
                permission_id=role_permission["permission_id"],
            )
            for role_permission in role_permissions
        ]
    )
    db.commit()
    db.commit()


def main():
    db = SessionLocal()

    try:
        seed(db)
        print("Database seeded successfully")
    except Exception as e:
        print("Error seeding database:")
        print(e)
    finally:
        db.close()


if __name__ == "__main__":
    main()
