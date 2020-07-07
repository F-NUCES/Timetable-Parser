from openpyxl import load_workbook
import re
import os
from pony.orm import *

import utils

from format import Course as Subject
from page_generator import *

db = Database()


class Courses(db.Entity):
    name = Required(str)
    section = Required(str)
    start_time = Required(str)
    end_time = Required(str)
    room = Required(str)
    day = Required(str)


class CoursesInfo(db.Entity):
    name = Required(str)


DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


class Reader:
    def __init__(self, filename):
        self.info = list(load_workbook(filename=filename).active.values)
        self.periods = self.info[2]
        self.timings = self.info[3]
        self.content = self.info[4:-3]

    @db_session
    def get_courses(self, sections=True):
        """
        Extracts all courses from xlsx file which are being offered.
        """
        subjects = []

        for row in self.content:
            # TODO: Why first two indexes are missed? [Add Documentation]
            for subject in row[2:]:
                if subject:
                    subjects.append(subject.strip())

        if sections:
            return subjects

        for i in sorted({i.split("(")[0].strip() for i in subjects}):
            CoursesInfo(name=i)
        return sorted({i.split("(")[0].strip() for i in subjects})

    def get_course_time(self, name, sheet_location):
        """
        Obtain lecture timings for course.

        @args:
            name: Name of the course
            sheet_location: index of name in sheet (required to interpret lecture timing)
        """
        if not self.timings[sheet_location]:
            for i in range(sheet_location)[::-1]:
                if self.timings[i]:
                    time, interval = self.timings[i].split()
                    interval = interval.replace(".", "").upper()
                    hour, minute = [int(i) for i in time.split(":")]
                    minute += self.periods[sheet_location - 1]
                    time = f"{str(hour).zfill(2)}:{str(minute).zfill(2)} {interval.replace('NOON', 'PM')}"
                    break
        else:
            time = (
                self.timings[sheet_location]
                .replace(".", "")
                .upper()
                .replace("NOON", "PM")
            )
            time = ":".join([i.zfill(2) for i in time.split(":")])

        return time.strip()

    def get_venue(self, content):
        return content[1]

    def get_section(self, name):
        """
        Obtain section from course name.
        """
        sections = re.findall(r"[BM]?CS-?\d?\w?\d?", name)
        print(name, sections)
        return ", ".join(sections)

    def display_courses(self, sections=True):
        for i in self.get_courses(sections=sections):
            section = self.get_section(i)
            if section:
                print(i)
            else:  # When no sections are found for the course, Probably a MS-Course
                print(i)

    def get_days_info(self):
        count = 0

        DAYS_INFO = {k: [] for k in DAYS}
        # Day [0] -> Data Stored for Day 0 which is Monday
        # Day [1] -> Data Stored for Day 1 which is Tuesday

        for row in self.content:
            if row[0]:
                if row[0].strip() == DAYS[count]:
                    count += 1
            DAYS_INFO[DAYS[count - 1]].append(row)

        return DAYS_INFO

    @db_session
    def dump_to_db(self):
        """
        Returns list of course objects
        """
        DAYS_INFO = self.get_days_info()
        # TODO: Simplify this logic
        for day in DAYS:
            for column in range(len(DAYS_INFO[day])):
                for index, course_title in enumerate(DAYS_INFO[day][column]):
                    if course_title and " (" in course_title:
                        # https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string
                        course_title = " ".join(course_title.split())

                        course_start_timing = self.get_course_time(course_title, index)

                        is_lab_course = True if "lab" in course_title.lower() else False

                        course_end_timing = utils.generate_end_time(
                            course_start_timing, lab_course=is_lab_course
                        )
                        section = self.get_section(course_title)

                        try:
                            Courses(
                                name=course_title,
                                # name=course_title[: course_title.find("(")],
                                section="MCS" if not section else section,
                                start_time=course_start_timing,
                                end_time=course_end_timing,
                                room=self.get_venue(DAYS_INFO[day][column]),
                                day=day,
                            )
                        except Exception as e:
                            print(e)


def export_timetable(export_directory, courses=None, dump_type="json"):
    # total hours - consumed hours
    if dump_type == "json":
        export_directory += "json/"
    elif dump_type == "text":
        export_directory += "text/"
    elif dump_type == "md":
        export_directory += "md/"

    with db_session:
        my_dict = {}
        # section_timing = {}
        a = sorted(
            select(c for c in Courses)[:], key=lambda x: DAYS.index(x.day)
        )

        b = sorted(a, key=lambda x: int(utils.convert_to_24h(x.start_time)))

        for course in b:
            for entity in courses:
                # print("%r - %r" % (entity, course.name))
                if entity in course.name:
                    section = re.search(r"[BM]?CS-?\d?\w?", course.section)
                    section = section.group() if section else course.section

                    export_entity = Subject(
                        course.name,
                        course.room,
                        course.day,
                        course.section,
                        course.start_time,
                        course.end_time,
                    )

                    if section not in my_dict.keys():
                        my_dict[section] = []

                    if dump_type == "json":
                        my_dict[section].append(export_entity.to_dict())
                    elif dump_type == "text":
                        my_dict[section].append(export_entity.get_text())
                    elif dump_type == "obj":
                        my_dict[section].append(export_entity)
                    elif dump_type == "md":
                        my_dict[section].append(export_entity.to_md())

        for k, v in sorted(my_dict.items()):
            if dump_type == "json":
                export_entity.write_to_file(
                    export_directory + k + ".json", data=v, dump_type=dump_type
                )

            elif dump_type == "text":
                export_entity.write_to_file(
                    export_directory + k + ".txt", data=v, dump_type=dump_type,
                )

            elif dump_type == "obj":
                pass

            elif dump_type == "md":
                with open(export_directory + k + ".md", "a") as f:
                    f.write(f"\n\n# Timetable for {k}\n\n")
                    f.write(
                        """| **Subject**                           | **Venue** | **Day**       | **Timing**     |
| --------------------------------- | ----- | --------- |:----------:|\n"""
                    )
                    for i in v:
                        f.write(i)
                    f.write("\n")


if __name__ == "__main__":

    files_path = "source_files/"
    output_path = "course_files/"
    timetable_files = {"old": "old.xlsx", "new": "new.xlsx", "latest": "latest.xlsx"}
    selected_timetable = timetable_files.get("latest")
    timetable = Reader(files_path + selected_timetable)
    db.bind(
        provider="sqlite",
        filename=f"{selected_timetable.split('.')[0]}.sqlite",
        create_db=True,
    )
    db.generate_mapping(create_tables=True)
    # timetable.get_courses(sections=False)
    # timetable.dump_to_db()
    # timetable.display_courses()

    courses = (
        "Discrete Structures (BCS-4A)",
        "Data Structures (BCS-4C)",
        "Data Structures Lab (BCS-4C",
        "Assembly L. (BCS-4A)",
        "Assembly Lang. Lab (BCS-4A",
        "Entrepreneurship (BCS-4A)",
        "Probability & Statistics (BCS-4A)",
    )

    # courses = (
    #     "Operating Systems",
    #     "Mass Communication",
    #     "Probability & Statistics",
    #     "Environmental Studies",
    #     "Principles of Leadership",
    #     "Design & Analysis of Algorithms",
    #     "Psychology",
    #     "Database Systems",
    # )

    # Cleanup
    # for i in os.listdir(output_path):
    #     if os.path.isfile(i):
    #         os.remove(output_path + i)

    # print("Extracting timetable for given courses:")
    # for i in courses:
    #     print(">>> ", i)

    export_timetable(output_path, courses=courses, dump_type="md")

