import scrapy

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/topics']

    # 获取主题链接
    def parse(self, response):
        response.xpath("/html/body/div[3]/div[1]/div/div/ul")
        print(response.text)


