
from app.utilities.enums import RoleName


PERMISSIONS = [
    ("organization:create", "Create organizations"),
    ("organization:update", "Update organizations"),
    ("organization:delete", "Delete organizations"),
    ("organization:view", "View organizations"),
    ("user:create", "Create users"),
    ("user:update", "Update users"),
    ("user:delete", "Delete users"),
    ("user:view", "View users"),
    ("asset:create", "Create assets"),
    ("asset:update", "Update assets"),
    ("asset:delete", "Delete assets"),
    ("asset:assign", "Assign assets"),
    ("asset:unassign", "Unassign assets"),
    ("asset:view", "View assets"),
    ("ticket:create", "Create tickets"),
    ("ticket:update", "Update ticket status"),
    ("ticket:resolve", "Resolve tickets"),
    ("ticket:view", "View tickets"),
]

ROLE_PERMISSIONS = {
    RoleName.SUPERADMIN.value: [p[0] for p in PERMISSIONS],
    RoleName.ORG_ADMIN.value: [
        "organization:update", "organization:view",
        "user:create", "user:update", "user:delete", "user:view",
        "asset:create", "asset:update", "asset:delete", "asset:assign", "asset:unassign", "asset:view",
        "ticket:update", "ticket:resolve", "ticket:view",
    ],
    RoleName.IT_ADMIN.value: [
        "asset:create", "asset:update", "asset:delete", "asset:assign", "asset:unassign", "asset:view",
        "ticket:update", "ticket:resolve", "ticket:view",
        "user:view",
    ],
    RoleName.EMPLOYEE.value: [
        "asset:view",
        "ticket:create", "ticket:view",
    ],
}