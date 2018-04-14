import requests

"""
代理相关
"""


def get_session_with_proxy(http, https, headers=None, cookies=None):
    session = requests.session()
    session.proxies = {
        'http': http,
        'https': https
    }
    session.headers.update(headers)
    session.cookies.update(cookies)
    return session


def get_proxy(http, https):
    proxy = {
        'http': http,
        'https': https
    }
    return proxy


def get_session(headers=None, cookies=None):
    session = requests.session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    return session



