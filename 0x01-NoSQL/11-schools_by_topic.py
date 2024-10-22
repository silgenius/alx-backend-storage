#!/usr/bin/env python3

"""
a Python function that returns the
list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    result = mongo_collection.find({"topics": topic})
    return result
