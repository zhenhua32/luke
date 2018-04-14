from . import db
from . import proxy

import multiprocessing.dummy as multiprocessing
from abc import ABC, abstractmethod
import requests
import atexit
import pickle
import random
import time
import os
import sys
# 修改递归深度, 递归挺占内存的, 不容易维护
sys.setrecursionlimit(10000)


class MyRequest(ABC):
    # todo, 应该有个保存状态的方法, 断点续传
    # todo, 使用session
    # todo, 最大的问题还是在于中断之后如何处理, 尽可能简单的恢复到上次运行的状态
    # todo, 必须解决一个问题, 在获取列表链接时不能中断
    def __init__(self, config):
        """
        config: 配置文件, 从 settings 中继承修改
        links: 内容链接, 可以是普通网页链接或图片链接
        links_done: 已完成的内容链接
        page_links: 列表链接, 适于用递归
        collection: 数据库
        state: 保存必要的状态, 以便在 pickle 的时候恢复, 用户自定义如何使用
        :param config:
        """
        self.config: dict = config
        self.links = set()
        self.links_done = set()
        self.page_links = set()
        self.collection = db.get_mongodb(
            collection=self.config['collection'],
            db=self.config['db'],
            host=self.config['mongodb_host'],
            port=self.config['mongodb_port'],
            unique=self.config['unique']
        )
        # 将要保存的内容放在这里, 以便 pickle 的时候能保存, 用户自定义的
        self.state = {
            'retry': 0
        }
        atexit.register(self.__save_class)

    def __getstate__(self):
        """
        pickle 时保存状态
        :return:
        """
        return {
            'links': self.links,
            'links_done': self.links_done,
            'page_links': self.page_links,
            'config': self.config,
            'state': self.state
        }

    def __setstate__(self, state):
        """
        pickle 时载入状态
        :param state:
        :return:
        """
        self.config = state['config']
        self.links = state['links']
        self.links_done = state['links_done']
        self.page_links = state['page_links']
        self.collection = db.get_mongodb(
            collection=self.config['collection'],
            db=self.config['db'],
            host=self.config['mongodb_host'],
            port=self.config['mongodb_port'],
            unique=self.config['unique']
        )
        self.state = state['state']
        atexit.register(self.__save_class)

    def __save_class(self):
        pickle.dump(self, open('cls.pick', 'wb'))

    def get_proxy(self):
        if type(self.config['proxy_pool']) == list:
            ip = random.choice(self.config['proxy_pool'])
        elif type(self.config['proxy_pool']) == function:
            ip = self.config['proxy_pool']()
        else:
            raise Exception('self.config["proxy_pool"]应该是一个数组或函数')

        assert (len(ip) == 2)
        return proxy.get_proxy(*ip)

    def get_request(self, link):
        try:
            if self.config['proxy']:
                proxies = self.get_proxy()
                r = requests.get(link, headers=self.config['headers'], proxies=proxies)
            else:
                r = requests.get(link, headers=self.config['headers'])
            self.state['retry'] = 0
        except Exception:
            if self.state['retry'] < self.config['max_retry']:
                self.state['retry'] += 1
                time.sleep(random.uniform(1, 5))
                return self.get_request(link)
            else:
                msg = '重试次数超出了{}次, 在config["max_retry"]中修改最大重试次数'
                raise Exception(msg.format(self.config["max_retry"]))
        return r

    @abstractmethod
    def parse_html_link(self, html, link):
        """
        解析网页, 得到内容页面的链接, 应该返回链接的数组
        应该返回 (links, next_link) 的形式
        :param html: 网页的html内容, 为utf-8文本
        :param link: 网页的链接
        :return: (links, next_link) 应该返回解析好的内容链接set和下一页的链接
        """
        raise NotImplementedError

    @abstractmethod
    def parse_html_content(self, html, link):
        """
        解析网页, 从内容页面提取所需要的数据, 应该返回一个字典, 符合bson格式
        如果__init__初始化的时候self.config['unique']为True, 那么字典中应该包含hash,
        hash的值应该能唯一标识网页, 最常见的做法是将hash设置为link
        应该返回 data:dict
        :param html: 网页的html内容, 为utf-8文本
        :param link: 网页的链接
        :return:
        """
        raise NotImplemented

    def get_link(self, link):
        r = self.get_request(link)
        r.encoding = 'utf-8'
        links, next_link = self.parse_html_link(r.text, link)
        self.links |= set(links)
        if next_link:
            self.page_links.remove(link)
            self.page_links.add(next_link)
            # todo, 递归不好控制, 无法恢复, 加上容易超出递归深度
            self.get_link(next_link)

    def get_content(self, link):
        r = self.get_request(link)
        r.encoding = 'utf-8'
        data = self.parse_html_content(r.text, link)
        db.insert_data(self.collection, data)
        self.links_done.add(link)
        print(len(self.links_done), len(self.links))

    def get_img(self, link):
        r = self.get_request(link)
        img_name = link.split('/')[-1]
        img_path = os.path.join(self.config['img_dir'], img_name)
        with open(img_path, 'wb') as f:
            f.write(r.content)

    @abstractmethod
    def run_link(self):
        """
        这里应该实现一个循环或递归, 持续获取从列表页面获取内容链接
        最好是能保存状态
        :return:
        """
        raise NotImplementedError

    def run_content(self):
        links = list(self.links - self.links_done)
        if len(links) == 0:
            print('所有的links都已经下载完成')
        else:
            pool = multiprocessing.Pool(10)
            pool.map(self.get_content, links)

    def run_img(self):
        links = list(self.links - self.links_done)
        if len(links) == 0:
            print('所有的links都已经下载完成')
        else:
            pool = multiprocessing.Pool(10)
            pool.map(self.get_img, links)


