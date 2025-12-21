import scrapy
import requests
import pymongo

from scrapy.http import TextResponse
from scrapy_test.scrapy_test.items import QuotesItem

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     allowed_domains = ["quotes.toscrape.com"]
#     start_urls = ["https://quotes.toscrape.com"]
#
#     def parse(self, response):
#         # 返回的对象实际还是一个选择器列表，这个选择器仍可以使用 css/xpath 选择器进行筛选
#         quotes = response.xpath("//div[@class = 'quote']")
#         for quote in quotes:
#             # print(quote)
#             item = QuotesItem()
#             # <span class="text" itemprop="text">“A day without sunshine is like, you know, night.”</span>
#             # . 从当前路径进行搜索，全局路径只会匹配到第一个结果
#             item["text"] = quote.xpath(".//span[@class = 'text']/text()").get()
#             item["author"] = quote.xpath('.//small[@class="author"]/text()').get()
#             item["tags"] = quote.xpath('.//div[@class="tags"]/a//text()').getall()
#             print(item)
#
#             # yield item
#
#         # css选择器中的写法： 当前文档下的 pager
#         next_page = response.xpath('//ul[@class="pager"]//li[class="next"]/a/@href').get()
#         print(next_page)
#         # 拼接完整的 url
#         next_url = response.urljoin(next_page)
#         print(next_url)
#         # if next_page:
#         #     yield scrapy.Request(url = next_url, callback = self.parse)
#
# url = "https://quotes.toscrape.com"
# response = requests.get(url)
# # 将 response 转换为 scrapy 的 response 对象，使用这个对象可以对原本的代码进行完美调试
# response = TextResponse(url = url, body = response.text, encoding = "utf-8")
# queto = QuotesSpider()
# queto.parse(response)
# mymongo = pymongo.MongoClient("192.168.74.134:27018")
# try:
#     print(mymongo.list_database_names())
# except Exception as e:
#     print(e)
