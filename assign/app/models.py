from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    assignments = relationship('Assignment', back_populates='course')

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    due_date = Column(Date)
    score = Column(Integer, default=0)
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    course = relationship('Course', back_populates='assignments')

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String)
    password = Column(String)
