import pendulum
import requests
from format import Course


server_url = "http://localhost:5000"


days_in_week = ("Mon", "Tue", "Wed", "Thu", "Fri")


def get_courses():
    courses_list = []
    r = requests.get(f"{server_url}/courses")
    for num, i in enumerate(r.json()):
        courses_list.append(i[str(num)])
    return courses_list


def get_courses_info(semester_number="4"):
    courses_list = get_courses()
    courses_info = []
    for index, course in enumerate(courses_list, 0):
        r = requests.get(f"{server_url}/course", params={"name": course})
        output = r.json()
        if (
            output[0]["semester"] == semester_number
            and "BCS" in output[0]["section"]
        ):
            courses_info = courses_info + output
    return courses_info


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
    c = Course(
        i["name"],
        i["room"],
        i["day"],
        i["section"],
        i["start_time"],
        i["end_time"],
    )
    courses_obj.append(c)

with open("file.md", "a") as f:

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
