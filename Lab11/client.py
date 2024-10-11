import ZODB, ZODB.FileStorage
import persistent
import transaction
from class_module import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

if __name__ == "__main__":
    courses = root.courses
    for c in courses:
        course = courses[c]
        course.printDetail()
    
    print()
    
    students = root.students
    for s in students:
        student = students[s]
        student.printTranscript()
        print()
    
db.close()