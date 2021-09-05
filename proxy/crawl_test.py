import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq

ua = UserAgent(path='fake_useragent.json')
start_url = 'https://www.kuaidaili.com/free/inha/{}/'


def test():
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
            page_html = requests.get(page, headers=headers).text
            if page_html:
                page_doc = pq(page_html)
                trs = page_doc(".table-responsive table tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1) a').text()
                    port = tr.find('td:nth-child(2)').text()
                    return ':'.join([ip, port])
                time.sleep(1)

if __name__ == "__main__":
    print(test())
