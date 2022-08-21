from pony.orm import *

import core.models.db_course as db_model
from core.preprocessors.timetable import Reader


class Database:
    def __init__(self, database_name="latest"):
        self.course_data = Reader()
        db_model.db.bind(
            provider="sqlite",
            filename=f"{database_name}.db",
            create_db=True,
        )
        db_model.db.generate_mapping(create_tables=True)
        self.database_name = database_name

    @db_session
    def add_course_info(self):
        names = set()
        for course_info in self.course_data.get_courses_info():
            _course = db_model.DBCourses(
                name=course_info.name,
                section=course_info.section,
                start_time=course_info.start_time,
                end_time=course_info.end_time,
                room=course_info.room,
                day=course_info.day,
                semester=course_info.semester,
            )
            names.add(course_info.name)

        for course_title in sorted(names):
            db_model.CourseTitle(name=course_title)

    @db_session
    def get_courses(self):
        return db_model.DBCourses.select()

    @db_session
    def get_courses_list(self):
        return db_model.CourseTitle.select()

