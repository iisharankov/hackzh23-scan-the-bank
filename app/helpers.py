

def check_valid_sensitivities(counter):
    if (counter[0] > 0) or (counter[1] > 0 and counter[2] > 0) or (counter[1] > 0 and counter[3] > 0):
        return True 
    return False