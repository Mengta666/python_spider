import json
import os
import requests
import re

from lxml import etree
from bs4 import BeautifulSoup



header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
}

# 获取视频与音频下载链接
def get_video_url(url):
    res = requests.get(url, headers=header)
    result = res.text
    info = (re.search(r"window.__playinfo__=(.*?)</script>", result, re.S)).group(1)
    info = json.loads(info)
    video_url = info["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = info["data"]["dash"]["audio"][0]["baseUrl"]

    result = etree.HTML(result)
    title = "".join(result.xpath('//*[@id="viewbox_report"]/div[1]/div/h1/@title'))

    return [video_url, audio_url], title



# 下载视频和音频并合并
def download_and_merge(url, title):
    if not os.path.exists(f"视频/B站/{title}"):
        os.makedirs(f"视频/B站/{title}")
    vedio = (requests.get(url[0], headers=header)).content
    audio = (requests.get(url[1], headers=header)).content

    with open(f"视频/B站/{title}/{title}_vedio.mp4", "wb") as f:
        f.write(vedio)
    with open(f"视频/B站/{title}/{title}_audio.mp4", "wb") as f:
        f.write(audio)

    path = f"E:/python/spider/learn/视频/B站/{title}/{title}"

    cmd = f"D:/ffmpeg-7.1.1-essentials_build/bin/ffmpeg -i {path}_vedio.mp4 -i {path}_audio.mp4 -c:v copy -c:a copy  -map 0:v:0 -map 1:a:0 {path}.mp4"
    os.system(cmd)
    print(f"{title}下载完成")
    os.remove(f"视频/B站/{title}/{title}_vedio.mp4")
    os.remove(f"视频/B站/{title}/{title}_audio.mp4")



def main(url):
    v_a_url, title = get_video_url(url)
    download_and_merge(v_a_url,  title)

if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV1VZL4zpE6C/?spm_id_from=333.1007.tianma.7-1-23.click"
    main(url)
