import uiautomator2 as u2
from time import sleep

def XiaomiCl(d,DevicesName):
    d.shell("am start -n com.android.settings/.Settings")
    sleep(2)
    if DevicesName == 'XiaomiMi9':
        d.swipe_ext("up")
        d.swipe_ext("up")
        d.swipe_ext("up")
    if DevicesName == 'XiaomiRedmiNote9':
        d.swipe_ext("up")
        sleep(2)
        d.xpath('//*[@text="Приложения"]').click_exists(5)
    d.xpath('//*[@text="Все приложения"]').click_exists(5)
    d(resourceId="android:id/input").click_exists(5)
    d(resourceId="android:id/input").send_keys('Html')
    d(text='Просмотр HTML').click_gone()
    d(text='Очистить').click_gone()
    d(text='Очистить все').click_gone()
    d(resourceId="android:id/button1").click_gone()
    if DevicesName == 'XiaomiMi9':
        d.press("back")
        sleep(1)
        d.press("back")
        sleep(1)
        d.press("back")
        sleep(1)
    if DevicesName == 'XiaomiRedmiNote9':
        d.press("back")
        sleep(1)
        d.press("back")
        sleep(1)
        d.press("back")
        sleep(1)
        d.press("back")
        sleep(1)
    d.swipe_ext("down", scale=2)
    sleep(1)
    d.press("home")

#
# # XiaomiMi9 = "be11611b"
# # MACMi9 = '60-ab-67-f7-1d-a0'
# #
# XiaomiRedmiNote9 = "a3f47191"
# MACNote9 = '18-87-40-45-D2-9B'
# #
# # # Samsung A32
# # number3 = "RF8R40BZQLP"
# # MAC3 = '80-9f-f5-9c-71-30'
# # Name3 = 'Samsung A32'
# #
# # d = u2.connect_usb(XiaomiMi9)
# d2 = u2.connect_usb(XiaomiRedmiNote9)
# # # d = u2.connect_usb(number3)
# #
# #
# #
# XiaomiCl(d2,'XiaomiRedmiNote9')
# # XiaomiCl(d,'XiaomiMi9')