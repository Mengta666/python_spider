# 动作链，对简单的一些需要点击，拖斗，滚动，右键等操作事件：ActionChains类

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


service = Service(executable_path=r"/selenium/chromedriver-win64\chromedriver.exe")
options = Options()
# options.add_experimental_option("detach", True)           # 保持窗口不关闭
# options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 将浏览器标记为无自动化
# options.add_argument("--disable-blink-features=AutomationControlled")       # 隐藏浏览器不必要标识
options.debugger_address="127.0.0.1:8888"

url = r"https://www.12306.cn/"
bowser = webdriver.Chrome(service=service, options=options)
bowser.get(url)

# 由车票栏只能悬停显示，不能点击，需要用到ActionChains类
# 把鼠标悬停在车票上
ticket_bar = bowser.find_element(By.XPATH, r"//*[@id='J-chepiao']/a")
ActionChains(bowser).move_to_element(ticket_bar).perform()        # 悬停到指定元素，并执行（使用perform()）

# 点击单程进入新的窗口
single_ticket = bowser.find_element(By.XPATH, r"//*[@id='megamenu-3']/div[1]/ul/li[1]/a")
ActionChains(bowser).click(single_ticket).perform()

# 开始查票
# 首先输入出发地
start_place = bowser.find_element(By.XPATH,r"//*[@id='fromStationText']")
ActionChains(bowser)\
    .click(start_place)\
    .pause(1)\
    .send_keys("西安")\
    .pause(1)\
    .send_keys(Keys.ARROW_DOWN)\
    .pause(0.5)\
    .send_keys(Keys.ENTER).perform()
# 输入目的地
stop_place = bowser.find_element(By.XPATH,r"//*[@id='toStationText']")
ActionChains(bowser)\
    .click(stop_place)\
    .pause(1)\
    .send_keys("北京")\
    .pause(1)\
    .send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN)\
    .pause(0.5).send_keys(Keys.ENTER).perform()

# 选择日期
date_element = bowser.find_element(By.XPATH,r"//*[@id='train_date']")
ActionChains(bowser)\
    .click(date_element)\
    .pause(1)\
    .send_keys(Keys.ARROW_RIGHT*10)\
    .pause(1)\
    .send_keys(Keys.BACKSPACE*10)\
    .pause(1)\
    .send_keys("2025-05-12").pause(0.5)\
    .send_keys(Keys.ENTER)\
    .perform()

# 勾选火车类型
train_type_element_1 = bowser.find_element(By.XPATH,r"//div[2]/div[2]/div[2]/ul/li[1]/input")
train_type_element_1.click()
train_type_element_2 = bowser.find_element(By.XPATH,r"//div[2]/div[2]/div[2]/ul/li[2]/input")
train_type_element_2.click()
train_type_element_3 = bowser.find_element(By.XPATH,r"//div[2]/div[2]/div[2]/ul/li[3]/input")
train_type_element_3.click()

# 选择发车事件
# 由于是复选框，需要一个select类进行选择操作
train_start_element = bowser.find_element(By.XPATH,r"//*[@id='cc_start_time']")
Select(train_start_element).select_by_visible_text("12:00--18:00")   # 选择12:00--18:00

# 查询
search_element = bowser.find_element(By.XPATH,r'//*[@id="query_ticket"]')
search_element.click()



