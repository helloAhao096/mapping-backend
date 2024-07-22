from fastapi import APIRouter
router_guide = APIRouter(prefix='/guide', tags=["指南模块"], include_in_schema=True)

from ..api import guide_api

