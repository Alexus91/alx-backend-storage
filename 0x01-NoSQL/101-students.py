#!/usr/bin/env python3
""" sorted by average score """


def top_students(mongo_collection):
    """
    Return all students sorted by average score."
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id", "name": {
            "$first": "$name"}, "averageScore": {
                "$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ]

    students = list(mongo_collection.aggregate(pipeline))
    return students
