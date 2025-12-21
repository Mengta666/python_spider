import time
import pymongo
import base64

from project.zhihu.api.database import zhihu_cookies_collention
from project.zhihu.api.database import zhihu_new_user_collention
from flask.views import MethodView
from flask import request, jsonify

from project.zhihu.zhihu_login.login import ZhiHuLogin
from pymongo.errors import DuplicateKeyError

from project.zhihu.api.encrypt import aes_encrypt

# 全程使用username进行查找，需要保证username唯一

class CookieAPI(MethodView):

    # 请求cookie，随机返回一个用户的cookie
    def get(self):
        username = request.json.get('username')
        # 查询条件，忽略id
        ingore_id = {
            "_id" : 0
        }
        if username is None:
            cookie = zhihu_cookies_collention.find_one(projection=ingore_id)
            if cookie is None:
                result = {
                    "code": 400,
                    "msg": "当前数据库中没有用户",
                    "data": None
                }
            else:
                cookie['password'] = base64.b64encode(cookie['password']).decode('utf-8')
                cookie['iv'] = base64.b64encode(cookie['iv']).decode('utf-8')
                result = {
                    "code": 200,
                    "msg": "获取成功",
                    "data": cookie
                }
        else:
            cookie = zhihu_cookies_collention.find_one({
                "username": username,
                "status": "正常"
            }, projection=ingore_id)
            if cookie is None:
                result = {
                    "code": 400,
                    "msg": f"请求的用户{username}不可用",
                    "data": None
                }
            else:
                cookie['password'] = base64.b64encode(cookie['password']).decode('utf-8')
                cookie['iv'] = base64.b64encode(cookie['iv']).decode('utf-8')
                result = {
                    "code": 200,
                    "msg": "获取成功",
                    "data": cookie
                }
        return jsonify(result)

    # 按照用户名和密码查询cookie
    def post(self):
        # 只接受 JSON 格式的请求
        if not request.is_json:
            return jsonify({
                "code": 400,
                "msg": "请求格式必须为 JSON",
                "data": None
            })

        username = request.json.get('username')

        # 输入验证
        if not username:
            return jsonify({
                "code": 400,
                "msg": "用户名无效",
                "data": None
            })

        # 查询条件，忽略id
        ingore_id = {
            "_id": 0
        }
        cookie = zhihu_cookies_collention.find_one({
            "username": username,
            "status": "正常"
        }, projection=ingore_id)
        if cookie is None:
            result = {
                "code": 400,
                "msg": f"请求的用户{username}不可用",
                "data": None
            }
        else:
            cookie['password'] = base64.b64encode(cookie['password']).decode('utf-8')
            cookie['iv'] = base64.b64encode(cookie['iv']).decode('utf-8')
            result = {
                "code": 200,
                "msg": "获取成功",
                "data": cookie
            }
        return jsonify(result)


    # 更新cookie，put请求
    def put(self):
        # 只接受 JSON 格式的请求
        if not request.is_json:
            return jsonify({
                "code": 400,
                "msg": "请求格式必须为 JSON",
                "data": None
            })
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            return jsonify({
                "code": 400,
                "msg": "用户名或密码无效",
                "data": None
            })
        try:
            # 检查用户是否存在
            is_exist = zhihu_cookies_collention.find_one({"username": username})

            if is_exist:
                # 更新已有记录
                # 使用账号密码登录，返回 cookie 和 headers
                try:
                    user_data = zhihu_cookies_collention.find_one({"username": username})
                    from project.zhihu.zhihu_login.check_cookie import CheckCookies
                    if not CheckCookies.check_cookies_zhihu(user_data['headers']):
                        login = ZhiHuLogin(username=username, password=password)
                        cookie, headers = login.main()
                        # 更新密码
                        pw, iv = aes_encrypt(password)
                        # 构造数据对象
                        data = {
                            "username": username,
                            "password": pw,
                            'iv': iv,
                            "cookie": cookie,
                            "headers": headers,
                            "status": "正常",
                            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
                        # 更新条件
                        update_condition = {
                            "username": username
                        }
                        result = zhihu_cookies_collention.update_one(
                            update_condition,
                            {"$set": data}
                        )
                        if result.matched_count == 0:
                            return jsonify({
                                "code": 500,
                                "msg": "更新失败：未找到匹配的数据"
                            })
                        # 返回结果，移除可能的 _id 字段，data在插入后，会被添加一个新的属性（object类），所以需要移除
                        data.pop("_id", None)  # 安全移除 _id，仅在 insert_one 后存在
                        data['password'] = base64.b64encode(data['password']).decode('utf-8')
                        data['iv'] = base64.b64encode(data['iv']).decode('utf-8')
                        return jsonify({
                            "code": 200,
                            "msg": "已在数据库中更新数据",
                            "data": data
                        })
                    else:
                        return jsonify({
                            "code": 200,
                            "msg": "数据已存在并且已是最新"
                        })
                except Exception as e:
                    status = {
                        "status": "异常"
                    }
                    condition = {
                        "username": username
                    }
                    zhihu_cookies_collention.update_one(condition, {"$set": status})
                    return jsonify({
                        "code": 500,
                        "msg": f"更新失败：{str(e)}，已将用户状态设置为异常，将在后台再次更新，请用其他正常的cookie"
                    })


            # 为新用户，插入新记录到new_user集合中
            else:
                # 插入新记录，加密
                pw, iv = aes_encrypt(password)
                # 寻找用户是否存在
                is_exist = zhihu_new_user_collention.find_one({"username": username})
                if is_exist:
                    new_user_info = {
                        "username": username,
                        "password": pw,
                        'iv': iv
                    }
                    zhihu_new_user_collention.update_one({"username": username},  {"$set": new_user_info})
                    return jsonify({
                        "code": 200,
                        "msg": "用户名已存在，仅更新密码"
                    })
                else:
                    new_user_info = {
                        "username": username,
                        "password": pw,
                        'iv': iv
                    }
                    zhihu_new_user_collention.insert_one(new_user_info)
                    return jsonify({
                        "code": 200,
                        "msg": "已插入新用户到数据库中，将在后台处理，请用其他已有的cookie",
                    })
        except DuplicateKeyError:
            return jsonify({
                "code": 400,
                "msg": "用户名已存在，无法插入重复记录",
                "data": None
            })
        except pymongo.errors.PyMongoError as e:
            return jsonify({
                "code": 500,
                "msg": f"数据库操作失败：{str(e)}",
                "data": None
            })
        except Exception as e:
            return jsonify({
                "code": 500,
                "msg": f"请求失败：{str(e)}",
                "data": None
            })


    # 删除cookie
    def delete(self):
        # 只接受 JSON 格式的请求
        if not request.is_json:
            return jsonify({
                "code": 400,
                "msg": "请求格式必须为 JSON",
                "data": None
            })
        username = request.json.get('username')
        if username is None:
            result = {
                "code": 400,
                "msg": "参数错误，请传入username",
                "data": None
            }
        else:
            delete_info = zhihu_cookies_collention.delete_one({
                "username": username
            })
            if delete_info.deleted_count == 0:
                result = {
                    "code": 500,
                    "msg": "删除失败，请检查用户名是否正确",
                }
            else:
                result = {
                    "code": 200,
                    "msg": "删除成功"
                }
        return jsonify(result)






