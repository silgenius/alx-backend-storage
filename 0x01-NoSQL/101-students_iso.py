#!/usr/bin/env python3

"""
a Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    a Python function that returns all students sorted by average score
    """
    results = mongo_collection.find({})
    students = []
    for result in results:
        student = {}
        student_score = 0
        print(result)
        topics = result.get("topics")
        for score in topics:
            student_score += score.get("score") or 0
        avg_score = student_score / len(topics)
        student['name'] = result.get("name")
        student['_id'] = result.get("_id")
        student['averageScore'] = avg_score
        students.append(student)
    students = sorted(students, key=lambda x: x['averageScore'], reverse=True)

    return students
