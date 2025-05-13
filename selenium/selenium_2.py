from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = r"https://www.lagou.com/"

service = Service(r"/selenium/chromedriver-win64\chromedriver.exe")
options = Options()
options.add_experimental_option("detach", True)
bowser = webdriver.Chrome(service=service, options=options)
bowser.get(url)

city_suggest_element = bowser.find_element(By.XPATH, "//*[@id='lg_tbar']/div[1]/ul/li[1]/em")
city_suggest_element.click()    # 点击城市
# 切换城市
city_element = bowser.find_element(By.XPATH, "//div[5]/ul/li[5]/span")
city_element.click()
# 搜索职位
search_element = bowser.find_element(By.XPATH,"//*[@id='search_input']")
search_element.send_keys("python爬虫工程师", Keys.ENTER)


# By 的多种定位方式
#  By.XPATH: 路径定位
#  By.ID: id定位
#  By.CLASS_NAME: class定位
#  By.NAME: name定位
#  By.TAG_NAME: 标签定位
#  By.LINK_TEXT: 链接定位
#  By.PARTIAL_LINK_TEXT: 部分链接定位
#  By.CSS_SELECTOR: css定位

# Keys类有键盘所有操作的常量，可以执行键盘上的操作



