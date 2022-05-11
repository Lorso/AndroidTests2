from datetime import datetime


def NowDateVideo():
    now = datetime.now().strftime("%d_%m_%Y(%H_%M)")
    return now


def NowDate():
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return now
