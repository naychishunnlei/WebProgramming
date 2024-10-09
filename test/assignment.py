from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, datetime
from typing import List
import json

app = FastAPI()

# Add CORS middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class Assignment(BaseModel):
    course: str
    title: str
    due_date: date
    description: str

# Sample data storage (replace with a database in a real app)
assignments = []

@app.get("/assignments", response_model=List[Assignment])
def get_assignments():
    return assignments

@app.post("/assignments", response_model=List[Assignment])
def add_assignment(assignments: List[Assignment]):
    for assignment in assignments:
        assignments.append(assignment)
    return assignments

class ClassTimetable(BaseModel):
    id: int
    course: str
    start_time: datetime
    end_time: datetime

JSON_FILE_PATH = 'timetable.json'

def read_timetable():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        write_timetable([])
        return []
    
def write_timetable(timetable):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(timetable, file, indent=4)

@app.get("/timetable", response_model=List[ClassTimetable])
def get_timetable():
    return read_timetable()

@app.post("/timetable", response_model=ClassTimetable)
def add_timetable_entry(entry: ClassTimetable):
    timetable = read_timetable()

    entry_id = len(timetable) + 1
    entry.id = entry_id

    timetable.append(entry.dict())
    write_timetable(timetable)

    return entry

@app.get("/")
def read_root():
    return {"message": "Welcome to the assignment and Timetable Page API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
