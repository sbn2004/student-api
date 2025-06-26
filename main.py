from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

app = FastAPI()

class Student(BaseModel):
    id: int
    FirstName: str
    LastName: str
    MiddleName: Optional[str]
    Age: int
    City: str

class ClassInfo(BaseModel):
    id: int
    ClassName: str
    Description: str
    StartDate: date
    EndDate: date
    Hours: int

students = {}
classes = {}
registrations = {}

@app.post("/students/")
def add_student(student: Student):
    students[student.id] = student
    return {"message": "Student added."}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student
    return {"message": "Student updated."}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id in students:
        del students[student_id]
        return {"message": "Student deleted."}
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/classes/")
def create_class(classinfo: ClassInfo):
    classes[classinfo.id] = classinfo
    return {"message": "Class created."}

@app.put("/classes/{class_id}")
def update_class(class_id: int, classinfo: ClassInfo):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    classes[class_id] = classinfo
    return {"message": "Class updated."}

@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    if class_id in classes:
        del classes[class_id]
        return {"message": "Class deleted."}
    raise HTTPException(status_code=404, detail="Class not found")

@app.post("/register/")
def register(student_id: int, class_id: int):
    if class_id not in registrations:
        registrations[class_id] = []
    registrations[class_id].append(student_id)
    return {"message": "Student registered to class."}

@app.get("/classes/{class_id}/students")
def get_students_in_class(class_id: int):
    student_ids = registrations.get(class_id, [])
    return [students[sid] for sid in student_ids if sid in students]