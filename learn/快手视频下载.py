import random

import requests
import os
import time
import re

header = {
'content-type ':'application/json',
'Host':'www.kuaishou.com',
'Origin': 'https://www.kuaishou.com',
'Referer': 'https://www.kuaishou.com/search/video?searchKey=%E7%BE%8E%E5%A5%B3%E5%90%88%E9%9B%86',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
'content-type':'application/json',
'Cookie': 'kpf=PC_WEB; clientid=3; did=web_8ccfab7a4e511260099e0f0f91b4cb07; kpn=KUAISHOU_VISION'
}

# json文件，用json传入
parame = {"operationName":"visionSearchPhoto","variables":{"keyword":"美女合集","pcursor":"","page":"search"},"query":"fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n"}

# 获取视频链接
def get_video_url(url):
    response = requests.post(url, json=parame, headers=header)
    result = response.json()['data']['visionSearchPhoto']['feeds']
    url_info = []
    for feed in result:
        id = feed['author']['id']
        name = feed['author']['name']
        name_id = name +'_' + id
        url = feed['photo']['manifest']['adaptationSet'][0]['representation'][0]['url']
        url_info.append([url, name_id])
    return url_info

def download_video(url, title):
    # 判断是不是m3u8类视频
    if 'm3u8' in url:
        m3u8_done(url, title)
    else:
        res = requests.get(url)
        with open(f"视频/快手视频/{title}.mp4", "wb") as f:
            f.write(res.content)
            print(f"{title}下载完成")
def m3u8_done(url, title):
    res = requests.get(url)
    res = re.sub(r'#EX.*','', res.text).split()
    url_list = url.split("/")[:-1]
    header_url = "/".join(url_list)
    for url in res:
        real_url = header_url + "/" + url
        res = requests.get(real_url)
        with open(f"视频/快手视频/{title}.mp4", "ab") as f:
            f.write(res.content)

def main(url):
    if not os.path.exists("视频/快手视频/"):
        os.makedirs("视频/快手视频/")
    download_url = get_video_url(url)
    for url_info in download_url:
        time.sleep(random.uniform(1,3))
        download_video(url_info[0], url_info[1])


if  __name__ == '__main__':
    url = 'https://www.kuaishou.com/graphql'
    main(url)
