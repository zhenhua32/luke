from pymongo import MongoClient
import os.path

"""
保存数据相关, 使用mongodb作为数据库
"""


def get_mongodb(collection, db, host, port, unique=False):
    client = MongoClient(host, port)
    db = client[db]
    collection = db[collection]
    if unique:
        collection.create_index('hash', unique=True)
    return collection


def insert_data(collection, data):
    try:
        result = collection.insert_one(data)
    except Exception as e:
        return {'code': 1, 'error': e}
    return {'code': 0, 'result': result}


def save_file(dir_name, file_name, content):
    with open(os.path.join(dir_name, file_name), 'wb') as f:
        f.write(content)



