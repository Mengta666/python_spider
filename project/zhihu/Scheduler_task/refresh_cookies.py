import time
from project.zhihu.zhihu_login.check_cookie import CheckCookies
from project.zhihu.zhihu_login.login import ZhiHuLogin
from project.zhihu.api.database import zhihu_cookies_collention
from project.zhihu.api.database import zhihu_new_user_collention
from project.zhihu.Scheduler_task.task_log import logger

from project.zhihu.api.encrypt import (
    aes_encrypt,
    aes_decrypt
)


# mongodb中的数据结构
# data = {
#     "username": username,
#     "password": password,
#     "cookie": cookie,
#     "headers": headers,
#     "status": "正常",
#     "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# }

class RefreshCookies:

    #  获取Cookie和headers，并更新数据库
    @staticmethod
    def get_cookie_headers(username, password):
        """获取Cookie和headers，并更新数据库"""
        try:
            zhihu_login = ZhiHuLogin(username=username, password=password)
            cookies, headers = zhihu_login.main()
            update_condition = {
                "username": username
            }
            # 重新加密密码
            pw, iv = aes_encrypt(password)
            data = {
                "password": pw,
                "iv": iv,
                "cookie": cookies,
                "headers": headers,
                "status": "正常"
            }
            result = zhihu_cookies_collention.update_one(update_condition, {"$set": data})
            if result.matched_count == 0:
                logger.warn(f"Cookie: {username} 更新失败")
                return None, None
            else:
                logger.warn(f"Cookie: {username} 更新成功")
                return cookies, headers
        except Exception as e:
            logger.error(f"登录时出错{e}，已将Cookie状态设置为异常")
            status = {
                "status": "异常"
            }
            update_condition = {
                "username": username
            }
            zhihu_cookies_collention.update_one(update_condition, {"$set": status})
            return None, None

    # 定时刷新已有的Cookie
    @staticmethod
    def refresh_cookies():
        """"定时刷新已有的Cookie"""
        logger.info("正在刷新Cookie")
        zhihu_infos = zhihu_cookies_collention.find()
        while True:
            try:
                zhihu_info = next(zhihu_infos)
                # 密码解密
                password = aes_decrypt(zhihu_info["password"], zhihu_info["iv"])
                RefreshCookies.get_cookie_headers(zhihu_info["username"], password)
            except StopIteration:
                logger.info("刷新Cookie完成，数据库中已全部更新")
                break

    # 设置Cookie异常
    @staticmethod
    def set_error():
        """设置Cookie异常"""
        logger.info("正在检查Cookie是否可用")
        condition = {"status": "正常"}
        zhihu_infos = zhihu_cookies_collention.find(condition)
        while True:
            try:
                zhihu_info = next(zhihu_infos)
                logger.info(f"正在检查 {zhihu_info["username"]} 的Cookie")
                zhihu_headers = zhihu_info["headers"]
                if not CheckCookies.check_cookies_zhihu(zhihu_headers):
                    status = {
                        "status": "异常"
                    }
                    update_condition = {
                        "username": zhihu_info["username"]
                    }
                    result = zhihu_cookies_collention.update_one(update_condition, {"$set": status})
                    if result.matched_count == 0:
                        logger.warn(f"Cookie: {zhihu_info["username"]} 设置异常失败")
                    else:
                        logger.warn(f"已将 Cookie: {zhihu_info["username"]} 设置异常")
                else:
                    logger.info(f"Cookie: {zhihu_info["username"]} 可用")
            except StopIteration:
                logger.info("数据库中cookies已全部检查完毕")
                break


    # 刷新不能使用的Cookie（状态为异常）
    @staticmethod
    def refresh_unusable_cookies():
        """刷新不能使用的Cookie（状态为异常）"""
        logger.info("正在搜索不能使用的Cookie（状态为异常）")
        condition = {"status": "异常"}
        zhihu_infos = zhihu_cookies_collention.find(condition)
        while True:
            try:
                zhihu_info = next(zhihu_infos)
                logger.info(f"正在重新更新异常的Cookie: {zhihu_info["username"]}")
                # 解密
                password = aes_decrypt(zhihu_info["password"], zhihu_info["iv"])
                RefreshCookies.get_cookie_headers(zhihu_info["username"], password)
            except StopIteration:
                logger.info("搜索完成，数据库中cookie已经刷新")
                break

    # 处理新的Cookie请求
    @staticmethod
    def get_cookies():
        """处理新的Cookie请求"""
        logger.info("正在处理新的Cookie请求")
        new_user_infos = zhihu_new_user_collention.find()
        while True:
            try:
                new_user_info = next(new_user_infos)
                try:
                    username = new_user_info["username"]
                    pw = new_user_info["password"]
                    # 对密码进行解密
                    password = aes_decrypt(pw, new_user_info["iv"])
                    zhihu_login = ZhiHuLogin(username=username, password=password)
                    cookies, headers = zhihu_login.main()
                    # 重新对密码进行加密
                    pw, iv = aes_encrypt(password)
                    data = {
                        "username": username,
                        "password": pw,
                        'iv': iv,
                        "cookie": cookies,
                        "headers": headers,
                        "status": "正常",
                        "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    }
                    if zhihu_cookies_collention.find_one({"username": username}):
                        logger.warn(f"Cookie: {username} 已存在")
                        zhihu_new_user_collention.delete_one({"username": username})
                        continue
                    result = zhihu_cookies_collention.insert_one(data)
                    if result.inserted_id:
                        logger.info(f"Cookie: {username} 添加成功")
                        zhihu_new_user_collention.delete_one({"username": username})
                    else:
                        logger.warn(f"Cookie: {username} 添加失败")
                except Exception as e:
                    username = new_user_info["username"]
                    logger.error(f"对新用户{username}进行登录时出错{e}")
            except StopIteration:
                logger.info("已完成")
                break

if __name__ == '__main__':
    RefreshCookies.refresh_cookies()
    RefreshCookies.refresh_unusable_cookies()
    RefreshCookies.set_error()
    RefreshCookies.get_cookies()