import re


def get_section(name):
    """
    Obtain section from course name.
    """
    sections = re.findall(r"[BM]?(?:CS|SP|DS)-?\d?\w?\d?", name)
    if sections:
        return ", ".join(sections)


with open("nc.txt", "r") as f:
    courses = f.readlines()

    info = []
    for i in courses:
        try:
            code = i[:5]
            course = i.replace(code, "").strip()
            if "(" in course:
                course, _ = course.split("(")

            split_key = f"({get_section(course)})"

            if split_key:
                course = course.split(split_key)[0].strip()
            course = course.strip()
            if course:
                info.append((code, course))
        except Exception as e:
            print(e)
            continue

    for code, name in set(info):
        print(code, name)
