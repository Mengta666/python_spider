# 项目目录结构
```plaintext
project                           # 项目根目录
└── zhihu                         # 项目
    ├── README.md
    ├── requirements.txt          # 依赖包
    ├── main.py                   # 主程序
    ├── cnf                       # 配置文件
    │   ├── login.cnf             # zhihu_login登录账号获取cookies所用的全局配置
    │   ├── task.cnf              # 定时任务配置文件
    │   └── api.cnf               # api接口配置
    ├── zhihu_login               # 登陆组件
    │   ├── zhihu_login.py        # 登陆爬虫
    │   ├── check_cookie.py       # 检验获得的cookie是否有效
    │   ├── login_log.py          # 登陆日志脚本
    │   ├── train_pic_json        # 识别的背景图片留存（目录）
    │   ├── click_pic.png         # 滑块按钮的图片
    │   ├── login_pic.png         # 登陆按钮的图片
    │   └── slider_fsterrcnn.pth  # 用于识别的模型（详细查看 https://github.com/Mengta666/slider_model）
    ├── api                       # api接口，用来调用登陆组件，返回登陆后的cookies以供本地使用
    │   ├── __init__.py           # api接口，使用flask框架
    │   ├── mongo_config.py       # 数据库配置
    │   ├── database.py           # mongo数据库操作，定义了一个变量，用来操作数据库
    │   └── cookies.py            # 获取数据库中登陆成功后的cookies
    ├── Scheduler_task
    │   ├── __init__.py           # 定时任务配置，并将任务集导入
    │   ├── clear_db.py           # 启动定时任务时，先清除前面数据库中残留的任务
    │   ├── refresh_cookies.py    # 定时任务，刷新cookie的任务函数
    │   ├── task_log.py           # 定时任务日志脚本
    │   └── tasks.py              # 任务集
    └── zhihu                     # 分布式爬虫（登陆后使用的）

```

### 说明
-  **zhihu_login**：确保修改zhihu_login.py中的config路径和对于config中的其他配置路径
-  **api**：确保修改api.py中的配置路径和对应数据库配置