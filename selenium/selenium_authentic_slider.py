import time
import json
import pyautogui

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from random import uniform, randint



# 对于滑块验证码的相关操作

# 自动识别登录图片并点击：
def auto_click_picture(pic_path):
    pic_path = pic_path
    loc = pyautogui.locateOnScreen(pic_path)
    center = pyautogui.center(loc)
    pyautogui.click(center)


# 每秒钟拖动的距离，避免过快（模拟鼠标滑动）
def move_speed(distance):
    slow_distance = []
    while sum(slow_distance) <= distance:
        slow_distance.append(randint(-2, 20))

    if sum(slow_distance) != distance:
        slow_distance.append(distance - sum(slow_distance))
    return slow_distance

# 拖动滑块
def drag_slider(tracks, path):
    slider_pic_loc = pyautogui.locateOnScreen(r"E:\python\spider\selenium\picture\slider.PNG", confidence=0.80)
    center = pyautogui.center(slider_pic_loc)
    pyautogui.moveTo(center)
    pyautogui.mouseDown()         # 按下鼠标左键
    for track in tracks:
        pyautogui.move(track, uniform(-2,2))
    pyautogui.mouseUp()


# 豆瓣登录
def login(url, info, pic_path, page_scale):
    service = Service(r"chromedriver-win64\chromedriver.exe")
    options = Options()
    options.debugger_address="127.0.0.1:8888"
    bowser = webdriver.Chrome(service=service, options=options)
    bowser.get(url)

    # 切换登陆方式
    bowser.find_element(By.XPATH, '//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()

    # 输入登陆的账号和密码
    username_element = bowser.find_element(By.XPATH, '//*[@id="username"]')
    ActionChains(bowser).click(username_element).pause(0.5)\
    .send_keys(f"{info['phone_number']}").pause(1).perform()
    time.sleep(uniform(1, 2))

    password_element = bowser.find_element(By.XPATH, '//*[@id="password"]')
    ActionChains(bowser).click(password_element).pause(0.5)\
    .send_keys(f"{info['password']}").pause(1).perform()
    time.sleep(uniform(1,2))

    # 点击登陆按钮
    # 第一种方式：易被检测
    # bowser.find_element(By.XPATH, '//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()
    # 换一种方式：使用pyautogui模块，自动识别登录图片并点击，模拟鼠标点击
    time.sleep(uniform(1,2))
    auto_click_picture(pic_path["login_picture"])

    # 出现滑块验证码
    # 处理滑块验证码
    # 首先获取验证码背景图片与滑块
    # 在一个iframe里面，需要进行窗口切换
    WebDriverWait(bowser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="tcaptcha_iframe_dy"]')))
    iframe = bowser.find_element(By.XPATH, '//*[@id="tcaptcha_iframe_dy"]')
    bowser.switch_to.frame(iframe)
    # 获取背景图片
    # 获取元素的实际渲染大小
    WebDriverWait(bowser, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="slideBg"]')))
    time.sleep(uniform(1, 2))
    back_pic = bowser.find_element(By.XPATH, '//*[@id="slideBg"]')
    rect = bowser.execute_script("""
        var elem = arguments[0];
        var rect = elem.getBoundingClientRect();
        return {width: rect.width, height: rect.height};
    """, back_pic)
    back_location = back_pic.location   # 取得当前背景在iframe中的坐标
    with open(f"{pic_path['back_picture']}", "wb") as f:
        f.write(back_pic.screenshot_as_png)

    # 获取滑块图片（会随机获取到两种滑块，一种是图片上的滑块，一种是图片下方拖动的滑块，这里需要图片上的滑块）
    slide_pic_1 = bowser.find_element(By.XPATH, '//*[@id="tcOperation"]/div[7]')
    slide_pic_2 = bowser.find_element(By.XPATH, '//*[@id="tcOperation"]/div[8]')
    if slide_pic_1.location['y'] < slide_pic_2.location['y']:
        """
        图片中的滑块的y值要小于图片下方的滑块的y值，因为第一种在第二种的上方
        """
        slide_pic = slide_pic_1
    else:
        slide_pic = slide_pic_2
    with open(f"{pic_path['slider_picture']}", "wb") as f:
        f.write(slide_pic.screenshot_as_png)
    slide_pic_location = slide_pic.location # 取得当前滑块在iframe中的坐标

    # 第二步，使用opencv对图片进行比对，获得缺失模块的位置，得到大概应该滑动的距离
    # 使用opencv的模板匹配函数：cv2.matchTemplate()
    from CalculateDistance import CalculateDistance
    offset_x = slide_pic_location['x'] - back_location['x']
    offset_y = slide_pic_location['y'] - back_location['y']
    cal_distance = CalculateDistance(pic_path["back_picture"], pic_path["slider_picture"],
                                     offset_x, offset_y, page_scale,True)

    # 得到滑动距离
    distance = cal_distance.run()
    print("滑动距离：", distance)

    # 第三步，使用pyautogui模块，模拟鼠标滑动，实现自动滑动滑块
    time.sleep(uniform(1, 2))
    track = move_speed(distance)  # 设置滑动速度
    drag_slider(track, pic_path["slider_picture_bottom"])
    time.sleep(uniform(1, 2))




if __name__ == '__main__':
    url = r"https://accounts.douban.com/passport/login?redir=https://www.douban.com/doumail/"
    pic_path = {
        "login_picture": r"picture/douban/login_picture.jpeg",                        # 豆瓣登录的按钮
        "slider_picture": r"picture/douban/slider_picture.jpeg",                      # 背景图片中的滑块
        "back_picture": r"picture/douban/back_picture.jpeg",                          # 背景图片
        "slider_picture_bottom": r"picture/douban/slider_picture.jpeg",               # 底部的滑块（用来匹配按下的位置，自行截图配置）
    }
    with open("username_password/douban.json",  "r", encoding="utf-8") as f:
        info = json.loads(f.read())
    # 浏览器载入原始的页面在没有特殊缩放的情况下是1：1，并且selenium截取的图片也是按照1：1截取的，计算滑块想要移动的距离（像素块）时，也是按照1：1计算的
    # 但是一般情况下，计算机有默认的缩放比例（参见系统设置显示里面的缩放），高分辨率对于小屏幕的推荐缩放是1.5，意味着原本的1：1的图片，在1.5倍的缩放下，对一个100px的图片，
    # 会放大到150px，所以在原来1：1的距离上还需要乘以1.5才能得到当前缩放下的移动距离，缩放系数page_scale，可根据需求进行设置
    page_scale = 1.5
    login(url, info, pic_path, page_scale)
