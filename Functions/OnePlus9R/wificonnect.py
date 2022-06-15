from time import sleep

from Functions.DataName import NowDate
from Functions.TelegramApi import SendMessage


def wificonnect(d, ssid, f, devices_name):
    d.press("home")
    d.shell('svc wifi enable')
    sleep(1)

    d.shell("am start -n com.steinwurf.adbjoinwifi/.MainActivity -e ssid '" + ssid + "'")
    sleep(5)
    d.app_start("com.android.settings", ".Settings$WifiSettings2Activity")
    sleep(5)
    d.shell("am force-stop com.steinwurf.adbjoinwifi")  # Отключения АДБджоина
    if d(description="Настройки").exists:
        d(description="Настройки").click()
        print(f"{NowDate()}  SSID найден")
        f.write(f"{NowDate()}  SSID найден\n")
        sleep(5)

        # мак с рандомного на обычный
        while d(text='Регистрация в сети').exists or d(text='Не подключено').exists:
            if d(resourceId="android:id/title", text="Дополнительно").exists():
                d(resourceId="android:id/title", text="Дополнительно").click()
            sleep(3)
            if d(resourceId="android:id/title", text="Конфиденциальность").exists():
                d(resourceId="android:id/title", text="Конфиденциальность").click()
            sleep(3)
            if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
                sleep(10)
            if d(resourceId="android:id/title", text="Дополнительно").exists():
                d(resourceId="android:id/title", text="Дополнительно").click()
            sleep(3)
            if d(resourceId="android:id/title", text="Конфиденциальность").exists():
                d(resourceId="android:id/title", text="Конфиденциальность").click()
            sleep(2)
            if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
            sleep(3)
            if d(resourceId="android:id/title", text="Конфиденциальность").exists():
                d(resourceId="android:id/title", text="Конфиденциальность").click()
            sleep(2)
            if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
            sleep(12)
        if d(text='НАСТРОИТЬ WI-FI').exists:
                d(resourceId="com.android.systemui:id/back").click()
                sleep(2)
                if d(description="Настройки").exists:
                    d(description="Настройки").click()
                    sleep(5)

        if d(text="Подключено").exists:
            print(f"{NowDate()}  Сессия не убита")
            f.write(f"{NowDate()}  Сессия не убита\n")
            SendMessage(f"{devices_name} 🔥 {ssid}: Сессия не убита")
            err_name = 'Error: No kill session'
            check_err = 1
            return False

        if d(text="Без доступа к Интернету").exists or d(text="Нет подключения к Интернету").exists:
            print(f"{NowDate()}  ТД без доступа к Интернету")
            f.write(f"{NowDate()}  ТД без доступа к Интернету\n")
            SendMessage(f"{devices_name} 🔥 {ssid}: ТД без доступа к Интернету")
            check_err = 1
            err_name = 'Error: ТД без доступа в Интернет, на Идент не попасть'
            return False

        if d(text="Войти").exists() and d(resourceId="android:id/text1", text="MAC-адрес устройства").exists:
            d(resourceId="com.android.settings:id/button2").click()

    else:
        sleep(3)
        if d(text="Сохранено").exists:
            print(f"{NowDate()}  Нет ассоциации с ТД")
            f.write(f"{NowDate()}  Нет ассоциации с ТД\n")
            SendMessage(f"{devices_name} 🔥 {ssid}: Нет ассоциации с ТД")
            check_err = 1
            err_name = 'Error: No Association'
            return False

        else:
            print(f"{NowDate()}  SSID не найден")
            f.write(f"{NowDate()}  SSID не найден\n")
            SendMessage(f"{devices_name} 🔥 {ssid}: SSID не найден")
            check_err = 1
            err_name = 'Error: No SSID'
            return False
