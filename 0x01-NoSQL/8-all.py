#!/usr/bin/env python3

"""
 a Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    collection = list(mongo_collection.find())
    if not collection:
        return []
    return collection
