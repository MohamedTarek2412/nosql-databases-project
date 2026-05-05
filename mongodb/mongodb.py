from pymongo import MongoClient
from pprint import pprint
import sys
import os

def connect():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    db = client["university_db"]
    print("Connected to MongoDB successfully!")
    return client, db

# PART 1 – TASK 1: Create 2 Collections + 3+ Documents Each
def task1_create_collections(db):
    print("\n" + "="*60)
    print("TASK 1: Creating Collections & Documents")
    print("="*60)

    # Drop if exists (clean run)
    db.students.drop()
    db.courses.drop()

    # Collection 1: students
    students = [
        {"_id": 1, "name": "Ahmed Hassan",   "age": 20, "major": "CS",   "gpa": 3.8},
        {"_id": 2, "name": "Sara Mohamed",   "age": 22, "major": "IT",   "gpa": 3.5},
        {"_id": 3, "name": "Omar Khaled",    "age": 21, "major": "CS",   "gpa": 3.2},
        {"_id": 4, "name": "Nour Ali",       "age": 23, "major": "Math", "gpa": 3.9},
        {"_id": 5, "name": "Youssef Tarek",  "age": 20, "major": "IT",   "gpa": 2.8},
    ]

    # Collection 2: courses
    courses = [
        {"_id": 1, "title": "Database Systems",   "credits": 3, "instructor": "Dr. Smith",   "dept": "CS"},
        {"_id": 2, "title": "Data Structures",    "credits": 3, "instructor": "Dr. Johnson",  "dept": "CS"},
        {"_id": 3, "title": "Machine Learning",   "credits": 4, "instructor": "Dr. Williams", "dept": "AI"},
        {"_id": 4, "title": "Web Development",    "credits": 3, "instructor": "Dr. Brown",    "dept": "IT"},
        {"_id": 5, "title": "Linear Algebra",     "credits": 3, "instructor": "Dr. Davis",    "dept": "Math"},
    ]

    db.students.insert_many(students)
    db.courses.insert_many(courses)

    print(f"Inserted {db.students.count_documents({})} students into 'students' collection")
    print(f"Inserted {db.courses.count_documents({})} courses into 'courses' collection")

# PART 1 – TASK 2: Delete at Least 1 Document from Each
def task2_delete_documents(db):
    print("\n" + "="*60)
    print("TASK 2: Deleting Documents")
    print("="*60)

    # Delete student with _id=5
    result1 = db.students.delete_one({"_id": 5})
    print(f"Deleted {result1.deleted_count} student (Youssef Tarek, _id=5) from 'students'")

    # Delete course with _id=5
    result2 = db.courses.delete_one({"_id": 5})
    print(f"Deleted {result2.deleted_count} course (Linear Algebra, _id=5) from 'courses'")

    print(f"   → Remaining students: {db.students.count_documents({})}")
    print(f"   → Remaining courses:  {db.courses.count_documents({})}")

# PART 1 – TASK 3: Update 2+ Documents — Add 'Score' Array
def task3_add_score_array(db):
    print("\n" + "="*60)
    print("TASK 3: Adding 'Score' Array to Documents")
    print("="*60)

    # Add Score array to ALL students
    db.students.update_many(
        {},
        {"$set": {"Score": [70, 80, 0, 0]}}
    )
    print("Added 'Score' array [70, 80, 0, 0] to all students")

    # Add Score array to ALL courses
    db.courses.update_many(
        {},
        {"$set": {"Score": [85, 90, 0, 0]}}
    )
    print("Added 'Score' array [85, 90, 0, 0] to all courses")

# PART 1 – TASK 4: Conditional Score Update
def task4_conditional_score_update(db):
    print("\n" + "="*60)
    print("TASK 4: Conditional Score Update")
    print("="*60)

    for collection_name in ["students", "courses"]:
        col = db[collection_name]
        docs = list(col.find({}))
        for doc in docs:
            if doc["_id"] == 1:
                col.update_one(
                    {"_id": 1},
                    {"$set": {"Score.2": 5}}   
                )
                print(f"[{collection_name}] _id=1 → Score[2] (3rd pos) = 5")
            else:
                col.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"Score.3": 6}}
                )
                print(f"[{collection_name}] _id={doc['_id']} → Score[3] (4th pos) = 6")

    # Show results
    print("\n Students after conditional update:")
    for s in db.students.find({}, {"name":1, "Score":1}):
        print(f"      {s['name']}: Score = {s['Score']}")

    print("\nCourses after conditional update:")
    for c in db.courses.find({}, {"title":1, "Score":1}):
        print(f"      {c['title']}: Score = {c['Score']}")

