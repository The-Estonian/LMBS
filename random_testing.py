from re import match

def email_validator(variable):
    pat = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if len(variable) > 5:
        if match(pat,variable):
            return True
    return False

if __name__ == "__main__":
    print(email_validator(""))