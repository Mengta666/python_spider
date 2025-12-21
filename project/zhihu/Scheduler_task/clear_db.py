from project.zhihu.api.database import zhihu_cookies_db

def clear_db():
    zhihu_cookies_jobs_collection = zhihu_cookies_db["jobs"]
    zhihu_cookies_jobs_collection.delete_many({})