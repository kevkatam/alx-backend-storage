#!/usr/bin/env python3
"""
module containing script that provides some stats about Nginx logs stored
in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    get = collection.count_documents({'method': 'GET'})
    post = collection.count_documents({'method': 'POST'})
    put = collection.count_documents({'method': 'PUT'})
    patch = collection.count_documents({'method': 'patch'})
    delete = collection.count_documents({'method': 'DELETE'})
    status = collection.count_documents({
        'method': 'GET',
        'path': '/status'
        })

    print(f"{total_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{status} status check")
