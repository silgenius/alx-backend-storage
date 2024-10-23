#!/usr/bin/env python3

"""
a Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    a Python function that returns all students sorted by average score
    """
    students = mongo_collection.find()
    
    result = []
    
    for student in students:
        # Calculate average score
        scores = [topic['score'] for topic in student.get('topics', [])]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Add to result with the average score
        student_data = {
            '_id': student['_id'],
            'name': student['name'],
            'averageScore': average_score
        }
        result.append(student_data)
    
    # Sort students by average score in descending order
    result.sort(key=lambda x: x['averageScore'], reverse=True)
    
    return result

