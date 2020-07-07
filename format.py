import utils
import json
import io
import os


class Course:
    def __init__(
        self,
        name: str,
        room: str,
        day: str,
        section: str,
        start_time: str,
        end_time: str,
    ):
        """
        @args:
        Name: Name of the course
        Section: Section of the course
        start_time: start_time of the course (start-time; end-time)
        Room: Venue of the course

        @Example:
        name: Linear Algebra
        section: CS-A
        start_time: ((9:30, 10:50),(...))
        room: (CS-2)
        day: Monday
        """
        self.name = name
        self.section = section
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.day = day
        self.course_type = "BS" if "MS" not in self.name else "MS"

    @classmethod
    def from_dict(cls, mydict):
        return cls(
            name=mydict["name"],
            section=mydict["section"],
            start_time=mydict["start_time"],
            end_time=mydict["end_time"],
            room=mydict["room"],
            days=mydict["days"],
        )

    def to_dict(self):
        return {
            "name": self.name,
            "section": self.section,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "room": self.room,
            "day": self.day,
        }

    def to_md(self):
        return f"{self.name.split('(')[0].strip(): <50} | {self.room: <23} | {self.day: <11} | {self.start_time: <25} - {self.end_time: <25} |\n"

    def to_json(self, filename=None, data=None):
        if data:
            json.dump(data, filename, indent=4)
        else:
            json.dump(self.to_dict(), filename, indent=4)

    def write_to_file(self, file_path=".", mode="a", data=None, dump_type="text"):
        with open(file_path, mode) as f:
            if dump_type == "json":
                self.to_json(f, data=data)
            else:
                if isinstance(data, list):
                    for i in data:
                        f.write(i)
                else:
                    f.write(self.get_text())

    def is_lab_course(self):
        return "lab" in self.name.lower()

    def get_text(self):
        return f"{self.name.split('(')[0].strip(): <40}\t{self.section.replace('BCS-',''): <8}\t{self.room: <13}\t{self.day: <11}\t{self.start_time: <9} - {self.end_time: <9}\n\n"

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"
