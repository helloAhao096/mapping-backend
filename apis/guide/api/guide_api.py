from fastapi import Depends
from apis.guide.api import router_guide
from db.async_database import depends_get_db_session
from db.async_database import AsyncSession
from exts.responses.json_response import Success, Fail
from utils.datatime_helper import diff_days_for_now_time


@router_guide.get("/guide_list", summary='获取可以预约医生列表信息')
async def callbadk(db_session: AsyncSession = Depends(depends_get_db_session)):
    '''
    :param db_session: 数据库连接依赖注入对象\n\n
    :return: 返回可以预约医生列表信息\n\n
    '''
    # info = await DoctorServeries.get_doctor_list_infos(db_session)
    return Success()


@router_guide.get("/doctor_scheduling_info", summary='获取医生排班信息')
async def callbadk(forms = Depends(), db_session: AsyncSession = Depends(depends_get_db_session)):
    # 当前系统日期对比，判断当前是否是否已操作系统时间，超过系统时间预约信息则无法查询
    if forms.start_time:
        try:
            is_limt_start_time = diff_days_for_now_time(forms.start_time)
            if is_limt_start_time < 0:
                return Fail(message="当前日期无效,无排班信息!")
        except:
            return Fail(message="当前日期无效,日期格式错误!")
    # 查询排班信息