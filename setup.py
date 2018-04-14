from distutils.core import setup

setup(
    name='luke',
    version='1.0',
    description='simple Web Crawler',
    author='tzh',
    author_email='2375626546@qq.com',
    license='MIT',
    packages=['luke'],
    requires=['requests', 'pymongo']
)
