from sqlalchemy.orm import Session
from . import models, schemas

# Create a new course
def create_course(db: Session, name: str):
    db_course = models.Course(name=name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Get all courses
def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

# Get a specific course by ID
def get_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    print(course)
    return course

# Create a new assignment
def create_assignment(db: Session, title: str, description: str, due_date: str, course_id: int):
    db_assignment = models.Assignment(
        title=title,
        description=description,
        due_date=due_date,
        course_id=course_id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

# Get assignments by course
def get_assignments_by_course(db: Session, course_id: int):
    return db.query(models.Assignment).filter(models.Assignment.course_id == course_id).all()

# Get a specific assignment by ID
def get_assignment(db: Session, assignment_id: int):
    return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
