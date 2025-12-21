# 任务存储，将任务存储在哪（默认为内存），这里存储在mongodb中
from apscheduler.jobstores.mongodb import MongoDBJobStore
# 执行器，线程池执行器
from apscheduler.executors.pool import ThreadPoolExecutor
# 调度器，后台调度
from apscheduler.schedulers.background import BackgroundScheduler
# 触发器在执行中直接定义

# 自定义模块
from project.zhihu.api.mongo_config import mongo_config
from project.zhihu.Scheduler_task.task_log import logger


mongo_store = MongoDBJobStore(
    host=mongo_config['host'],
    port=mongo_config['port'],
    database=mongo_config['db'],
    collection='jobs'
    # username=mongo_config['username'],
    # password=mongo_config['password']
)

scheduler = BackgroundScheduler(
    jobstores={
        'default': mongo_store
    },
    executor={
        'default': ThreadPoolExecutor(max_workers=20)
    },
    job_defaults={
        # 假如一个任务堆积了很多次，是执行最新的一次（True）还是执行多次（False）
        'coalesce': True,
        # 任务同时执行最大数
        'max_instances': 5,
        # 如果一个任务没有在规定的时间内执行，并且发现的时候已经过去一段时间了，是否要重新执行（给出时间的阈值（秒），在这个时间内都可以重新被执行）
        'misfire_grace_time': 3600
    },
    timezone="Asia/Shanghai",
    logger=logger
)

# print("scheduler 完成")

# 下面利用装饰器添加任务

# 凌晨刷新cookies的任务，按照网页不同可以添加多个
run_jods_refresh = []
def add_job_refresh(func):
    run_jods_refresh.append(func)
    return func

# 判断cookies是否可用的任务，按照网页不同可以添加多个
run_jods_check_cookies = []
def add_job_check_cookies(func):
    run_jods_check_cookies.append(func)
    return func

# 刷新不可用的cookies，按照网页不同可以添加多个
run_jods_refresh_unusable_cookies = []
def add_job_refresh_unusable_cookies(func):
    run_jods_refresh_unusable_cookies.append(func)
    return func

# 获取新用户的cookies，按照网页不同可以添加多个
run_jods_get_cookies = []
def add_job_get_cookies(func):
    run_jods_get_cookies.append(func)
    return func


from project.zhihu.Scheduler_task.tasks import *

# 不同的任务，执行的时间不一样
# 每日刷新cookies，凌晨执行，使用cron
for func in run_jods_refresh:
    scheduler.add_job(func, 'cron', hour=0,  minute=1)
# 判断cookies是否可用，使用interval，每一小时执行一次
for func in run_jods_check_cookies:
    scheduler.add_job(func, 'interval', minutes=60)
# 刷新不可用的cookies，使用interval，每两小时执行一次
for func in run_jods_refresh_unusable_cookies:
    scheduler.add_job(func, 'interval', minutes=120)
# 获取新用户的cookies，使用interval，每30分钟执行一次
for func in run_jods_get_cookies:
    scheduler.add_job(func, 'interval', minutes=30)
