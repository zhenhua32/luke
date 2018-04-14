# 爬虫框架 luke

尝试封装常见的操作

## 文件说明
* main.py: 主文件
* db.py: 封装数据库操作
* proxy.py: 代理
* settings.py: 设置

## 设计原则
* Not
  * 不解析页面, 如何获取需要的内容和本框架无关
  * 不维护代理池, 只暴露了一个获取代理ip的接口, 必须自建代理池
  * 不维护列表链接, 内部只有内容链接, 必须处理如何获取列表链接并在必要时保存状态
  * 不使用异步请求, 只有一个简单的多线程请求
* Assert 
  * 数据库使用 mongodb
  * 请求使用 requests
  * 保存文件直接写入目录
  * 使用配置文件
* Must
  * 你必须实现, 解析列表页面 parse_html_link
  * 你必须实现, 解析内容页面 parse_html_content
  * 你必须实现, 运行列表页面 run_link
  * 你必须实现, 扩展 luke.settings.config, 自定义配置


## 配置文件示例
```python
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
```

## 示例
参考 example 目录


=======
# luke
simple web crawler
>>>>>>> fa7694eecd3c68d18c7c9b27708268eaae8eea43
