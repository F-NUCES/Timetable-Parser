# https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string
def remove_multiple_spaces(string):
    return " ".join(string.split()).strip()

