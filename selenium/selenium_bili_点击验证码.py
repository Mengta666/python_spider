import random
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client


# bilibili是点击式的验证方式，使用超级鹰识别验证码，自动返回验证码位置，还是很快速的


def login(url):
    service = Service(r"chromedriver-win64\chromedriver.exe")
    options = Options()
    options.debugger_address="127.0.0.1:8888"
    bowser = webdriver.Chrome(service=service, options=options)
    bowser.get("https://www.bilibili.com")

    WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='i_cecream']/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div/div")))
    login_element = bowser.find_element(By.XPATH, "//*[@id='i_cecream']/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div/div")
    login_element.click()

    time.sleep(random.uniform(1,2))

    WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[4]/div[2]/form/div[1]/input")))
    username_element = bowser.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/div[2]/form/div[1]/input")
    ActionChains(bowser).click(username_element).pause(1).send_keys("18585280717")\
    .pause(1).perform()

    WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[4]/div[2]/form/div[3]/input")))
    password_element = bowser.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/div[2]/form/div[3]/input")
    ActionChains(bowser).click(password_element).pause(1).send_keys("password")\
    .pause(1).perform()

    bowser.find_element(By.XPATH,"/html/body/div[4]/div/div[4]/div[2]/div[2]/div[2]").click()


    # 获取登录的验证码图片
    WebDriverWait(bowser, 10).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div[6]/div")))
    bg_pic_element = bowser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[6]/div")
    pic_width = bg_pic_element.size["width"]
    pic_height = bg_pic_element.size["height"]
    bg_pic = bg_pic_element.screenshot_as_png

    with open(r"E:\python\spider\selenium\user_pass.json",  "r", encoding="utf-8") as f:
        info = json.loads(f.read())
    chaoj_client = Chaojiying_Client(info["username"],  info["password"], info["soft_id"])
    loc = chaoj_client.PostPic(bg_pic, 9004)["pic_str"]
    print(loc[:])
    loc = loc.split("|")                  # 返回的位置坐标，左上角为原点
    # ActionChains要对某元素进行操作时，默认的鼠标位置在该元素的中心
    for i in loc:
        x, y = i.split(",")
        x_loc = int(x) - pic_width / 2
        y_loc = int(y) - pic_height / 2
        ActionChains(bowser).move_to_element_with_offset(bg_pic_element, x_loc, y_loc).click().perform()

    # 点击确认
    time.sleep(random.uniform(1,2))
    WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div[6]/div/div/div[3]/a/div")))
    bowser.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[6]/div/div/div[3]/a/div").click()


if __name__ == '__main__':
    url = ""
    login(url)