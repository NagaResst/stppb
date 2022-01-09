def pos_neg(a, b, negative):
    if (a < 0 and b > 0) or (b < 0 and a > 0):
        test = "AB"
    elif b < 0 and a < 0:
        test = "BA"
    else:
        test = "NO"

    if test == "AB" and negative == False:
        return True
    elif test == "BA" and negative == True:
        return True
    else:
        return False
