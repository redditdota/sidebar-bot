from datetime import *

def get_countdown():
    today = date.today()
    release = date(2018,11,28)
    days = int((release - today).days)

    if days == 3:
        days = "3!"
    elif days == 2:
        days = "2!!"
    elif days == 1:
        days = "1!!!"
    elif days < 1:
        days = "Pog"

    return str(days)