import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student
from typing import Tuple

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student) -> Tuple[str, int]:
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409
    if not student.first_name or not student.last_name:
        return 'invalid input', 405

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    try:
        student_id = int(student_id)
    except ValueError:
        return "invalid ID supplied", 400

    student = student_db.get(doc_id=student_id)
    if not student:
        return "not found", 404
    student = Student.from_dict(student)
    if not subject or subject in student.grades:
        # student was found, and, if requested, the grade was also found
        return student
    else:
        return "not found", 404


def delete_student(student_id):
    try:
        student_id = int(student_id)
    except ValueError:
        return "invalid ID supplied", 400

    student = student_db.get(doc_id=student_id)
    if not student:
        return "not found", 404
    student_db.remove(doc_ids=[student_id])
    return student_id


def get_student_by_last_name(last_name: str):
    last_name_query = Query()
    matches = student_db.search(last_name_query.last_name == last_name)
    if matches:
        # Arbitrarily return the first match in the list.
        # In real applications this is not acceptable however for now this will do.
        return matches[0]
    else:
        return "not found", 404
