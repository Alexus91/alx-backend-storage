#!/usr/bin/env python3
"""
 that list all document
"""
import pymongo


def list_all(mongo_collection):
    """
    list all collections
    """
    documents = list(mongo_collection.find({}))
    return documents
