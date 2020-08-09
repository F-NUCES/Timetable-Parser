from pony.orm import *

db = Database()

class DBCourses(db.Entity):
    name = Required(str)
    section = Required(str)
    start_time = Required(str)
    end_time = Required(str)
    room = Required(str)
    day = Required(str)
    semester = Required(str)

class CourseTitle(db.Entity):
    name = Required(str)
    