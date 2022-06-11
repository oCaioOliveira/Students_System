from email.generator import Generator
from typing import Dict, List, Optional, Union
from fastapi import(
    Depends,
    FastAPI, 
    HTTPException,
    Response, 
    status
)
from sqlalchemy.orm import Session
from crud import(
    create_student, 
    remove_student,
    retrieve_all_students,
    retrieve_student_with_id,
    update_student,
)
from database import Base, SessionLocal, engine
from datatypes import StudentType, StudentListType
from datetime import datetime
import json
from schemas import(
    CreateStudentSchema,
    StudentSchema,
    UpdateStudentSchema,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

students = json.load(open("students.json", "r"))

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def welcome() -> str:
    return {"Welcome!"}


@app.get("/health/")
def alive() -> Dict[str, datetime]:
    return {"timestamp": datetime.now()}


@app.get("/students/", status_code=status.HTTP_200_OK,)
def get_all_students(db: Session = Depends(get_db)) -> Generator:
    if result := retrieve_all_students(db):
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Não existem estudantes cadastrados."
    )


@app.get("/students/{student_id}/", status_code=status.HTTP_200_OK,)
def get_student_with_id(student_id: int, db: Session = Depends(get_db)) -> StudentType:
    if result := retrieve_student_with_id(db, student_id):
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Estudante de 'id={student_id}' não encontrado."
    )


@app.delete("/students/{student_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)) -> None:
    if not remove_student(db, student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estudante de 'id={student_id}' não encontrado",
        )


@app.post("/students/", status_code=status.HTTP_201_CREATED,)
def post_student(student: CreateStudentSchema, db: Session = Depends(get_db),) -> StudentType:
    if result := create_student(db, student):
        return result
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.put("/students/{student_id}", status_code=status.HTTP_201_CREATED)
def put_student(student_id: int, student: UpdateStudentSchema, db: Session = Depends(get_db)) -> StudentType:
    if result := update_student(
        db, student_id, {
            key: value for key, value in student if value
        },
    ):
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Estudante de 'id={student_id}' não encontrado.",
    )