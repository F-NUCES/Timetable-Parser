import core.preprocessors.timetable as pt
from core.exporters.database import Database

# pt.main()

Database("latest").add_course_info()
