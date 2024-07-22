from typing import Optional
from passlib.context import CryptContext
from fastapi import Query
from pydantic import BaseModel, validator
import re
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2ClientCredentialsRequestForm:

    def __init__(
            self,
            grant_type: str = Query(..., regex="client_credentials"),
            scope: str = Query(""),
            client_id: str = Query(...),
            client_secret: str = Query(...),
            username: Optional[str] = Query(None),
            password: Optional[str] = Query(None),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password


class SelectUserForm(BaseModel):
    id: Optional[int]
    nano_id: Optional[str]
    email: Optional[str]


class UserForm(BaseModel):
    # id: Optional[int]
    # nano_id: Optional[str]
    email: Optional[str]
    # username: Optional[str]
    password: Optional[str]
    captcha: Optional[str]

    @validator('email', pre=True, always=True)
    def validate_email(cls, v):
        if v is not None and "@" not in v:
            raise ValueError('Invalid email address')
        return v


    @validator('password')
    def validate_password(cls, value):
        print(value)
        # 密码必须至少8个字符
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # 密码必须包含至少一个大写字母
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        # 密码必须包含至少一个小写字母
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        # 密码必须包含至少一个数字
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        # 密码必须包含至少一个特殊字符
        # if not re.search(r'[\W_]', value):
        #     raise ValueError('Password must contain at least one special character')
        # hash_value = pwd_context.hash(value)
        hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')


#
# class UserRead(BaseModel):
#     pass
#
#
# class UserCreate(BaseModel):
#     pass
#
#
# class UserUpdate(BaseModel):
#     pass
