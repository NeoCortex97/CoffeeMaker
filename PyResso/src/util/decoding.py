

def separateBy(text="", sep=" "):
    result = ""
    for c in text:
        if c == sep:
            break
        result += c
    return result


def isInteger(string):
    try:
        int(string)
        return True
    except ValueError:
        return False