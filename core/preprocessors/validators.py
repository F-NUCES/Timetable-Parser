# Course title detection happens here.
def is_course_title(text_stream):
    
    if not text_stream or isinstance(text_stream, int):
        return False
    elif len(text_stream) < 12:
        return False
    elif not " (" in text_stream:
        return False
    return True

def is_lab_course(text_stream):
    return "lab" in text_stream.lower()

