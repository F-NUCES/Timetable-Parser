
def export_timetable(export_directory, courses=None, dump_type="json"):
    # total hours - consumed hours
    export_directory = f"{dump_type}/"

    with db_session:
        my_dict = {}
        # section_timing = {}
        a = sorted(select(c for c in Courses)[:], key=lambda x: DAYS.index(x.day))
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
