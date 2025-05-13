import asyncio
import time

import os
import aiohttp

from lxml import etree
from bs4 import BeautifulSoup
from aiofile import AIOFile

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    'Referer': 'https://www.bizhihui.com/tags/2Kbizhi/'
}

async def get_total_picture_url(url, classify_url, semaphore):   # 获取分类下的所有图片链接
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()
                result = etree.HTML(text)
                res = result.xpath("//li[@class='item-list masonry-brick']//a[@class='item-img']//@href")
                classify = result.xpath(f"//div[@class='container p-top']//div[@class='siftMore clear']/a[@href='{classify_url}']/text()")

                classify = "".join(classify)

                if classify:
                    if not os.path.exists(f"E:/python/spider/learn/图片/{classify}"):
                        os.mkdir(f"E:/python/spider/learn/图片/{classify}")
                else:
                    classify = "未分类"
                    if not os.path.exists(f"E:/python/spider/learn/图片/{classify}"):
                        os.mkdir(f"E:/python/spider/learn/图片/{classify}")
                path = f"E:/python/spider/learn/图片/{classify}"
                return res, path


async def get_picture_url(url,  semaphore):    #获取要下载的图片原图链接
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()
                result = etree.HTML(text)
                res = result.xpath("//div[@class='shadow-list']//a//@href")  # 原图下载链接
                soup = BeautifulSoup(text, 'lxml')  # 使用BeautifulSoup解析lxml中的部分标签
                title = soup.find('h1').text
                return res[2], title

async def download_picture(url, path, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url[0], headers=headers) as response:
                img = await response.content.read()
                title = url[1].replace(' ', '_')
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                async with AIOFile(f"{path}/{title}-{timestamp}.jpg", 'wb') as f:
                    await f.write(img)
                    print(f"{url[0]}_{time.ctime()}下载完成")



async def main(classify_url):
    # 设置并发量
    semaphore = asyncio.Semaphore(5)
    # 获取分类下指定页面的图片链接任务
    main_url = classify_url
    task_picture_url = []
    for i in range(5, 10):
        url = main_url + f"{i}"
        task_picture_url.append(asyncio.create_task(get_total_picture_url(url, classify_url, semaphore)))
    dones,pending = await asyncio.wait(task_picture_url)
    picture_url = []
    path_dir = []
    for done in dones:
        res, path = done.result()
        for i in res:
            picture_url.append(i)
            path_dir.append(path)

    # 获取每个图片原图链接任务
    task_download_picture_url = []
    for i in picture_url:
        task_download_picture_url.append(asyncio.create_task(get_picture_url(i, semaphore)))
    done,pending = await asyncio.wait(task_download_picture_url)
    picture_real_url = []
    for done in done:
        res,title = done.result()
        picture_real_url.append([res,title])

    # 下载任务
    task_download_picture = []
    for i in range(len(picture_real_url)):
        task_download_picture.append(asyncio.create_task(download_picture(picture_real_url[i],  path_dir[i], semaphore)))
    await asyncio.wait(task_download_picture)
    print("所有图片下载完成，已退出")


if __name__ == '__main__':
    urls = [
        "https://www.bizhihui.com/renwu/",
        "https://www.bizhihui.com/fengjing/",
        "https://www.bizhihui.com/youxi/",
        "https://www.bizhihui.com/tuijian/"
    ]
    for classify_url in urls:
        asyncio.run(main(classify_url))
        print(f"类：{classify_url} 下载完成")