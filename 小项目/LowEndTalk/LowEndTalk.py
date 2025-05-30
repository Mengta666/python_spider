import cloudscraper
import os
import json
import time
import pytz
import asyncio
import dotenv
import logging
from datetime import datetime
from random import uniform
from bs4 import BeautifulSoup
from telegram import Bot

# 加载环境变量
dotenv.load_dotenv("/opt/LowEndTalk/env/LowEndTalk.env")

# 加载环境变量
token = os.getenv("telegram_bot_token_lowtalkend")
chat_id = os.getenv("telegram_chat_id_lowtalkend")
# 设置日志
if not os.path.exists('/opt/LowEndTalk/log'):
    os.mkdir('/opt/LowEndTalk/log')
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s  [%(levelname)s]  %(filename)s:%(lineno)d  %(message)s',
                   filename='/opt/LowEndTalk/log/LowEndTalk.log',
                   filemode='w',
                   )
# 获取当前的日期转为iso8601标准时间，网站所用的标准时间是这个
str_time = datetime.now(pytz.UTC)
datetime_today_date = str_time.strftime('%Y-%m-%d')
vps_info_old = None
url_old = None
length = 0

# 先读取存储的文件
def read_file():
    global vps_info_old, url_old, length
    if os.path.exists(f'/opt/LowEndTalk/vps_info/vps_info_total.json') and os.path.getsize(f'/opt/LowEndTalk/vps_info/vps_info_total.json') > 0:
        with open(f'/opt/LowEndTalk/vps_info/vps_info_total.json', 'r', encoding='utf-8') as fp:
            vps_info_old = json.load(fp)
    # print(vps_info_old)
    # 清理数据，将不是今天的数据全部移除
    if vps_info_old is not None:
        vps_info_old = [item for item in vps_info_old if item['datatime'].split()[0] == datetime_today_date]
    # 获取所有已保存的链接，以便用来比较
    if vps_info_old is not None:
        url_old = [item['url'] for item in vps_info_old]
        length = len(url_old)


# 获取抓取的数据
def get_vps_info():
    global length
    vps_info_new = []
    for id in range(1, 3):
        url = f"https://lowendtalk.com/categories/offers/p{id}"

        time.sleep(uniform(1, 3))

        scraper = cloudscraper.create_scraper()
        response = (scraper.get(url)).text

        soup = BeautifulSoup(response, 'html.parser')
        vps_info = soup.find_all('div', class_='ItemContent Discussion')


        # 提取每一页的数据
        for i, vps in enumerate(vps_info):
            title = vps.a.text
            vps_url = vps.a.attrs['href']
            view_count = vps.find('span', class_='MItem MCount ViewCount').span['title']
            comment_count = vps.find('span', class_='MItem MCount CommentCount').span['title']
            datatime_rightnow = datetime.fromisoformat(vps.time.attrs['datetime']).strftime('%Y-%m-%d %H:%M:%S')
            str_datatime_rightnow = datatime_rightnow.split()[0]
            vps_json = {
                "id": length + i + 1,
                'title': title,
                'url': vps_url,
                'view_count': view_count,
                'comment_count': comment_count,
                'datatime': datatime_rightnow
            }
            if vps_info_old is None:
                if datetime_today_date == str_datatime_rightnow:
                    vps_info_new.append(vps_json)
            else:
                if vps_json['url'] not in url_old and datetime_today_date == str_datatime_rightnow:
                # 将单个json存入列表
                    vps_info_new.append(vps_json)
        time.sleep(uniform(1, 3))

    return vps_info_new

# 将新的数据发送给机器人
async def send_message(data):
    bot = Bot(token=token)
    message = (
        "新的vps咨询：\n\n"
        f"{data['title']}\n\n"
        f"URL:   {data['url']}\n\n"
        f"Views:    {data['view_count']}\n"
        f"Comments:    {data['comment_count']}\n"
        f"Time:    {data['datatime']}"
    )
    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        # print(f"已发送数据")
    except Exception as e:
        logging.error(f"{e}")

# 将新数据存入文件
def save_file(vps_info_new):
    if vps_info_old is not None:
        vps_info_total = vps_info_old + vps_info_new
    else:
        vps_info_total = vps_info_new
    with open(f'/opt/LowEndTalk/vps_info/vps_info_total.json', 'w', encoding='utf-8') as fp:
        if vps_info_total :
            json.dump(vps_info_total, fp=fp, ensure_ascii=False)
            logging.info(f"已将数据重新已保存数据到 vps_info_total.json 中")
        # else:
            # print(f'没有数据')

async def main():
    if not os.path.exists('/opt/LowEndTalk/vps_info'):
        os.mkdir('/opt/LowEndTalk/vps_info')
    # 读取存储的文件
    read_file()

    # 获取抓取的数据，并返回新的内容
    vps_info_new = get_vps_info()

    # 将数据通过机器人发送给客户端,异步
    if vps_info_new:
        task = []
        for data in vps_info_new:
            task.append(asyncio.create_task(send_message(data)))
        await asyncio.wait(task)
        logging.info(f"已发送数据")
    else:
        logging.info(f"没有数据")

    # 将新数据存入文件
    save_file(vps_info_new)



if __name__ == '__main__':
    asyncio.run(main())