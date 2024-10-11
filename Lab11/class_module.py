import ZODB, ZODB.FileStorage
import persistent
import transaction
import BTrees._OOBTree

class Course(persistent.Persistent):
    def __init__(self, id, name, credit = 3):
        self.credit = credit
        self.id = id
        self.name = name
        
    def __str__(self):
        return "Course ID: {}, Course Name: {}, Course Credit: {}".format(self.id, self.name, self.credit)
    
    def getCredit(self):
        return self.credit
    
    def setName(self, name):
        self.name = name
    
    def printDetail(self):
        print(self.__str__())

class Enrollment(persistent.Persistent):
    def __init__(self, course, grade, student):
        self.course = course
        self.grade = grade
        self.student = student
        
    def __str__(self):
        return "Course: {}, Grade: {}".format(self.course, self.grade, self.student)
    
    def getCourse(self):
        return self.course
    
    def getGrade(self):
        return self.grade
    
    def setGrade(self, grade):
        self.grade = grade
        
    def printDetail(self):
        print(self.__str__())
    
class Student(persistent.Persistent):
    def __init__(self, enrolls, id, name):
        self.enrolls = enrolls
        self.id = id
        self.name = name
        
    def __str__(self):
        courses = ""
        courses += "================= Transcripts =================\n"
        courses += "Student ID: {}, Student Name: {}\n".format(self.id, self.name)
        for enroll in self.enrolls:
            courses += "Course: {}, Credit: {}, Grade: {}\n".format(enroll.getCourse().name, enroll.getCourse().credit, self.convertGradeToLetter(enroll.getGrade()))
        courses += "Total GPA is: {:.3}\n".format(self.getGPA())
        courses += "==============================================="
        return courses
    
    def convertGradeToLetter(self, grade):
        if grade >= 4.0:
            return "A"
        elif grade >= 3.0:
            return "B"
        elif grade >= 2.0:
            return "C"
        elif grade >= 1.0:
            return "D"
        else:
            return "F"
        
    def getGPA(self):
        totalpoint = 0
        totalcredit = 0
        for enroll in self.enrolls:
            totalpoint += enroll.getGrade() * enroll.getCourse().getCredit()
            totalcredit += enroll.getCourse().getCredit()
        return totalpoint / totalcredit
    
    def enrollCourse(self, course):
        enrollobj = Enrollment(course, None, self)
        self.enrolls.append(enrollobj)
        return enrollobj
    
    def getEnrollment(self, course):
        for enroll in self.enrolls:
            if enroll.getCourse() == course:
                return enroll
        return None
    
    def printTranscript(self):
        print(self.__str__())
    
    def setName(self, name):
        self.name = name