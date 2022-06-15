import time
from time import sleep
from datetime import datetime
from Functions.DataName import NowDate
from Functions.Browser import BrowserMiuiExit
from Functions.Browser import BrowserChromeExit


def CheckInternet (d, DevicesName):
    d.press("home")
    sleep(10)

    # t0 = time.time()
    # d.shell("am start -a android.intent.action.VIEW  https://gb.ru/")
    # google = d.xpath('//*[@content-desc="gb"]')
    # google.wait(10)
    # check1 = google.exists
    # t1 = time.time() - t0
    #
    # sleep(3)

    t2 = time.time()
    d.shell("am start -a android.intent.action.VIEW  https://vk.com")
    sleep(5)
    button3 = d(resourceId="com.android.chrome:id/positive_button")
    if button3.exists: d(resourceId="com.android.chrome:id/positive_button").click()

    lenta = d.xpath('//*[@text="Войти"]')
    lenta.wait(35)
    check2 = lenta.exists
    t3 = time.time() - t2


    sleep(3)

    if check2:
        # print(f"{NowDate()}  gb: {check1} | Время загрузки страницы: {round(t1,2)} сек")
        print(f"{NowDate()}  VK.com: {check2} | Время загрузки страницы: {round(t3,2)} сек")
        BrowserChromeExit(d)
        return True
    else:
        # print(f"{NowDate()}  gb: {check1} | Страница не загрузилась")
        print(f"{NowDate()}  VK.com: {check2} | Страница не загрузилась")
        BrowserChromeExit(d)
        return False
