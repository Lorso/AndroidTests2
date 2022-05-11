def scroll (d, DevicesName):
    if DevicesName == "Samsung A32":
        d.swipe_ext('up', scale=0.6)
    else:
        d.swipe_ext('up', scale=0.9)



