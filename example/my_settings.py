
# 配置文件
config = {
    'mongodb_host': '192.168.1.148',
    'mongodb_port': 27017,
    'collection': 'example',
    'db': 'tzh_db',
    'unique': False,
    'headers': {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',

    },
    'proxy': False,
    'session': False,
    # proxy_pool 应该是一个数组或函数, 不断地获取代理ip, 返回值应该是一个有2个元素的列表或元组
    # 分别代表 http 代理和 https 代理
    'proxy_pool': [],
    'img_dir': './img',
    'max_retry': 5
}

