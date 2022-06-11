from typing import Dict, List, Optional, Union
from fastapi import FastAPI, HTTPException, status
from datetime import datetime
import json
from schemas import CreateStudentSchema, UpdateStudentSchema

app = FastAPI()

students = json.load(open("students.json", "r"))

@app.get("/")
def welcome() -> str:
    return {"Welcome!"}


@app.get("/health/")
def alive() -> Dict[str, datetime]:
    return {"timestamp": datetime.now()}


@app.get("/students/")
def get_all_students() -> List[Dict[str, Union[float, int, str]]]:
    if response := students:
        return response
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não existem estudantes cadastrados."
    )


@app.get("/students/{student_id}/")
def get_student_with_id(student_id: int) -> Dict[str, Union[float, int, str]]:
    try:
        if response := list(
            filter(lambda i: i.get("id") == student_id, students)
        )[0]:
            return response
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante de 'id={student_id}' não encontrado."
        )


@app.delete("/students/{student_id}/")
def delete_student(student_id: int) -> Dict[str, bool]:
    try:
        if response := list(
            filter(lambda i: i.get("id") == student_id, students)
        )[0]:
            del students[students.index(response)]
            return {"success": True}
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante de 'id={student_id}' não encontrado",
        )

    
def get_max() -> int:
    max_student = max(students, key=lambda i: i.get("id", 0))
    return max_student.get("id", 0)


@app.post("/students/")
def post_student(student: CreateStudentSchema) -> Dict[str, Union[float, int, str]]:
    students.append(
        new_student := {**{"id": get_max() + 1}, **student.dict()}
    )
    return new_student


def retrieve_student(student_id: int):
    try:
        if response := list(
            filter(lambda i: i.get("id") == student_id, students)
        )[0]:
            return response
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante de 'id={student_id}' não encontrado."
        )


@app.put("/students/{student_id}")
def put_student(student_id: int, student: UpdateStudentSchema) -> Dict[str, Union[float, int, str]]:
    if old_student := retrieve_student(student_id):
        updated_student = {
            **old_student,
            **{key: value for key, value in student if value},
        }
    students[students.index(old_student)] = updated_student
    return updated_student  