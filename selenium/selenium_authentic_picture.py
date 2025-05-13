import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client

from CalculateDistance import CalculateDistance




# 模拟登录有图形验证码的网站

# 登陆函数
def login(url):
    service = Service(r"/selenium/chromedriver-win64\chromedriver.exe")
    options = Options()
    options.debugger_address="127.0.0.1:8888"
    options.page_load_strategy = "normal"
    bowser = webdriver.Chrome(service=service, options=options)
    bowser.get(url)

    login_element = bowser.find_element(By.XPATH, "//*[@id='login-register']")
    ActionChains(bowser).move_to_element(login_element).perform()

    # 提取用户名与密码
    with open("user_pass.json",  "r", encoding="utf-8") as f:
        info = json.loads(f.read())

    # 输入用户名
    WebDriverWait(bowser,10).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='userone']/section/form/div[1]/div")))
    login_username_element = bowser.find_element(By.XPATH, "//*[@id='userone']/section/form/div[1]/div")
    ActionChains(bowser).click(login_username_element)\
    .pause(1).send_keys(info["username"]).perform()

    # 输入密码
    WebDriverWait(bowser,10).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='userone']/section/form/div[2]/div")))
    login_password_element = bowser.find_element(By.XPATH, "//*[@id='userone']/section/form/div[2]/div")
    ActionChains(bowser).click(login_password_element)\
    .pause(1).send_keys(info["password"]).perform()

    # 提取验证码
    auth_picture = bowser.find_element(By.XPATH, "//*[@id='userone']/section/form/div[3]/div/img").screenshot_as_png
    authentic_code = Chaojiying_Client(info["username"], info["password"], info["soft_id"])
    result = authentic_code.PostPic(auth_picture, 1902)["pic_str"]

    # 输入验证码
    WebDriverWait(bowser,20).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='userone']/section/form/div[4]/div")))
    login_auth_element = bowser.find_element(By.XPATH, "//*[@id='userone']/section/form/div[4]/div")
    ActionChains(bowser).click(login_auth_element).pause(1).send_keys(result).perform()

    WebDriverWait(bowser,10).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='userone']/section/form/div[6]/button")))
    login_element = bowser.find_element(By.XPATH, "//*[@id='userone']/section/form/div[6]/button")
    ActionChains(bowser).click(login_element).perform()





if __name__ == '__main__':
    url = r"https://www.chaojiying.com/"
    login(url)



