from typing import Dict, List, Optional, Union
from fastapi import FastAPI, HTTPException, status
import json

app = FastAPI()

students = json.load(open("students.json", "r"))

@app.get("/")
def welcome() -> str:
    return {"Welcome!"}


@app.get("/health/")
def alive() -> str:
    return {"HEALTH"}


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