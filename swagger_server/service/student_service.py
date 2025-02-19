import os
import tempfile
from functools import reduce
from pymongo import MongoClient
from bson import ObjectId

# from tinydb import TinyDB, Query
#
# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

client =  MongoClient('mongo', 27017)
db = client["students_db"]
students_collection = db["students"]


def add(student=None):
    query = {"first_name": student.first_name, "last_name": student.last_name}
    res = students_collection.find_one(query)
    if res:
        return 'already exists', 409

    doc_id = students_collection.insert_one(student.to_dict())
    return str(doc_id.inserted_id)


def get_by_id(student_id=None, subject=None):

    query = {"_id": ObjectId(student_id)}
    student = students_collection.find_one(query)

    if not student:
        return 'not found', 404

    student["_id"] = str(student["_id"])

    return student


def delete(student_id=None):
    query = {"_id" : ObjectId(student_id)}
    result = students_collection.delete_one(query)
    if result.deleted_count == 0:
        return "not found", 404
    return student_id