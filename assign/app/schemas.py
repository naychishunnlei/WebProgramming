from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class AssignmentBase(BaseModel):
    title: str
    course_id: int
    due_date: date
    score: int

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    course_id: int
    score: int

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    name: str

class Course(CourseBase):
    id: int
    assignments: List[Assignment] = []

    class Config:
        orm_mode = True
