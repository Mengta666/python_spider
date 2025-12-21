import configparser


# 数据库配置读取

api_config_path = r"E:\python\spider\project\zhihu\cnf\api.cnf"

mongo_cnf = configparser.ConfigParser()
mongo_cnf.read(api_config_path, encoding="utf-8")
mongo_config = {
    "host": mongo_cnf["mongo"]["host"],
    "port": int(mongo_cnf["mongo"]["port"]),
    "db": mongo_cnf["mongo"]["db"],
    "username": mongo_cnf["mongo"]["username"],
    "password": mongo_cnf["mongo"]["password"]
}

# print(mongo_config)

