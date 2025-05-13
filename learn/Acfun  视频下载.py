import lxml.etree
import requests
from lxml import etree
import re
import json
import os
from tqdm import tqdm



header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}


# 获取主连接，即m3u8的列表地址
def get_main_url(url):
    res = requests.get(url, headers=header)
    result = ((re.search(r" window.pageInfo = window.videoInfo = (.*?) window.videoResource", res.text, re.S)).group(1)).strip()[:-1]
    result = json.loads(result)
    result = json.loads(result["currentVideoInfo"]["ksPlayJson"])['adaptationSet'][0]["representation"][0]["url"]
    # print(result)

    res_lxml = lxml.etree.HTML(res.text)
    title = res_lxml.xpath("//title/text()")
    title = (re.match(r"(.*) -",title[0])).group(1)
    print(title)
    return result , title

# 获取每一个m3u8视频的连接列表
def get_m3u8_url(url):
    res = requests.get(url, headers=header)
    result = re.sub(r"#EX.*", "", res.text)
    result = result.split()
    return result


# 下载视频并合并
def download_and_merge(url, title):
    if not os.path.exists(f"视频/Acfun/{title}"):
        os.makedirs(f"视频/Acfun/{title}")
    with open(f"视频/Acfun/{title}/{title}.mp4", "ab") as f:
        for path in tqdm(url):
            real_path = "https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/" + path
            res = requests.get(real_path, headers=header)
            f.write(res.content)

def main(url):
    base_url , title = get_main_url(url)
    m3u8_list = get_m3u8_url(base_url)
    download_and_merge(m3u8_list, title)

if __name__ == '__main__':
    url = "https://www.acfun.cn/v/ac47253041"
    main(url)