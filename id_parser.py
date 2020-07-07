def get_courses_metadata():
    courses_metadata = {}
    with open("course_ids.txt", "r") as f:
        for i in f:
            id, name = i.split("|")
            if id not in courses_metadata:
                courses_metadata[id] = []
            courses_metadata[id].append(name)

    return courses_metadata
