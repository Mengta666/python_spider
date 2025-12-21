import requests
from project.zhihu.Scheduler_task.task_log import logger

from project.zhihu.zhihu_login.login import ZhiHuLogin

class CheckCookies:

    @staticmethod
    def check_cookies_zhihu(zhihu_headers):
        # login = ZhiHuLogin(username=18026853660, password='密码')
        # zhihu_cookies, zhihu_headers = login.main()
        url = "https://www.zhihu.com/topic/19550517/top-answers"
        response = requests.get(url, headers=zhihu_headers)
        print(response.status_code)
        if response.status_code == 200:
            return True
        else:
            logger.warning("Cookies失效, 开始获取新的cookies")
            return False

if __name__ == '__main__':
    headers =  {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            # "cookie": "BEC=04f80badde0b95441251f0ed57775ff7; captcha_ticket_v2=2|1:0|10:1756635274|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfbVFqSypaRWFwb1JXamw2OUNlS2Y4Z0xzMFFIeVE4akNnOXlaXzF5KkJneTVUUDYxOUNwczNObXBuT0tlYnB2cjFOOXJobEZSYkxCdzZiQ2dPd1kqUGRaYmoqeloqM3lvMm5EUkNuc3R1aS4ucDlzWXRvNl9vUUQyR2U2Z1l4KllhblZ5REx4TmZnUjR0Ni5aMkw4bXNnLm1Jak81d0lraklnZ0ExeGpWc3VXRjllKmZnWmguZWJYMDhJemxMYUtXRCpVbWVKX2hXdVdwVERnRmVvZFRJSTFxWDNDbzNMRWhxUXhBaWs4VjNOSkJ3bk5aanUqT2xmaFBoRmlrSEVDZUV5VXp5OGpRZ3diRDM1NV9wR0NmeURxSlhLTWFibWh5WEpWTWxCU3U2aEtkUWRXX0Q4dUlPZzZlRzQyekFKVG5KeUJFVypRLnA0cGJaR09rQlR1Sm1oTkxYKllfSDM5QXZmNFluT29HR2wxalhiZVNEMi5Xb1EqNU5NZVZTTlM2elRCZTRubUgqNGd6UTZYZGZhYXd3cEkwNGJjOFcwQUN1cjEuaUFkd25DUW1ERGp4ejZPTlNwTDQuemwuNGtvQTI4OU1pNG1ZSENZZjhqMlhIRWpueTBRV0dRbzQqMk1lKmFIS1Y1VVpuaHpiVHJrZDRoQi5kTVFYb3EqSzlBX1d0WXFJUk03N192X2lfMSJ9|9ce43962314a50ff755a328a5be7fc587ce531e5dbe8eef168e5564dba8e51f9; gdxidpyhxdE=7KfRYiSW6vyUe9NpDKtPZfgRfkV8W7Q7QPZjwDARyZUPygPPRm5XazrA0KXTrVCD1LS3SJ0BAtYuy12dYIU7Up1dPHJcj8VB%5CZa1Q4zNxLcGWypPotxsYGrE8Ccycswy8rsBgRXem07dWzXx0fs%2B4VrB8pJbEP22%2BNR%5CqOdrPSAenW0A%3A1756636180553; crystal=U2FsdGVkX19laZ2vM2U5E2dLGtDEHlxO5egcnqkn8ZXVJZKd0Ozer6BH/O4Wde3UJyL9hCylGJPfaDU5KkAetwKbmsFEOl2kuxEPZhntyZoYPvijnmc/zcU4XBZG4mmUFaf2cKjuZ8w2cnYZibq8pz/Pp49RMditXzeizKpcew7rmDmffjaB9d6gWGG4XuJKWifd7hLAaM7g2q9oEMpBi1GKVGJG58Jqkhq1QK+2CUFnyedu/60lzOM7X5ZKmjA4; z_c0=2|1:0|10:1756635274|4:z_c0|92:Mi4xQmRvYVpRQUFBQUNrNXRPRVhQdl9HaVlBQUFCZ0FsVk5pbTZoYVFCSGdEYVhNd1BWSXQxWlk2Wm1pQ0g5dGF2Z01n|6d5a21302643e08a8b7bd03d4025f9c8a9c2f1f026fae52fd903190dec2090d4; vmce9xdq=U2FsdGVkX19BCnbBxcYpBt9SiJTQIdES+dsBa/HXzxueYsBSNl0KPfiQT7ahwTGemWBeEwezkgj8OM45pW3SPE/Zv8KPd6v/8cmGw2sa9KipQfxF41a9Oz4kC4YDglOxMD9a5pdCQtmjG2bG1+9Q57dk7yVdgqsY/hy8U/FObqQ=; assva5=U2FsdGVkX1+3OqTjovq4nYcx2DUqqovstN2gL8HQ8RwtTRI2Q6YC6KBevkYpfCwIsSKzno6rIRe2pWADTlS0bA==; pmck9xge=U2FsdGVkX19ZFkaRuAoSpc5BTXcsQ+1bvehvmvxtsYo=; cmci9xde=U2FsdGVkX19Mai9lRuwioX7j4KEQYyUfPAB/ah51i2yi1W2JHTeiyTQuOVcH64kIYO48KTW/CyHP5MmXB70xrA==; DATE=1756635279517; __snaker__id=fBhZ8UKLhhj5JR0r; captcha_session_v2=2|1:0|10:1756635254|18:captcha_session_v2|88:Q3cxbms0NkxVeEVrK2o5R24xaVptaUhrekRmRW1UeDdqQjVPUC9SZ25rd2p6S0JINVJnemJtQ0hRTVdwYzFBQw==|66edf3188dfe066f4c7403bf8f390fcc52009edd99be3f229223a0ffcfabe6f6; osd=UVoXBEivYEDic9qGBU_EkmUsJXge6RgNpSPp_2bWECyoAZfVa9hF9Y5y24MEzZDbvOa8vCQ1_3GjvlsPnTz8Mdk=; SESSIONID=GxHCP2yfyqlOvMRnQfRhLttnvRHKttpEgEYW1VwmZsm; __zse_ck=004_EhLl4S3qF6z51sw2cfo4R61QVJ0soTWQrc=WFhgF1K11N59p0knFvAKM17D4R=/A0fvx8phauOESNPhgYFu45/8RJE6nBASLsCA5LP89c0OL3fdciAqAs8V7gmAufE4P-QT3F6QdheYe1XMiJGNdrpcx57VaPon6AG8cuRBMglKh925eUKZkCcZGHb4u4eQjobqDTS3auWH1Ec+wXeytJdHVBUNXet6FzrIkKENtXdyKtW9GC9NCGCNcbttgTQeQFbblWXQJ+XGL2Jm1xnIvBni5W/MhxKc31/gkzqq39PsE=; assva6=U2FsdGVkX1+u8slWr0CLfzt8mB4NmcgdVF9A0XsiZRw=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1756635279; HMACCOUNT=A25477FB7D1B49C6; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1756635303; _zap=ad280959-413e-4507-bb66-17ddb395f452; d_c0=pObThFz7_xqPTl5LDCaZa2lw2oWpgZLUpoU=|1756635251; JOID=VVEcBk2ra0vgdt6NDk3Blm4nJ30a4hMPoCfi9GTTFCejA5LRYNNH8Ip50IEByZvQvuO4ty83-nWotVkKmTf3M9w=; _xsrf=3750ed84-e71c-4f66-bcfe-b72c7066460c",
            "priority": "u=0, i",
            "referer": "https://www.zhihu.com/explore",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    status = CheckCookies.check_cookies_zhihu(headers)
    print(status)
