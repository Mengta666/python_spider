# 定义任务
from project.zhihu.Scheduler_task import (
    add_job_refresh,
    add_job_check_cookies,
    add_job_get_cookies,
    add_job_refresh_unusable_cookies
)
from project.zhihu.Scheduler_task.refresh_cookies import RefreshCookies

@add_job_refresh
def refresh_cookies():
    """每日凌晨刷新cookies"""
    RefreshCookies.refresh_cookies()

@add_job_check_cookies
def check_cookies():
    """检查cookies，将不能使用的cookie设置为异常"""
    RefreshCookies.set_error()

@add_job_refresh_unusable_cookies
def refresh_unusable_cookies():
    """刷新异常的cookies"""
    RefreshCookies.refresh_unusable_cookies()

@add_job_get_cookies
def get_cookies():
    """获取新用户的cookies"""
    RefreshCookies.get_cookies()


