
from fastapi import FastAPI, Request, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date
from typing import List,Optional
from collections import defaultdict
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

users_db = {
    "1001": {"role": "lecturer"},
    "9001": {"role": "student"},
}

# assignments = []
counter = 0
assignments_by_course = defaultdict(list)

class Assignment(BaseModel):
    id : int
    name: str
    course: str
    file: str  
    due_date: date
    score: int
    description: str


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(request: Request, id: str = Form(...)):
    
    user = users_db.get(id)
    if user:
        role = user["role"]
        if role == "lecturer":
            return RedirectResponse(f"/teacher/{id}", status_code=302)
        elif role == "student":
            return RedirectResponse(f"/student/{id}", status_code=302)
    else:
        raise HTTPException(status_code=400, detail="Invalid ID")
    

@app.get("/teacher/{user_id}", response_class=HTMLResponse)
async def teacher_page(request: Request, user_id: str):
   
    user = users_db.get(user_id)
    if user and user["role"] == "lecturer":
        return templates.TemplateResponse("teacher.html", {"request": request, "user_id": user_id, "assignments_by_course": assignments_by_course, "active_page" : "list"})
    else:
        return RedirectResponse("/", status_code=302)


@app.get("/student/{user_id}", response_class=HTMLResponse)
async def student_page(request: Request, user_id: str):
    
    user = users_db.get(user_id)
    if user and user["role"] == "student":
       
        return templates.TemplateResponse("student.html", {"request": request, "user_id": user_id})
    else:
        
        return RedirectResponse("/", status_code=302)

@app.get("/logout")
async def logout():
    return RedirectResponse("/", status_code=302)




#add assignment in teacher side
@app.post("/addAssignment")
async def add_assignment(request: Request, assignmentName: str = Form(...), courseName: str = Form(...), 
                          file: UploadFile = File(...), dueDate: str = Form(...), score: int = Form(...), 
                          description: str = Form(...)):
    new_assignment = Assignment(
        id=len(assignments_by_course[courseName]) + 1,  # Assuming auto-increment for assignment IDs
        name=assignmentName,
        course=courseName,
        file=file.filename,  
        due_date=dueDate,
        score=score,
        description=description
    )
    assignments_by_course[courseName].append(new_assignment)
    
    return templates.TemplateResponse("teacher.html", {"request": request, "assignments_by_course": assignments_by_course, "active_page" : "list", "course_name" : courseName})


@app.get("/teacher")
async def teacher_page(request: Request):
    return templates.TemplateResponse("teacher.html", {"request": request, "assignments_by_course": assignments_by_course, "active_page" : "list"})

@app.get("/teacher/{course_name}", response_class=HTMLResponse)
async def teacher_course_page(course_name: str, request: Request):
    assignments = assignments_by_course.get(course_name, [])
    return templates.TemplateResponse("teacher.html", {"request": request, "course_name": course_name, "assignments": assignments})

#get the details of assignment
@app.get("/assignment/{course_name}/{assignment_id}", response_class=HTMLResponse)
async def show_details(request: Request, course_name: str, assignment_id: int):
    assignments = assignments_by_course.get(course_name)  # Use the get_course function

    found_assignment = None
    for assignment in assignments:
        if assignment.id == assignment_id:
            found_assignment = assignment
            break  # Exit the loop once the assignment is found
    
    if not found_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return templates.TemplateResponse("teacher.html", {
        "request": request,
        "assignment": found_assignment,
        "active_page": "details",
        "assignments_by_course": assignments_by_course,
        "course_name": course_name
    })
# @app.get("/assignment/grade/{assignment_id}", response_class = HTMLResponse)
# async def give_grade(request : Request, assignment_id : int):
#     if assignment_id < 0 or assignment_id >= len(assignments):
#         raise HTTPException(status_code = 404, detail = "Assignment not found")
#     assignment = assignments[assignment_id]
#     return templates.TemplateResponse("teacher.html", {"request" : request, "assignment" : assignment, "active_page" : "grade"})

#edit the assignment
@app.get("/assignment/edit/{course_name}/{assignment_id}", response_class = HTMLResponse)
async def edit_assignment(request : Request, assignment_id : int, course_name : str):
    assignments = assignments_by_course.get(course_name)
    found_assignment = None

    for assignment in assignments:
        if assignment.id == assignment_id:
            found_assignment = assignment
            break  
    
    if not found_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return templates.TemplateResponse("teacher.html", {
        "request" : request, 
        "assignment" : found_assignment, 
        "active_page" : "edit", 
        "assignments_by_course": assignments_by_course,
        "course_name" : course_name
    })


