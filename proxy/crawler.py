import time

import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent

ua = UserAgent(path="fake_useragent.json")

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('Get proxies successfully, ', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=10):
        start_url = 'http://www.66ip.cn/{}.html'
        headers = {
            "user-agent": ua.random
        }
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling ', url)
            html = requests.get(url, headers=headers).text
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])
                time.sleep(1)

    def crawl_kuaidaili(self, page_count=10):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        headers = {
            "user-agent": ua.random
        }
        for url in urls:
            print('Crawling ', url)
            html = requests.get(url, headers=headers).text
            if html:
                doc = pq(html)
                trs = doc('#list table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])
                time.sleep(1)

    def crawl_kxdali(self):
        start_url = "https://ip.ihuan.me/anonymity/2.html"
        headers = {
            "user-agent": ua.random
        }
        start_html = requests.get(start_url, headers=headers).text
        if start_html:
            doc = pq(start_html)
            a_list = doc('.pagination li:gt(0)').items()
            for a in a_list:
                page = start_url + a.find('a:first').attr('href')
                print('Crawling ', page)
                page_html = requests.get(page, headers=headers).text
                if page_html:
                    page_doc = pq(page_html)
                    trs = page_doc(".table-responsive table tr:gt(0)").items()
                    for tr in trs:
                        ip = tr.find('td:nth-child(1) a').text()
                        port = tr.find('td:nth-child(2)').text()
                        yield ':'.join([ip, port])
                    time.sleep(1)
