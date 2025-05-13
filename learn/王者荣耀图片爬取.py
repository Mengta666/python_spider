import  requests
import lxml
import os
import fake_useragent
import re

from lxml import etree

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup



useragent = fake_useragent.UserAgent()
header = {
    'User-Agent': f'{useragent.random}'
}

def get_main_page(url):
    service = Service(r"E:\python\spider\selenium\chromedriver-win64\chromedriver.exe")
    options = Options()
    options.debugger_address="127.0.0.1:8888"

    bowser = webdriver.Chrome(service=service, options=options)
    bowser.get(url)
    hero_info_parent = bowser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div[2]/ul")
    hero_info_children = hero_info_parent.find_elements(By.XPATH,"./li")
    hero_list = []
    for hero_info in hero_info_children:
        heros = hero_info.find_element(By.XPATH,"./a")
        hero_url = heros.get_attribute("href")
        hero_list.append(hero_url)
    # print(hero_list)
    return hero_list

def get_hero_page(url):
    res = requests.get(url=url, headers=header)
    res.encoding = res.apparent_encoding
    result = lxml.etree.HTML(res.text)
    pic_name = result.xpath("//div[@class='pic-pf']//ul/@data-imgname")
    # print(pic_name)
    pic_name = re.sub("&[0-9]+", "", pic_name[0])
    # print(pic_name)
    pic_name = pic_name.split("|")                 # 所有皮肤的名字
    # print(pic_name)
    soup = BeautifulSoup(res.text, "html.parser")

    # 找到所有 <script> 标签
    script_tags = soup.find_all('script')

    # 遍历 <script> 标签，查找包含 cname 和 ename 的内容
    for script in script_tags:
        script_text = script.string  # 获取 <script> 标签的文本内容
        if script_text and 'cname' in script_text and 'ename' in script_text:
            # 使用正则表达式提取 cname(英雄名称) 和 ename(id) 的值
            hero_name = (re.search(r"var cname = '([^']*)'", script_text)).group(1)
            hero_id = (re.search(r"ename = '([^']*)'", script_text)).group(1)

    download_url = []
    for i in range(len(pic_name)):
        pic_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_id}/{hero_id}-bigskin-{i+1}.jpg"
        download_url.append(pic_url)
    # print(download_url, pic_name)
    return download_url, pic_name, hero_name



def download_img(down_url, pic_name, hero_name):
    if not os.path.exists(f"图片/王者荣耀/{hero_name}"):
        os.makedirs(f"图片/王者荣耀/{hero_name}")
    for i in range(len(pic_name)):
        res = requests.get(url=down_url[i], headers=header)
        with open(f"图片/王者荣耀/{hero_name}/{pic_name[i]}.jpg", "wb") as f:
            f.write(res.content)
            print(f"{pic_name[i]}.jpg下载完成")



def main():
    hero_list = get_main_page('https://pvp.qq.com/web201605/herolist.shtml')
    for hero_url in hero_list:
        download_url, pic_name, hero_name = get_hero_page(hero_url)
        download_img(download_url, pic_name, hero_name)


if __name__ == '__main__':

    main()