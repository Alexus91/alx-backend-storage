#!/usr/bin/env python3
""" function that returns the list of schools having a specific topic """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of schools having a specific topic
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
