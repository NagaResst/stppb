def not_string(str):
    if str[0:2] == "not":
        return str
    else:
        str = "not " + str
        return str