@app.get("/assignment/remove/{course_name}/{assignment_id}", response_class = HTMLResponse)
async def remove_assignment(request : Request, assignment_id : int, course_name : str):
    assignments = assignments_by_course.get(course_name)
    found_assignment = None
    found_course = None
    
    for i,assignment in enumerate(assignments):
        if assignment.id == assignment_id:
            found_course = course_name
            found_assignment = i
            break
    

    if found_assignment is None:
        raise HTTPException(status_code = 404, detail = "Assignment Not found")

    assignments_by_course[found_course].pop(found_assignment)

    return templates.TemplateResponse("teacher.html", {"request" : request, "active_page" : "remove", "assignments_by_course": assignments_by_course, "course_name" : found_course})


@app.post("/assignment/upload", response_class=RedirectResponse)
async def update_assignment(request: Request, assignment_id: int = Form(...), assignmentName: str = Form(...),
                            courseName: str = Form(...), file: Optional[UploadFile] = File(None), 
                            dueDate: date = Form(...), score: int = Form(...), description: str = Form(...)):
    
    # Search for the assignment in the appropriate course
    found_assignment = None
    old_course = None
    
    for course, assignments in assignments_by_course.items():
        for assignment in assignments:
            if assignment.id == assignment_id:
                found_assignment = assignment
                old_course = course
                break
        if found_assignment:
            break

    # If the assignment was not found, raise an error
    if not found_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Remove the found assignment from the old course's list
    assignments_by_course[old_course].remove(found_assignment)

    # Update the found assignment with new data
    found_assignment.name = assignmentName
    found_assignment.course = courseName
    found_assignment.due_date = dueDate
    found_assignment.score = score
    found_assignment.description = description

    # Handle file upload if a new file is provided
    # if file:
    #     # Define where you want to save the file (this is just an example, adjust the path as needed)
    #     file_location = f"uploads/{file.filename}"
    #     os.makedirs("uploads", exist_ok=True)  # Ensure the directory exists
        
    #     # Save the uploaded file
    #     with open(file_location, "wb") as f:
    #         f.write(await file.read())
        
    #     # Update the assignment with the file path
    #     found_assignment.file = file_location

    # Add the updated assignment to the new course list
    assignments_by_course[courseName].append(found_assignment)

    # Redirect to the course's page to display the updated assignment list
    return RedirectResponse(url=f"/teacher", status_code=303)

#Assignment page
@app.get("/assignments/{user_id}", response_class=HTMLResponse)
async def assignments_page(request: Request, user_id: str):
    user = users_db.get(user_id)
    if user and user["role"] == "student":
        # You can pass assignments to the student page if needed
        return templates.TemplateResponse("assignment.html", {"request": request, "user_id": user_id, "assignments_by_course": assignments_by_course})
    else:
        return RedirectResponse("/", status_code=302)

#Get the assignment from teacher  
@app.get("/course/{course_name}/assignments", response_model=List[Assignment])
async def get_assignments_for_course(course_name: str):
    assignments = assignments_by_course.get(course_name, [])
    
    if not assignments:
        raise HTTPException(status_code=404, detail="No assignments found for this course")
    
    return assignments

@app.get("/course/{course_id}", response_class=HTMLResponse)
async def course_detail_page(request: Request, course_id: int):
    course = courses_by_id.get(course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course_name = course["name"]  # Get the course name based on the ID

    # Fetch assignments for this specific course (assuming assignments_by_course exists)
    assignments = [a for a in assignments_by_course.get(course_name, [])]

    return templates.TemplateResponse("course_detail.html", {
        "request": request,
        "course": course,  # Pass the course object
        "assignments": assignments  # Pass assignments for the course
    })

@app.get("/assignment/{course_name}/{assignment_id}/download")
async def download_assignment(course_name: str, assignment_id: int):
    # Fetch assignments for the given course
    assignments = assignments_by_course.get(course_name)
    
    if not assignments:
        raise HTTPException(status_code=404, detail="Course not found")

    # Find the specific assignment by ID
    found_assignment = next((a for a in assignments if a.id == assignment_id), None)
    
    if not found_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Assuming that the file is saved on the server, you need to return it
    file_location = f"uploads/{found_assignment.file}"
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_location, media_type='application/octet-stream', filename=found_assignment.file)
