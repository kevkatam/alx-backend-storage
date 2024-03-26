#!/usr/bin/env python3
"""
module that lists all documents in a collection
"""


def list_all(mongo_collection):
    """ function that lists all documents in a collection """
    for doc in mongo_collection.find():
        return doc
    return []
