import time
import re
from datetime import datetime


def get_section(name, joiner=","):
    """
        Obtain section from course name.
    """
    # https://stackoverflow.com/a/12999616
    if joiner in name:
        joiner = ", "
    else:
        joiner = " & "
    sections = re.findall(r"[BM]?(?:CS|SP|DS|SE)-?\d?\w?\d?", name)
    if len(sections) == 1:
        return sections[0]
    return f"{joiner}".join(sections)


def remove_section(course_title):
    """
        Course title without section
    """
    section = get_section(course_title)
    return course_title.rstrip(f"({section})").strip()


def convert_to_12h(t):
    strt = time.strptime(str(t).replace(".", ":") + "0", "%H:%M")
    return time.strftime("%I:%M %p", strt)


def convert_to_24h(t):
    strt = time.strptime(t, "%I:%M %p")
    a = time.strftime("%H:%M", strt)
    return float(a.replace(":", "."))


# Probably add some time library in future for better time manipulation
def generate_end_time(course_start_time, lab_course=False):
    # TODO: Timing for lab [X]
    # TODO: Interval check am -> pm conversion
    time, interval = course_start_time.split()
    hour, minute = [int(float(i)) for i in time.split(":")]
    interval = interval.replace(".", "").upper().replace("NOON", "PM")

    if lab_course:
        # TODO: Simplify this!
        if hour + 3 >= 12:  # TODO: Add unit tests, need to check this condition
            interval = "PM"
        if hour + 3 > 12:
            hour -= 12
        return f"{str(hour+3).zfill(2)}:{str(minute).zfill(2)} {interval}"

    if hour >= 12:
        hour = 0

    hour += 1

    minute += 20

    if minute >= 60:
        hour += 1
        minute -= 60

    return f"{str(hour).zfill(2)}:{str(minute).zfill(2)} {interval}"


# BAK
def display_courses(sections=True):
    for i in get_courses(sections=sections):
        section = get_section(i)
        if section:
            print(i)
        else:  # When no sections are found for the course, Probably a MS-Course
            print(i)


def get_course_time(name, sheet_location, timings, periods):
    """
    Obtain lecture timings for course.

    @args:
        name: Name of the course
        sheet_location: index of name in sheet (required to interpret lecture timing)
    """
    if not timings[sheet_location]:
        for i in range(sheet_location)[::-1]:
            if timings[i]:
                time, interval = timings[i].split()
                interval = interval.replace(".", "").upper()
                hour, minute = [int(i) for i in time.split(":")]
                minute += periods[sheet_location - 1]
                time = f"{str(hour).zfill(2)}:{str(minute).zfill(2)} {interval.replace('NOON', 'PM')}"
                break
    else:
        time = timings[sheet_location].replace(".", "").upper().replace("NOON", "PM")
        time = ":".join([i.zfill(2) for i in time.split(":")])

    return time.strip()
