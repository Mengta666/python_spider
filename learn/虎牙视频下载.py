# 配置参数虎牙视频有参数，需要注意添加
# 头为：https://liveapi.huya.com/moment/getMomentContent
import json
import random

import requests
import re
import os
import time

from lxml import etree


header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}


# 在目录页获取每一个视频的视频id
def get_video_id(url):
    res = requests.get(url, headers=header)
    result = etree.HTML(res.text)
    video_id = result.xpath("//div[@id='root']//section[@class='mod-wrap']//ul[@class='vhy-video-list clearfix ']/li//@data-vid")
    return video_id


# 获取视频
def get_video(video_id):
    url = "https://liveapi.huya.com/moment/getMomentContent"
    params = {
        "videoId": f"{video_id}",
        "uid": "",
        "_": "1747121178998"
    }

    res = requests.get(url, headers=header, params=params)
    info = json.loads(res.text)
    title = info["data"]["moment"]["title"]
    video_url = info["data"]["moment"]["videoInfo"]["definitions"][0]["url"]

    return (video_url, title)

# 下载视频
def download_video(url, title):
    title = re.sub(r"[\\/:*?\"<>|]", "", title)
    res = requests.get(url, headers=header)
    with open(f"视频/虎牙视频/{title}.mp4", "wb") as f:
        f.write(res.content)
        print(f"{title}下载完成")

def main(url):
    if not os.path.exists(f"视频/虎牙视频"):
        os.makedirs(f"视频/虎牙视频")
    video_id_list = get_video_id(url)

    video_url_list = []
    for id in video_id_list:
        video_url_list.append(get_video(id))
    for url_title in video_url_list:
        time.sleep(random.uniform(1, 2))
        download_video(url_title[0], url_title[1])

if __name__ == '__main__':
    url = "https://www.huya.com/video/g/Dance"
    main(url)



