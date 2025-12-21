import requests
import torch
import torchvision
import numpy as np
import pyautogui
import random
import os
import time
import json
import traceback
import configparser

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision import transforms
from PIL import Image
from PIL import ImageDraw
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException
)
from requests.exceptions import RequestException

# 自定义模块
from project.zhihu.zhihu_login.login_log import logger

class ZhiHuLogin:
    def __init__(self, config_path=r"E:\python\spider\project\zhihu\cnf\login.cnf", username=None, password=None, scale=1.5):
        """
        初始化 ZhiHuLogin，加载配置文件。
        :param config_path: 配置文件路径
        :param scale: 系统缩放系数
        """
        try:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"配置文件未找到: {config_path}")

            self.config = configparser.ConfigParser()
            self.config.read(config_path, encoding='utf-8')

            # 验证配置文件
            required_sections = ['path', 'user']
            required_path_keys = ['driver_path', 'login_url', 'login_pic', 'click_pic', 'model_path', 'save_path']
            required_user_keys = ['phone_number', 'password']

            for section in required_sections:
                if section not in self.config:
                    raise ValueError(f"配置文件缺少 '{section}' 部分")
            for key in required_path_keys:
                if key not in self.config['path']:
                    raise ValueError(f"配置文件 'path' 部分缺少 '{key}' 键")
            for key in required_user_keys:
                if key not in self.config['user']:
                    raise ValueError(f"配置文件 'user' 部分缺少 '{key}' 键")

            self.driver_path = self.config['path']['driver_path']
            self.login_url = self.config['path']['login_url']
            self.login_pic = self.config['path']['login_pic']
            self.click_pic = self.config['path']['click_pic']
            self.model_path = self.config['path']['model_path']

            if username is not None and password is not None:
                self.username = username
                self.password = password
            else:
                self.username = self.config['user']['phone_number']
                self.password = self.config['user']['password']

            self.scale = scale

            self.transform = transforms.Compose([
                transforms.ToTensor()
            ])
        except FileNotFoundError as e:
            logger.error(f"配置文件未找到: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"配置文件验证失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"初始化时发生未知错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def draw_box(self, image, box):
        """
        在图片上绘制红框并保存。
        :param image: PIL 图像对象
        :param box: (min_x, min_y, max_x, max_y) 的坐标元组
        """
        try:
            output_path = self.image_path['output_with_box']
            draw = ImageDraw.Draw(image)
            draw.rectangle(box, outline='red', width=3)
            image.save(output_path)
            logger.info(f"已保存带红框的预测图片至: {output_path}")
        except (KeyError, OSError) as e:
            logger.error(f"绘制红框失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"绘制红框时发生未知错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def load_model(self, model_path):
        """
        加载 Faster R-CNN 模型用于滑块检测。
        :param model_path: 模型权重路径
        :return: 加载的模型
        """
        try:
            model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
            num_classes = 2
            in_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
            device = torch.device("cpu")
            model.to(device)
            model.load_state_dict(torch.load(model_path, map_location=device))
            model.eval()
            return model
        except FileNotFoundError as e:
            logger.error(f"模型文件未找到: {model_path}")
            raise
        except RuntimeError as e:
            logger.error(f"加载模型权重失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"加载模型时发生未知错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def predict_slider(self):
        """
        使用深度学习模型预测滑块位置。
        :return: (min_x, min_y, max_x, max_y, image) 元组
        """
        try:
            if not os.path.exists(self.image_path['background_picture']):
                raise FileNotFoundError(f"背景图片未找到: {self.image_path['background_picture']}")

            model = self.load_model(self.model_path)
            image = Image.open(self.image_path['background_picture'])
            image_tensor = self.transform(image)
            with torch.no_grad():
                prediction = model([image_tensor])
            pre = prediction[0]
            boxes = pre['boxes'].cpu().numpy()
            scores = pre['scores'].cpu().numpy()
            if len(scores) == 0:
                raise ValueError("未在图片中检测到对象")
            max_score_index = np.argmax(scores)
            min_x, min_y, max_x, max_y = boxes[max_score_index]
            return min_x, min_y, max_x, max_y, image
        except FileNotFoundError as e:
            logger.error(f"背景图片未找到: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"预测滑块位置失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"预测滑块位置时发生未知错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def auto_click_picture(self):
        """
        使用 pyautogui 点击登录按钮。
        """
        try:
            click_login_loc = pyautogui.locateOnScreen(self.login_pic, confidence=0.8)
            if click_login_loc is None:
                raise ValueError("未找到登录按钮图片")
            center = pyautogui.center(click_login_loc)
            pyautogui.click(center)
        except pyautogui.PyAutoGUIException as e:
            # print(f"点击登录按钮失败: {e}")
            logger.error(f"点击登录按钮失败: {str(e)}")
            raise
        except Exception as e:
            # print(f"点击登录按钮失败: {e}")
            logger.error(f"点击登录按钮时发生未知错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def move_speed(self, distance):
        """
        生成模拟人类滑动的移动距离列表。
        :param distance: 总移动距离
        :return: 移动增量列表
        """
        try:
            slow_distance = []
            while sum(slow_distance) < distance:
                step = random.randint(1, 20)
                slow_distance.append(step)
            if sum(slow_distance) > distance:
                slow_distance[-1] = distance - sum(slow_distance[:-1])
            return slow_distance
        except Exception as e:
            logger.error(f"生成移动距离列表失败: {str(e)}\n{traceback.format_exc()}")
            raise

    def move(self, distance):
        """
        使用 pyautogui 移动滑块到指定距离。
        :param distance: 滑块移动距离
        """
        try:
            click_loc = pyautogui.locateOnScreen(self.click_pic, confidence=0.8)
            if click_loc is None:
                raise ValueError("未找到滑块图片")
            center = pyautogui.center(click_loc)
            pyautogui.moveTo(center)
            pyautogui.mouseDown()
            slow_distance = self.move_speed(distance)
            for dist in slow_distance:
                pyautogui.move(dist, random.uniform(-1, 1))
                time.sleep(random.uniform(0.01, 0.05))  # 添加小延迟模拟人类行为
            pyautogui.mouseUp()
        except pyautogui.PyAutoGUIException as e:
            # print(f"移动滑块失败: {e}")
            logger.error(f"移动滑块失败: {str(e)}")
            raise
        except Exception as e:
            # print(f"移动滑块失败: {e}")
            logger.error(f"移动滑块时发生未知错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def login(self):
        """
        执行登录流程，包含滑块验证。
        :return: 成功时返回 WebDriver 实例，失败时返回 None
        """
        max_try = 2
        logger.info("开始登录...")
        for i in range(max_try):
            driver = None
            success = False
            try:
                service = Service(executable_path=self.driver_path)
                options = Options()
                # 如果需要使用特定调试地址，取消以下注释
                # options.debugger_address = "127.0.0.1:8888"
                # options.add_argument("--headless")  # 无头模式，取消注释启用
                options.add_argument('--disable-blink-features=AutomationControlled')
                driver = WebDriver(service=service, options=options)
                driver.get(self.login_url)

                # 点击登录/注册按钮
                WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
                    (By.XPATH, '//*[@id="root"]/div/div[2]/header/div[1]/div[2]/div[2]/div/button')))
                login_element = driver.find_element(By.XPATH,
                                                    '//*[@id="root"]/div/div[2]/header/div[1]/div[2]/div[2]/div/button')
                login_element.click()

                # 选择密码登录
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,
                                                                                  '/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/div[1]/div[2]')))
                login_element = driver.find_element(By.XPATH,
                                                    '/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/div[1]/div[2]')
                login_element.click()

                # 输入用户名和密码
                driver.implicitly_wait(3)
                username_element = driver.find_element(By.XPATH,
                                                       '/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/div[2]/div/label/input')
                ActionChains(driver).click(username_element).send_keys(self.username).pause(3).perform()
                password_element = driver.find_element(By.XPATH,
                                                       '/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/div[3]/div/label/input')
                ActionChains(driver).click(password_element).send_keys(self.password).pause(3).perform()

                # 点击登录按钮，模拟鼠标点击
                # self.auto_click_picture()
                # 使用selenium直接点击
                driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/button').click()

                # 处理滑块验证
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/div/div[1]')))
                background_pic_url = driver.find_element(By.XPATH,
                                                         '/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]').get_attribute(
                    "src")
                if background_pic_url is None:
                    raise ValueError("未找到背景图片url")
                background_pic = requests.get(background_pic_url, timeout=5).content
                slider_pic_element = driver.find_element(By.XPATH,
                                                         '/html/body/div[6]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]')
                slider_pic_url = slider_pic_element.get_attribute("src")
                slider_pic = requests.get(slider_pic_url, timeout=5).content

                # 初始化图片路径
                self.save_path = os.path.join(self.config['path']['save_path'], f"pic_json_{int(time.time())}")
                # 创建保存目录
                os.makedirs(self.save_path, exist_ok=True)
                self.image_path = {
                    "background_picture": os.path.join(self.save_path, "background_pic.png"),
                    "slider_picture": os.path.join(self.save_path, "slider_pic.png"),
                    "output_with_box": os.path.join(self.save_path, "output_with_box.png")
                }

                # 保存图片
                with open(self.image_path['background_picture'], "wb") as f:
                    f.write(background_pic)
                with open(self.image_path['slider_picture'], "wb") as f:
                    f.write(slider_pic)

                # 预测滑块位置
                min_x, min_y, max_x, max_y, image = self.predict_slider()
                self.draw_box(image, [min_x, min_y, max_x, max_y])

                # 保存 JSON 数据
                json_data = {
                    "flags": {},
                    "shapes": [
                        {
                            "label": "gap",
                            "points": [
                                [float(min_x), float(min_y)],
                                [float(max_x), float(max_y)]
                            ],
                            "group_id": None,
                            "shape_type": "rectangle",
                            "flags": {}
                        }
                    ],
                    "imageHeight": 160,
                    "imageWidth": 320
                }
                with open(os.path.join(self.save_path, "json_data.json"), "w") as f:
                    json.dump(json_data, f)

                # print(f"目标 x 位置: {min_x * self.scale}")

                # move_distance = min_x * self.scale + 5  # 调整偏移，需要结合系统缩放
                # # 模拟鼠标滑动，仅限于可视化时有用，使用无头或者虚拟显示器时，需要直接使用selenium库
                # self.move(move_distance)
                # 使用selenium库，模拟滑动，会自动根据系统缩放进行调整实际的滑动距离
                slow_distance = self.move_speed(min_x + 10)
                slider = driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div[2]/div/div[2]/div[2]')
                # 使用 ActionChains 模拟滑动
                action = ActionChains(driver)
                action.click_and_hold(slider).perform()  # 按住滑块
                for dist in slow_distance:
                    # 水平移动，添加随机垂直偏移模拟人类行为
                    action.move_by_offset(dist, random.randint(-1, 1)).perform()
                    time.sleep(random.uniform(0.01, 0.1))  # 添加随机延迟
                action.release().perform()  # 释放滑块

                # 等待登录成功
                WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="Popover5-toggle"]')))
                success = True
                logger.info(f"第 {i + 1} 次尝试登录成功")
                return driver
            except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                logger.warning(f"第 {i + 1} 次尝试失败 - Selenium错误: {str(e)}")
            except RequestException as e:
                logger.warning(f"第 {i + 1} 次尝试失败 - 网络请求错误: {str(e)}")
            except (FileNotFoundError, ValueError) as e:
                logger.warning(f"第 {i + 1} 次尝试失败 - 文件或数据错误: {str(e)}")
            except Exception as e:
                logger.warning(f"第 {i + 1} 次尝试失败 - 未知错误: {str(e)}\n{traceback.format_exc()}")
            finally:
                if driver is not None and not success:
                    try:
                        driver.quit()
                    except WebDriverException as e:
                        logger.warning(f"关闭 WebDriver 失败: {str(e)}")
                        return driver
        logger.error("所有登录尝试均失败")
        return None

    def get_driver_headers(self, cookies):
        try:
            cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'referer': 'https://www.zhihu.com/explore',
                'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'cookie': cookie_string
            }
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            return cookie_dict, headers
        except Exception as e:
            logger.error(f"生成请求头失败: {str(e)}\n{traceback.format_exc()}")
            raise

    def main(self):
        """
        主方法，执行登录流程。
        返回获取到的cookies
        """
        driver = None
        try:
            driver = self.login()
            if driver is None:
                raise RuntimeError("所有登录尝试均失败，稍后重试或联系管理员查询日志")
            # print(f"登录成功，获取到的 cookies: {cookie_string}")
            logger.info(f"登录成功，获取到cookies!")
            # cookies = driver.get_cookies()
            logger.info(f"开始利用登录cookie获取其他cookie")
            driver.refresh()
            driver.get("https://www.zhihu.com/question/33889180/answer/1476766572")
            new_cookies = driver.get_cookies()
            time.sleep(2)
            logger.info(f"获取其他cookie完成")
            cookie_dict, headers = self.get_driver_headers(new_cookies)
            return new_cookies, headers
        except Exception as e:
            logger.warning(f"所有尝试均失败: {str(e)}\n{traceback.format_exc()}")
            raise
        finally:
            if driver is not None:
                try:
                    driver.quit()
                except WebDriverException as e:
                    logger.warning(f"关闭 WebDriver 失败: {str(e)}")

if __name__ == '__main__':
    try:
        config_path = r"E:\python\spider\project\zhihu\cnf\login.cnf"
        zhihu_login = ZhiHuLogin(config_path=config_path, scale=1.5)
        cookie, headers = zhihu_login.main()
        print(cookie,  headers)
    except Exception as e:
        print(e)