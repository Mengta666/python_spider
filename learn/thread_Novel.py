import threading
import time
import requests
from lxml import etree
import re
from queue import Queue
import os


# 多线程下载小说

Lock = threading.Lock()
get_urls_done = False

def get_urls(index_url, header, queue):
    global get_urls_done
    res = requests.get(url=index_url, headers=header)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    chapter_url= html.xpath("//ul/li/a[@target = '_blank']/@href")
    for i in chapter_url:
        queue.put(i)
    get_urls_done = True

def downloads(header, queue, path):
    url = None
    try:
        while True :
            if queue.empty() and  get_urls_done:
                print('下载完成', time.ctime())
                break # 线程结束
            else:
                url = queue.get()
                res = requests.get(url=url, headers=header)
                res.encoding = res.apparent_encoding
                html = etree.HTML(res.text)
                content = html.xpath("//div[@class='txtnav']/text()")
                title = html.xpath("//div[@class='txtnav']/h1/text()")
                title = "".join(title)
                if title == '':
                    queue.put(url)
                    continue
                title = re.sub(r"[<|>|?|*|\"|:|/|\\]+", "", title)
                content = "".join(content)
                content = re.sub(r'\n', r'', content)
                content = re.sub(r'\u2003\u2003', r'\n', content)
                with open(path + '/' + title + '.txt', 'w', encoding='utf-8') as f :
                    f.write(content)
                    print(f"线程{threading.current_thread().name}下载：{title}...已经完成, 当前时间：{time.ctime()}")
    except Exception as e:
        print(e)
    finally:
        queue.put(url)

def get_info(url):
    res = requests.get(url=url, headers=header)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    content = html.xpath("//script/text()")
    content = "".join(content)
    name = re.search(r"articlename\s*:\s*'(.*?)'", content, re.S)
    author = re.search(r"author\s*:\s*'(.*?)'", content, re.S)
    name = re.sub(r'articlename:', '', name.group())
    author = re.sub(r'author:', '', author.group())
    return [name, author]

if __name__ == '__main__':
    url = "https://www.69shuba.com/book/30289/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    }

    info = get_info(url)
    path = r"E:/python/spider/learn/小说/" + info[0] + " - " + info[1]
    if not os.path.exists(path):
        os.mkdir(path)

    q = Queue(20000)
    Th1 = threading.Thread(target=get_urls, args=(url, header, q,))
    Th1.start()
    t_downloads = []
    for i in range(5):
        t_downloads.append(threading.Thread(target=downloads, args=(header,q,path,)))
    for i in t_downloads:
        i.start()
    for i in t_downloads:
        i.join()
    Th1.join()


