import pendulum
import requests
from core.models.course import Course
import core.exporters.database as course_db
from pony.orm import *


server_url = "http://localhost:5000"

my_db = course_db.Database()

days_in_week = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat")


@db_session
def get_courses():
    courses_list = []
    for i in my_db.get_courses_list():
        courses_list.append(i.to_dict()["name"])

    # r = requests.get(f"{server_url}/courses")
    # for num, i in enumerate(r.json()):
    #     courses_list.append(i[str(num)])
    return courses_list


@db_session
def get_courses_info(semester_number="4"):
    # courses_list = get_courses()
    courses_info = []
    total_courses_info = my_db.get_courses()
    for course in total_courses_info:
        courses_info.append(course.to_dict())
    
    return courses_info




def main():
    cleaned_courses = []

    for i in get_courses_info():
        new_dict = {}
        new_dict["name"] = i["name"]
        new_dict["time"] = pendulum.from_format(i["start_time"], "HH:mm A")
        new_dict["start_time"] = i["start_time"]
        new_dict["end_time"] = i["end_time"]
        new_dict["day"] = i["day"]
        new_dict["section"] = i["section"]
        new_dict["room"] = i["room"]
        days = i["day"].split(",")
        if days:
            new_dict["day"] = days
        else:
            new_dict["day"] = [days]

        cleaned_courses.append(new_dict)
    courses_obj = []

    for i in cleaned_courses:
        # for i in sorted(cleaned_courses, key=lambda x: x["start_time"]):
        day = []

        for j in i["day"]:
            j = j.strip()
            if len(j) > 3:
                day.append(j[:3])
            else:
                day.append(j)
        
        c = Course(
            i["name"],
            i["room"],
            day,
            i["section"],
            i["start_time"][:5],
            i["end_time"][:5],
            ""
        )
        courses_obj.append(c)

    with open(f"timetable.md", "a") as f:
        start_day = 0
        end_day = 2
        num = 0
        timetable_heading = False
        for i in sorted(courses_obj, key=lambda x: days_in_week.index(x.day[0])):
            if days_in_week.index(i.day[0]) != num:
                num += 1
                start_day += 1
                end_day += 1
                timetable_heading = False

            if not timetable_heading:
                if len(i.day) == 2:
                    days_info = (
                        f"{days_in_week[start_day]} - {days_in_week[end_day]}"
                    )
                else:
                    days_info = i.day[0]

                f.write(f"\n\n# Timetable on Day {days_info}\n\n")

                f.write(
                    """| **Subject**                           | **Venue** | **Day**       | **Section**       | **Timing**       |
| --------------------------------- | ----- | --------- | -----| :----------:|\n"""
                )
                timetable_heading = True

            f.write(i.to_md())

# get_courses()
# get_courses_info()
main()