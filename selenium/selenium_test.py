import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 指定浏览器驱动位置，创建服务
service = Service(r"/selenium/chromedriver-win64\chromedriver.exe")
# 将服务放入浏览器中，并设置属性
browser = webdriver.Chrome(service=service)
browser.maximize_window()
# 使用浏览器访问服务
browser.get("https://www.baidu.com")
time.sleep(10)
browser.close()