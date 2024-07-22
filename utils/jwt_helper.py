from datetime import timedelta
from fastapi.exceptions import HTTPException
from typing import Optional, Dict
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Depends, status, Query
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from jose import jwt, JWTError
from datetime import datetime
from fastapi.security import OAuth2
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

SECRET_KEY = "9d0d57912db3f200142bf1e7467451b0d9be5904e631a9c9969c0bc993538a04"
ALGORITHM = "HS256"


class TokenUtils:

    @staticmethod
    def token_encode(data):
        jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def token_decode(token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": f"Bearer"},
        )
        try:
            # 开始反向解析我们的TOKEN.,解析相关的信息
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except (JWTError, ValidationError):
            raise credentials_exception
        return payload


class OAuth2ClientCredentialsBearer(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            clientCredentials={
                "tokenUrl": tokenUrl,
                "scopes": scopes,
            }
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None  # pragma: nocover
        return param


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
