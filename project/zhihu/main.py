from project.zhihu.api import app
from project.zhihu.api.cookies import CookieAPI
from project.zhihu.Scheduler_task import scheduler

from project.zhihu.Scheduler_task.clear_db import clear_db



if __name__ == '__main__':
    clear_db()
    scheduler.start()
    app.add_url_rule("/cookies/", view_func=CookieAPI.as_view("cookies"))
    app.run(debug=False, host='0.0.0.0', port=5000)
