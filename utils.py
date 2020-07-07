import time
from datetime import datetime


def convert_to_12h(t):
    strt = time.strptime(str(t).replace(".", ":") + "0", "%H:%M")
    return time.strftime("%I:%M %p", strt)


def convert_to_24h(t):
    strt = time.strptime(t, "%I:%M %p")
    a = time.strftime("%H:%M", strt)
    return float(a.replace(":", "."))


# Probably add some time library in future for better time manipulation
def generate_end_time(start_time, lab_course=False):
    # TODO: Timing for lab [X]
    # TODO: Interval check am -> pm conversion
    time, interval = start_time.split()
    hour, minute = [int(i) for i in time.split(":")]
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
