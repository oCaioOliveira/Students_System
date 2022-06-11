from typing import Any
from pydantic import BaseModel, validator
from enumerators import StatesBrEnum as StatesEnum
import re

POSTAL_CODE_REGEX = re.compile("[0-9]{5}\\-[0-9]{3}")

class StudentBaseSchema(BaseModel):
    name: str
    addres: str
    neighbour: str
    city: str
    postal_code: str

    @validator("postal_code")
    def validate_postal_code(cls, v: str, **kwargs: int) -> str:
        if not POSTAL_CODE_REGEX.match(postal_code := v.rjust(9, "0")):
            raise ValueError("O CEP informado não é válido!")
        return postal_code


class CreateStudentSchema(StudentBaseSchema):
    state: StatesEnum


class StudentSchema(StudentBaseSchema):
    id: int
    state: StatesEnum


class UpdateStudentSchema(StudentBaseSchema):
    name: str = ""
    addres: str = ""
    neighbour: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""

    @validator("state")
    def validate_state(cls, v: Any, **kwargs: int) -> str:
        try:
            return v if StatesEnum(v) else ""
        except ValueError:
            raise ValueError(f"O valor '{v}' não é válido!")