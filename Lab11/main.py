import ZODB, ZODB.FileStorage
import persistent
import transaction
import BTrees.OOBTree
from class_module import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

root.courses = BTrees.OOBTree.BTree()
root.courses[101] = Course(101, "Computer Programming", 4)
root.courses[201] = Course(201, "Web Programming", 4)
root.courses[202] = Course(202, "Software Engineering Principles", 5)
root.courses[301] = Course(301, "Artificial Intelligent", 3)

root.students = BTrees.OOBTree.BTree()
root.students[1101] = Student([], 1101, "Mr. John Doe")
root.students[1101].enrolls = [Enrollment(root.courses[101], 3.0, root.students[1101]), Enrollment(root.courses[201], 3.0, root.students[1101]), Enrollment(root.courses[301], 2.0, root.students[1101])]

root.students[1102] = Student([], 1102, "Mr. Zhong Li")
root.students[1102].enrolls = [Enrollment(root.courses[101], 4.0, root.students[1102]), Enrollment(root.courses[201], 3.0, root.students[1102]), Enrollment(root.courses[202], 1, root.students[1102])]

root.students[1103] = Student([], 1103, "Mr. Dvalinn Durinson")
root.students[1103].enrolls = [Enrollment(root.courses[101], 2.0, root.students[1103]), Enrollment(root.courses[201], 4.0, root.students[1103]), Enrollment(root.courses[202], 3.0, root.students[1103]), Enrollment(root.courses[301], 2.0, root.students[1103])]

transaction.commit()
db.close()