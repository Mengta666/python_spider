import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

service = Service(r"/selenium/chromedriver-win64\chromedriver.exe")
options = Options()
bowser = selenium.webdriver.Chrome(service=service, options=options)
bowser.maximize_window()
bowser.get("https://www.baidu.com")
bowser.get("https://www.taobao.com")
# bowser.back()                # 后退
# bowser.forward()             # 前进
# bowser.refresh()             # 刷新
print(f"{bowser.page_source}")           # 获取网页源码
time.sleep(2)
bowser.close()                     # bowser.quit() 关闭浏览器并杀死进程，
                                   # close 只会关闭当前浏览器，而quit不仅会关闭浏览器也会杀掉驱动进程