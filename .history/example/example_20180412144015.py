from .main import MyRequest
from setttings import config
from bs4 import BeautifulSoup
import requests


config['headers'] = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


class ExampleRequest(MyRequest):
    def parse_html_link(self, html):
        body = BeautifulSoup(html, 'html5lib')
        links = set()
        for item in body.select('.ask-list-t2 .ques a'):
            links.add(item['href'])
        return links

    def parse_html_content(self, html, link):
        pass

    def run_link(self):
        start_url = 'https://ask.yuemei.com/'
        r = requests.get(start_url, headers=self.config['headers'])
        r.encoding = 'utf-8'
        body = BeautifulSoup(r.text, 'html5lib')
        page_link = []
        for item in body.select('.tab-nav-cont a'):
            page_link.append(item['href'])

        for link in page_link[:5]:
            # todo, 让 get_link 循环或递归起来
            self.get_link(link)
            print(link)


if __name__ == '__main__':
    example = ExampleRequest(config)
    example.run_link()


