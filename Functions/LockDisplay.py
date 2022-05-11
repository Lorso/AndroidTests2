from time import sleep
import uiautomator2 as u2


def Lock(d):
    sleep(1)
    d.shell('input keyevent 26')
    sleep(1)
    d.shell('input touchscreen swipe 930 880 930 280')


# d = u2.connect_usb("RF8R40BZQLP")
# d2 = u2.connect_usb("be11611b")
# d3 = u2.connect_usb("a3f47191")
# Lock(d2)
# Lock(d2)
# Lock(d3)