from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.features.permissions.repository import PermissionRepository
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_roles import UserRole
from app.seed.permission import PERMISSIONS, ROLE_PERMISSIONS
from app.utilities.config import settings
from app.utilities.security import Security
from app.utilities.session import AsyncSessionLocal, get_db
from app.utilities.exceptions import AppException
from app.features.role.usecases.get_role import GetRole

from app.features.auth.controller import router as AuthRouter
from app.features.users.controllers import router as UserRouter
from app.features.role.controllers import router as RoleRouter
from app.features.user_role.controllers import router as UserRoleRouter
from app.features.organizations.controllers import router as OrganizationRouter
from app.features.user_organization.controllers import router as UserOrganiaztionRouter
from app.features.assets.controllers import router as AssetRouter
from app.features.assets.controllers import assignment_router as AssetAssignmentRouter
from app.features.tickets.controllers import router as TicketRouter

app = FastAPI(
    title="Assetra : Asset Management System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppException)
async def app_exception_handler(request : Request, exc : AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message" : exc.detail
        }
    )

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(UserRoleRouter)
app.include_router(RoleRouter)
app.include_router(OrganizationRouter)
app.include_router(UserOrganiaztionRouter)
app.include_router(AssetRouter)
app.include_router(AssetAssignmentRouter)
app.include_router(TicketRouter)


@app.on_event("startup")
async def seed_superadmin():
    async with AsyncSessionLocal() as db: 
        try:

            '''-------------Seeding Permission----------------'''
            permission_map = {}
            for name, desc in PERMISSIONS:
                permission = await PermissionRepository.get_permission_by_name(name, db)
                if not permission:
                    permission = Permission(permission_name=name, permission_description=desc)
                    db.add(permission)
                    await db.flush()
                permission_map[name] = permission
            print(f"{len(permission_map)} Permissions Seeded Successfully!!")


            '''-------------Seeding Roles---------'''
            role_names = ["SUPERADMIN", "ORG_ADMIN", "IT_ADMIN", "EMPLOYEE"]
            existing_roles = {}

            for name in role_names:
                role_check = await db.execute(select(Role).where(Role.role_name == name))
                role_obj = role_check.scalars().first()
                
                if not role_obj:
                    role_obj = Role(role_name=name)
                    db.add(role_obj)
                    await db.flush() 
                
                existing_roles[name] = role_obj
            print('Roles Seeded Successfully!!!')


            '''Seeding Role based Permissions'''
            existing_mappings_check = await db.execute(select(RolePermission))
            existing_mappings = {
                (m.role_id, m.permission_id) for m in existing_mappings_check.scalars().all()
            }

            for role_name, perm_codes in ROLE_PERMISSIONS.items():
                role_obj = existing_roles[role_name]
                
                for code in perm_codes:
                    perm_obj = permission_map[code]
                    
                    mapping_key = (role_obj.role_id, perm_obj.permission_id) 
                    
                    if mapping_key not in existing_mappings:
                        new_mapping = RolePermission(
                            role_id=role_obj.role_id,
                            permission_id=perm_obj.permission_id
                        )
                        db.add(new_mapping)
            
            await db.flush()
            print('Role based Permissions Seeded Successfully!!!')

            '''----------SuperAdmin Seeding------------'''
            user_check = await db.execute(
                select(User).where(User.user_email == settings.SUPERADMIN_EMAIL)
            )
            existing_user = user_check.scalars().first()
            if not existing_user:
                password = Security.hash_password(settings.SUPERADMIN_PASSWORD)
                new_super_admin = User(
                    user_name=settings.SUPERADMIN_FIRST_NAME,
                    user_email=settings.SUPERADMIN_EMAIL,
                    user_password=password
                )
                db.add(new_super_admin)
                await db.flush() 
                
                superadmin_role = existing_roles["SUPERADMIN"]
                
                role_superadmin = UserRole(
                    user_id=new_super_admin.user_id, 
                    role_id=superadmin_role.role_id
                )
                db.add(role_superadmin)
                print('Superadmin user created successfully!')
            else:
                print('Superadmin user already exists.')

            # Single atomic commit for the entire seeding operation
            await db.commit()
            print('Seeding Successfully Completed!')
                
        except Exception as e:
            await db.rollback()
            print(f"Error seeding database: {e}")
            raise e



@app.get("/", tags=["Health"])
async def health():
    return {
        "status": "ok", 
        "message": "Asset Management API is running"
    }

