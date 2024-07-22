from fastapi import FastAPI
# from fastapi_users import FastAPIUsers
# from fastapi_users.authentication import AuthenticationBackend

from apis.guide.api import router_guide
from apis.user.api import router_user
from db.async_database import create_db_and_tables
from db.models import User
from exts.exceptions import ApiExceptionHandler
import os
import pathlib
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, )
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
# from config.config import get_settings

#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Not needed if you setup a migration system like Alembic
#     await create_db_and_tables()
#     yield


app = FastAPI(
    # lifespan=lifespan,
    docs_url="/docs",
    title="途钉路书指南",
    description="创建属于自己的途钉路书指南"
)

try:
    app.mount("/static", StaticFiles(directory=f"{pathlib.Path.cwd()}/static"), name="static")
except:
    pass



# 注册全局异常
ApiExceptionHandler().init_app(app)

# setup_ext_loguru(app, log_pro_path=str(pathlib.Path.cwd()))
# app.router.route_class = ContextLogerRoute
# app.add_middleware(BindContextvarMiddleware)

# 这个中间件会引发异步测试卡顿
# from middlewares.loger.middleware import  LogerMiddleware
# app.add_middleware(LogerMiddleware,log_pro_path=os.path.split(os.path.realpath(__file__))[0])

app.include_router(router_guide)
# app.include_router(router_auth)
app.include_router(router_user)


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    print(app.openapi_url)
    print(app.title)
    print(app.swagger_ui_oauth2_redirect_url)
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )

def creat_app():
    return app
