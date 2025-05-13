import time

from selenium.webdriver.chrome.service import  Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

url = r"https://www.lagou.com/"

service = Service(r"/selenium/chromedriver-win64\chromedriver.exe")
option = Options()
option.add_experimental_option("detach", True)        # 让窗口持久化显示
option.page_load_strategy =  "normal"
bowser = webdriver.Chrome(service=service, options=option)
bowser.get(url)


city_suggest_element = bowser.find_element(By.XPATH, "//*[@id='lg_tbar']/div[1]/ul/li[1]/em")
city_suggest_element.click()    # 点击城市
# 切换城市
WebDriverWait(bowser,10).until(ec.element_to_be_clickable((By.XPATH,"//div[5]/ul/li[5]/span")))
city_element = bowser.find_element(By.XPATH, "//div[5]/ul/li[5]/span")
city_element.click()
# 搜索职位
search_element = bowser.find_element(By.XPATH,"//*[@id='search_input']")
search_element.send_keys("python爬虫工程师", Keys.ENTER)  # 很多时候，可以不用等页面加载完就可以进行相应点击

# 切换到登录窗口，点击验证码登录，多个窗口时，按照时间先后顺序排列的窗口句柄，最后一个句柄为最新打开的窗口
bowser.switch_to.window(bowser.window_handles[-1])
WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='lg-passport-box']/div/div[2]/div/div[1]/div[2]")))
login_element = bowser.find_element(By.XPATH, "//*[@id='lg-passport-box']/div/div[2]/div/div[1]/div[2]")
login_element.click()

WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "//*[@id='lg-passport-box']/div/div[2]/div/div[1]/div[1]")))
login_element = bowser.find_element(By.XPATH, "//*[@id='lg-passport-box']/div/div[2]/div/div[1]/div[1]")
login_element.click()

# 下面是没有表单的登录方式
login_element_account = bowser.find_element(By.XPATH,"//*[@id='lg-passport-box']/div/div[2]/div/div[2]/div/div[1]/div[1]/input")
login_element_account.send_keys("13098071234")
login_element_password = bowser.find_element(By.XPATH,"//*[@id='lg-passport-box']/div/div[2]/div/div[2]/div/div[1]/div[2]/input")
login_element_password.send_keys("123456")
login_element_Enter = bowser.find_element(By.XPATH,"//*[@id='lg-passport-box']/div/div[2]/div/div[3]/button")
login_element_xieyi = bowser.find_element(By.XPATH,"//*[@id='lg-passport-box']/div/div[2]/div/div[4]/div[2]/div")
login_element_xieyi.click()
time.sleep(3)
login_element_Enter.click()
time.sleep(5)
# bowser.close()       #关闭这个登录窗口

# 当登录有表单的小窗口时
# 先定位到这个表单 frame = bowser.find_element(By.XPATH,"//*[@id='lg-passport-box']/div/div[2]/div/div[2]/iframe")
# 切换到表单: bowser.switch_to.frame(frame)
# 接下来登录通用
# 切换回表单所属的大窗口（网页） bowser.switch_to.default_content()

# 打开一个新的窗口
bowser.switch_to.window(bowser.window_handles[0])
bowser.switch_to.new_window('jd')
bowser.get("https://www.jd.com")
time.sleep(5)
bowser.close()

# 窗口切换到主页面
bowser.switch_to.window(bowser.window_handles[0])
city_suggest_element = bowser.find_element(By.XPATH, "//*[@id='lg_tbar']/div[1]/ul/li[1]/em")
city_suggest_element.click()    # 点击城市
# 切换城市
WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, "//div[5]/ul/li[2]/span")))
city_element = bowser.find_element(By.XPATH, "//div[5]/ul/li[2]/span")
city_element.click()

# 引入页面加载策略
# normal 默认，浏览器加载完页面后，再进行后续操作
# eager 浏览器加载完页面的静态资源，再进行后续操作，不需要等样式加载完毕
# none 等浏览器打开网址就开始进行下一步
# 使用 options 类传入策略
# 有些点击的浮动元素是动态资源，需要normal才能获取到对于元素


# 所以可以设置webdriver等待策略
# 引入隐式等待，设置等待时间，如果页面加载有了需要点击的元素，则进行后续操作，否则等待
# 隐式等待（implicitly_wait()）：在规定的时间范围内，不断查找需要操作的元素，如果找到了，则进行后续操作，否则继续查询，超时会抛出异常
# 显示等待（WebDriverWait()）：在指定的时间内，不断查询需要操作的元素，如果找到了，则进行后续操作，否则继续查询，超时会抛出异常（针对某一个元素）
# 显示需要导入模块：from selenium.webdriver.support.ui import WebDriverWait
#               from selenium.webdriver.support import expected_conditions as ec
# 隐式直接在option中添加



