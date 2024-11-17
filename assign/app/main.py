from fastapi import FastAPI, Depends, HTTPException, Request, Form, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import date, datetime

import app.database as database
import app.crud as crud
import app.models as models
import app.schemas as schemas

app = FastAPI()

# Mount the static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    models.Base.metadata.create_all(bind=database.engine)

def add_sample_data(db: Session):
    # Define courses and assignments
    courses_data = [
        {"name": "Software Engineering 101"},
        {"name": "Data Structures"},
        {"name": "Database Management"},
    ]
    
    assignments_data = [
        {
            'title': 'Assignment 1',
            'due_date': date(2024, 11, 18),
            'course_id' : 1,
            'score' : 0,
        },
        {
            'title': 'Assignment 2',
            'due_date': date(2024, 11, 20),
            'course_id' : 2,
            'score' : 0,
        },
        {
            'title': 'Assignment 3',
            'due_date': date(2024, 11, 22),
            'course_id' : 3,
            'score' : 0,            
        }
    ]

    # Add courses to the database
    courses = {}
    for course_data in courses_data:
        course = models.Course(name=course_data["name"])  # Use models.Course here
        db.add(course)
        courses[course.name] = course  # Save the course instance to reference later
    
    db.commit()  # Commit after adding courses
    
    # Add assignments to the database
    for assignment in assignments_data:
        db.add(models.Assignment(**assignment))  # Use course_id directly
    db.commit()

# Route to create tables (if they don't already exist)
@app.on_event("startup")
def on_startup():
    init_db()
    db = database.SessionLocal()
    add_sample_data(db)
    db.close()

# users_db = {
#     "1001": {"role": "lecturer"},
#     "9001": {"role": "student"},
# }

# @app.get("/", response_class=HTMLResponse)
# async def login_page(request: Request):
    
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/login")
# async def login(request: Request, id: str = Form(...)):
    
#     user = users_db.get(id)
#     if user:
#         role = user["role"]
#         if role == "lecturer":
#             return RedirectResponse(f"/teacher/{id}", status_code=302)
#         elif role == "student":
#             return RedirectResponse(f"/student/{id}", status_code=302)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid ID")
    
# @app.get("/teacher/{user_id}", response_class=HTMLResponse)
# async def teacher_page(request: Request, user_id: str):
   
#     user = users_db.get(user_id)
#     if user and user["role"] == "lecturer":
#         return templates.TemplateResponse("teacher.html", {"request": request, "user_id": user_id, "assignments_by_course": assignments_by_course, "active_page" : "list"})
#     else:
#         return RedirectResponse("/", status_code=302)


# @app.get("/student/{user_id}", response_class=HTMLResponse)
# async def student_page(request: Request, user_id: str):
    
#     user = users_db.get(user_id)
#     if user and user["role"] == "student":
       
#         return templates.TemplateResponse("student.html", {"request": request, "user_id": user_id})
#     else:
        
#         return RedirectResponse("/", status_code=302)

# @app.get("/logout")
# async def logout():
#     return RedirectResponse("/", status_code=302)

@app.get("/", response_class=HTMLResponse)
async def assignment(request: Request):
    
    return templates.TemplateResponse("assignment.html", {"request": request})

# Route to get all courses
@app.get("/courses", response_model=List[schemas.Course])
async def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db=db, skip=skip, limit=limit)
    return courses

# Route to get details of a specific course and its assignments
@app.get("/course/{course_id}", response_class=HTMLResponse)
async def course_detail(request: Request, course_id: int, db: Session = Depends(get_db)):
    try:
        course = db.query(models.Course).filter(models.Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        assignments = db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()

        if not assignments:
            assignments = []

        return templates.TemplateResponse("course_detail.html", {
            "request": request,
            "course": course,
            "assignments": assignments
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Route to create a new course
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseBase, db: Session = Depends(get_db)):
    return crud.create_course(db=db, name=course.name)

# Route to create a new assignment
@app.post("/assignments/", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, course_name: int, db: Session = Depends(get_db)):
    return crud.create_assignment(db=db, title=assignment.title, description=assignment.description, 
                                  due_date=assignment.due_date, course_name=course_name)

# Route to get assignments for a specific course
@app.get("/assignments/{course_name}", response_model=List[schemas.Assignment])
def get_assignments(course_name: str, db: Session = Depends(get_db)):
    assignments = db.query(models.Assignment).join(models.Course).filter(models.Course.name == course_name).all()
    return assignments

# Route to get a specific assignment
@app.get("/assignment/{assignment_id}", response_model=schemas.Assignment)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = crud.get_assignment(db=db, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@app.post("/addAssignment")
async def add_assignment(request: Request, assignmentName: str = Form(...), courseName: str = Form(...), 
                          file: UploadFile = File(...), dueDate: str = Form(...), score: int = Form(...), 
                          description: str = Form(...), db: Session = Depends(get_db)):
    # Find the course from the database using courseName
    course = db.query(models.Course).filter(models.Course.name == courseName).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    new_assignment = models.Assignment(
        title=assignmentName,
        description=description,
        due_date=dueDate,
        score=score,
        file=file.filename,
        course_id=course.id
    )
    
    db.add(new_assignment)
    db.commit()
    
    return RedirectResponse(url=f"/teacher/{courseName}", status_code=303)

@app.post("/submit-assignment")
async def submit_assignment(
    assignment_id: int = Form(...),
    assignment_name: str = Form(...),
    assignment_due_date: str = Form(...),
    assignment_description: str = Form(...),
    file: UploadFile = File(...),
    comment: str = Form(...)
):
    # You would typically save the file and handle the comment here
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Save the assignment submission details in the database (e.g., link the file, comment, and assignment)
    # Example:
    # db.save_submission(assignment_id, file_location, comment)

    return {"message": "Assignment submitted successfully!"}