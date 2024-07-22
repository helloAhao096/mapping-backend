from fastapi import Depends
from fastapi.exceptions import HTTPException

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from jose import jwt, JWTError
import datetime
from apis.user.api import router_user
from apis.user.repository import UserServeries
from apis.user.schemas import OAuth2ClientCredentialsRequestForm, SelectUserForm, UserForm
from db.models import User
from exts.exceptions import ExceptionEnum
from exts.responses.json_response import Success, Fail
from utils.jwt_helper import TokenUtils, OAuth2ClientCredentialsBearer
from db.async_database import AsyncSession, depends_get_db_session

@router_user.post("/register", summary="创建新用户")
async def call_back(forms: UserForm=Depends(),
                    db_session: AsyncSession = Depends(depends_get_db_session)):
    try:
        select_user_result = await UserServeries.select_by_user_email(db_session,
                                                                      email=forms.email,
                                                                      )
        print(select_user_result,"rsobj")
        if select_user_result:
            return Fail(api_code=400, message="用户邮箱已存在")

        create_user_result = await UserServeries.create_user(db_session,
                                                             username=forms.username,
                                                             email=forms.email,
                                                             password_hash=forms.password
                                                             )
        print(create_user_result,"xxxxx")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if create_user_result:
        return Success(api_code=200, result={'user_id': create_user_result.id, 'nano_id': create_user_result.nano_id,'username': create_user_result.username, 'email': create_user_result.email,}, message='注册成功！')
    else:
        return Fail(api_code=400, message='User creation failed')


@router_user.post("/login", summary="登录账号")
async def call_back(forms: UserForm=Depends(),
                    db_session: AsyncSession = Depends(depends_get_db_session),
                    Authorize: AuthJWT = Depends()):
    try:
        print(forms)
        select_user_result = await UserServeries.select_by_user_email(db_session,
                                                                      email=forms.email,
                                                                      )
        print(select_user_result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if select_user_result:
        expires = datetime.timedelta(days=30)
        access_token = Authorize.create_access_token(subject=select_user_result.username,
                                                     user_claims={'nano_id':select_user_result.nano_id,'email': select_user_result.email},
                                                     expires_time=expires)
        print(access_token)
        return Success(api_code=200, result=access_token, message='登录成功！')
    else:
        return Fail(api_code=400, message='User creation failed')


@router_user.get("/user_info", summary="查询用户基本信息（受保护资源）")
async def call_back(forms: SelectUserForm=Depends(),
                    db_session: AsyncSession = Depends(depends_get_db_session),
                    Authorize: AuthJWT = Depends()):
    '''
    定义API接口。改API接口需要token值并校验通过才可以访问
    :param token:
    :return:
    '''
    try:
        Authorize.jwt_required()
        select_user_result = await UserServeries.select_user_info(db_session, id=forms.id, nanoid=forms.nano_id, email=forms.email)

    except AuthJWTException as e:
        print(e)
        return Fail(api_code=400, message='permission error')
        # raise AuthJWTException()
    return Success(api_code=200,
                   result=select_user_result,
                   message='用户基本信息')
