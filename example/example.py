import sys
sys.path.append('../')

from luke.main import MyRequest
# from luke.settings import config
from .my_settings import config
from bs4 import BeautifulSoup
import requests
import os
import pickle
import urllib.parse
import multiprocessing.dummy as multiprocessing


# 配置文件见 my_settings, 最好不要直接导入 luke.settings


class ExampleRequest(MyRequest):
    """
    必须继承 MyRequest, 实现必要的方法, 包括
    * parse_html_link
    * parse_html_content
    * run_link
    如果要使用代理, 必须在 config 中配置 proxy_pool
    """
    def parse_html_link(self, html, link):
        body = BeautifulSoup(html, 'html5lib')
        links = set()
        for item in body.select('.ask-list-t2 .ques a'):
            links.add(item['href'])
        # 或许这边要设置一个是否递归的标识
        next_link = None
        for item in body.select('.pageNav a'):
            if '下一页' in item.get_text(strip=True):
                next_link = urllib.parse.urljoin(link, item['href'])
                break
        print(link)
        return links, next_link

    def parse_html_content(self, html, link):
        pass

    def run_link(self):
        # 从起始页获得列表页的开始
        start_url = 'https://ask.yuemei.com/'
        r = requests.get(start_url, headers=self.config['headers'])
        r.encoding = 'utf-8'
        body = BeautifulSoup(r.text, 'html5lib')
        for item in body.select('.tab-nav-cont a'):
            self.page_links.add(item['href'])

        # 递归或循环列表页
        pool = multiprocessing.Pool(100)
        pool.map(self.get_link, self.page_links)


def run():
    """
    运行函数, 调用 run_link() 获取内容链接, 调用 run_content() 获取内容
    :return:
    """
    example = ExampleRequest(config)
    example.run_link()
    # example.run_content()


def load():
    """
    从文件中载入, 查看状态, 继续运行函数
    :return:
    """
    example: ExampleRequest = pickle.load(open('cls.pick', 'rb'))
    print(len(example.links))
    print(len(example.page_links))
    print(example.page_links)
    example.run_link()
    # example.run_content()


if __name__ == '__main__':
    # if os.path.exists('cls.pick'):
    #     load()
    # else:
    #     run()
    # run()
    load()


