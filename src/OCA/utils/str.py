def intToStr(i, numDigits = 5):
    """Converts an integer to a string, prepending some 0 to get a certain number of digits"""
    s = str(i)
    while len(s) < numDigits:
        s = "0" + s
    return s
