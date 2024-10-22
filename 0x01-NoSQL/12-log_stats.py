#!/usr/bin/env python3

"""
a Python script that provides some stats
about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    logs = collection.count_documents({})
    get_log = collection.count_documents({"method": "GET"})
    post_log = collection.count_documents({"method": "POST"})
    put_log = collection.count_documents({"method": "PUT"})
    patch_log = collection.count_documents({"method": "PATCH"})
    delete_log = collection.count_documents({"method": "DELETE"})
    get_status_log = collection.count_documents(
            {'$and': [{"method": "GET"}, {"path": "/status"}]}
        )

    print(f"{logs} logs")
    print("Methods:")
    print(f'\tmethod GET: {get_log}')
    print(f'\tmethod POST: {post_log}')
    print(f'\tmethod PUT: {put_log}')
    print(f'\tmethod PATCH: {patch_log}')
    print(f'\tmethod DELETE: {delete_log}')
    print(f"{get_status_log} status check")
