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

    print(f"Total logs: {total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {
        method: collection.count_documents({"method": method})
        for method in methods
    }

    print("Methods:")
    for method in methods:
        print(f"\t{method}: {method_counts[method]}")

    status_count = collection.count_documents({
        "method": "GET", "path": "/status"})
    print(f"GET /status: {status_count}")