# PART 1 – TASK 5: Multiply Each Score Element by 20
def task5_multiply_scores(db):
    print("\n" + "="*60)
    print("TASK 5: Multiplying Each Score Element by 20")
    print("="*60)

    for collection_name in ["students", "courses"]:
        col = db[collection_name]
        docs = list(col.find({}))
        for doc in docs:
            new_scores = [x * 20 for x in doc["Score"]]
            col.update_one(
                {"_id": doc["_id"]},
                {"$set": {"Score": new_scores}}
            )

    print("ll Score elements multiplied by 20")
    print("\n Final Students Scores:")
    for s in db.students.find({}, {"name":1, "Score":1}):
        print(f"      {s['name']}: Score = {s['Score']}")

    print("\n Final Courses Scores:")
    for c in db.courses.find({}, {"title":1, "Score":1}):
        print(f"      {c['title']}: Score = {c['Score']}")

# PART 2 – One-to-Many Relationship
def part2_relationship(db):
    print("\n" + "="*60)
    print("PART 2 – TASK 1: One-to-Many Relationship")
    print("="*60)

    db.enrollments.drop()

    # One STUDENT → Many ENROLLMENTS (each referencing a course)
    enrollments = [
        {"_id": 1, "student_id": 1, "course_id": 1, "semester": "Fall 2024",   "grade": "A"},
        {"_id": 2, "student_id": 1, "course_id": 2, "semester": "Fall 2024",   "grade": "B+"},
        {"_id": 3, "student_id": 1, "course_id": 3, "semester": "Spring 2025", "grade": "A-"},
        {"_id": 4, "student_id": 2, "course_id": 1, "semester": "Fall 2024",   "grade": "B"},
        {"_id": 5, "student_id": 2, "course_id": 4, "semester": "Spring 2025", "grade": "A"},
        {"_id": 6, "student_id": 3, "course_id": 2, "semester": "Fall 2024",   "grade": "C+"},
        {"_id": 7, "student_id": 4, "course_id": 3, "semester": "Spring 2025", "grade": "A+"},
    ]

    db.enrollments.insert_many(enrollments)
    print(f"Created 'enrollments' collection with {len(enrollments)} documents")
    print("   Relationship: students (1) ──────< enrollments (Many)")
    print("   Relationship: courses  (1) ──────< enrollments (Many)")
    print()
    print("Enrollments:")
    for e in db.enrollments.find({}):
        print(f"      student_id={e['student_id']} → course_id={e['course_id']} | Grade: {e['grade']}")

# PART 2 – Aggregation Pipeline (printed as CMD reference)
def part2_aggregation_instructions():
    print("\n" + "="*60)
    print("PART 2 – TASK 2: Aggregation Pipeline (Run in Mongo Shell)")
    print("="*60)
    print("""
   Run this in mongosh or mongo CMD:

   use university_db

   db.enrollments.aggregate([
     {
       $lookup: {
         from: "students",
         localField: "student_id",
         foreignField: "_id",
         as: "student_info"
       }
     },
     {
       $lookup: {
         from: "courses",
         localField: "course_id",
         foreignField: "_id",
         as: "course_info"
       }
     },
     {
       $project: {
         _id: 0,
         semester: 1,
         grade: 1,
         "student_name": { $arrayElemAt: ["$student_info.name", 0] },
         "student_major": { $arrayElemAt: ["$student_info.major", 0] },
         "course_title":  { $arrayElemAt: ["$course_info.title", 0] },
         "course_credits":{ $arrayElemAt: ["$course_info.credits", 0] }
       }
     }
   ])
""")

# MAIN RUNNER
def main():
    try:
        client, db = connect()
        task1_create_collections(db)
        task2_delete_documents(db)
        task3_add_score_array(db)
        task4_conditional_score_update(db)
        task5_multiply_scores(db)
        part2_relationship(db)
        part2_aggregation_instructions()
        print("\n" + "="*60)
        print(" ALL MONGODB TASKS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        client.close()
    except Exception as e:
        print(f"\n Error: {e}")
        print("Make sure MongoDB is running: sudo systemctl start mongod")
        sys.exit(1)

if __name__ == "__main__":
    main()