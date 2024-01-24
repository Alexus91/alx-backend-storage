#!/usr/bin/env python3
"""Module utility function that insert documents
"""


def insert_school(mongo_collection, **kwargs):
    """Function that inserts a new document in a collection """
    rlt = mongo_collection.insert_one(kwargs)
    return rlt.inserted_id
