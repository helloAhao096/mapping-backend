from fastapi import APIRouter
router_user = APIRouter(prefix="/user")

from db.models import User
from ..api import user_api
from ..api import auth_api
import uuid
from typing import Optional

# from ..schemas import UserRead, UserCreate, UserUpdate

#
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

# router_auth = APIRouter(prefix="/auth")
#
# router_auth.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"])
# router_auth.include_router(fastapi_users.get_register_router(UserRead, UserCreate), tags=["auth"])
# router_auth.include_router(fastapi_users.get_reset_password_router(), tags=["auth"])
# router_auth.include_router(fastapi_users.get_verify_router(UserRead), tags=["auth"])
#
# router_user.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="", tags=["user"])