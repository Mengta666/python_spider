from project.zhihu.api.mongo_config import mongo_config
from pymongo import MongoClient

# 链接mongodb数据库（zhihu）
mongo_client = MongoClient(mongo_config["host"], mongo_config["port"])
# 库：zhihu
zhihu_cookies_db = mongo_client[mongo_config["db"]]
# 集合: cookies
zhihu_cookies_collention = zhihu_cookies_db["cookies"]
# 集合： new_user
zhihu_new_user_collention = zhihu_cookies_db["new_users"]