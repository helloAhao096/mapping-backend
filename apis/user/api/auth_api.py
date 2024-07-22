from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from jose import jwt, JWTError
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from apis.user.api import router_user
from apis.user.repository import UserServeries
from apis.user.schemas import OAuth2ClientCredentialsRequestForm
from db.async_database import depends_get_db_session
from exts.responses.json_response import Success
from utils.email_helper import EmailSchema, send_email
from utils.jwt_helper import TokenUtils, OAuth2ClientCredentialsBearer

# oauth2_scheme = OAuth2ClientCredentialsBearer(tokenUrl="/oauth2/authorize",scheme_name="客户端模式",description="我是描述")

@router_user.get("/email_signup", summary="邮箱注册")
async def call_back(email: str,
                    request: Request,
                    db_session: AsyncSession = Depends(depends_get_db_session),
                    Authorize: AuthJWT = Depends()):
    # 输入邮箱，然后在数据库给这个邮箱创建一条用户信息
    # 除了邮箱其他默认字段都是自动生成的，用户验证状态为pending
    select_user_result = await UserServeries.create_user(db_session, email=email)
    if select_user_result:
        expires = datetime.timedelta(minutes=30)
        access_token = Authorize.create_access_token(subject=select_user_result.username,
                                                     user_claims={'nano_id': select_user_result.nano_id,
                                                                  'email': select_user_result.email,
                                                                  'authorized': False},
                                                     expires_time=expires)

        base_url = request.url._url  # 获取当前请求的 URL
        # 拼接 token 到 URL
        full_url = f"{base_url}token/{access_token}"
        email_data = {
            "subject": "test email",
            "recipients": ["helloahao@qq.com"],
            "body": f"token: {full_url}"
        }
        email: EmailSchema = EmailSchema(**email_data)
        await send_email(email)
        print(full_url)
        return Success(api_code=200, result={"access_token": access_token}, message="发送验证邮件成功，请用户激活账号")

#
# @router_user.get("/auth_email", summary="验证邮箱")
# async def call_back(token: str):
#     try:
#         select_user_result = await UserServeries.select_by_user_email(db_session,
#                                                                       email=forms.email,
#                                                                       )
#         print(select_user_result,"rsobj")
#         if select_user_result:
#             return Fail(api_code=400, message="用户邮箱已存在")
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     if create_user_result:
#         return Success(api_code=200, result={'user_id': create_user_result.id, 'nano_id': create_user_result.nano_id,'username': create_user_result.username, 'email': create_user_result.email,}, message='注册成功！')
#     else:
#         return Fail(api_code=400, message='User creation failed')
