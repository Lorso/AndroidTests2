def AvtoTest (ser, MAC, DevicesName):
    import uiautomator2 as u2
    from time import sleep
    import requests
    import Functions.CheckInternet
    from Functions.DataName import NowDate
    from Functions.TelegramApi import SendMessage
    from Functions.TelegramApi import Send_screencast
    from Functions.LockDisplay import Lock
    from Functions.Sumsung import Connect_WiFi
    from Functions.Browser import BrowserExit
    from Functions.Browser import SamsungExit
    from Functions.FindSsid import scroll

    with open("logs/buttonClick.txt", 'a', encoding='utf-8') as f:
        flagBrowser = 0
        ssid = '_P_cppk'
        name_video = 'P_cppk'
        d = u2.connect_usb(ser)
        flag = 5
        flag2 = 10
        f = open("logs/buttonClick.txt", 'w', encoding='utf-8')

        try:
            print(f"{NowDate()}  {DevicesName}: 📣 {ssid}:  Автотест запущен📱")
            f.write(f"{NowDate()}  {DevicesName}: 📣 {ssid}:  Автотест запущен🚀\n")
            # Functions.TelegramApi.SendMessage(
            #     f"{DevicesName}: 📣 {ssid}:  Автотест запущен📱")  # Отправка сообщения в телеграмм канал
            if d.info.get('screenOn'):
                d.shell('input keyevent 26')  # Проверка активности экрана. Если активен, то выключится перед началом теста
            Lock(d)  # Разблокировка экрана

            if DevicesName == "Samsung A32":
                Connect_WiFi(d)
            else:
                d.shell("am start -n com.android.settings/com.android.settings.wifi.WifiSettings")  # Переход в настройки
                WIFI = d(text='Wi-Fi', className='android.widget.TextView')
                WIFI.click_exists(3)

            d.shell('svc wifi enable')  # Включение Wi-Fi

            # kargs = {'fps': 3, 'quality': 10, 'macro_block_size': 16, 'ffmpeg_params': ['-s', '384x800']}
            d.screenrecord(f"screencasts/{DevicesName}_{name_video}.mp4", )  # Запуск записи экрана
            sleep(5)

            # -- Подключение к SSID
            if DevicesName == "Samsung A32":
                SsidName = d.xpath(f'//*[@text="{ssid}"]')
                if SsidName.exists:
                    SsidName.click_exists(20)
                    sleep(7)
                    SsidName.click_exists(5)
                    print(f"{NowDate()}  SSID найден.Авторизация началась")
                    sleep(6)
                else:
                    scroll(d, DevicesName)
                    SsidName.click_exists(20)
                    sleep(7)
                    SsidName.click_exists(5)
                    print(f"{NowDate()}  SSID найден.Авторизация началась")
                    sleep(6)
            else:
                SsidName = d(text=f'{ssid}', className='android.widget.CheckedTextView')
                if SsidName.exists:
                    SsidName.click_exists(20)
                    print(f"{NowDate()}  SSID найден.Авторизация началась")
                    sleep(7)
                else:
                    scroll(d, DevicesName)
                    sleep(3)
                    SsidName.click_exists(20)
                    print(f"{NowDate()}  SSID найден.Авторизация началась")
                    sleep(7)

            # -- Проверка взлёта кептива
            if DevicesName == "Samsung A32":
                Captive = d.xpath('//*[@resource-id="android:id/action_bar"]/android.widget.LinearLayout[1]')
            else:
                Captive = d(text="Подключаться автоматически")

            if Captive.exists:
                print(f"{NowDate()}  Кептив открылся")
                f.write(f"{NowDate()}  Кептив открылся\n")
            else:
                print(f"{NowDate()}  Кептив не отработал.")
                f.write(f"{NowDate()}  Кептив не отработал.\n")

            # -- Подключение к ssid
            d.shell("am start -a android.intent.action.VIEW  http://gowifi.ru")
            print(f"{NowDate()}  Авторизация через браузер")
            f.write(f"{NowDate()}  Авторизация через браузер\n")
            sleep(5)

            # -- Нажатие на "Войти в интернет"
            while flag != 0:
                OpenSixtyMin = d(text='Войти в Интернет')
                if OpenSixtyMin.exists:
                    sleep(2)
                    # кнопка находится но неактивна в течении 5 сек. Нужен кликабле
                    OpenSixtyMin.click(2)
                    print(f"{NowDate()}  Нажата кнопка 'Войти в Интернет'")
                    f.write(f"{NowDate()}  Нажата кнопка 'Войти в Интернет'\n")
                    sleep(6)
                    break
                if flag == 1:
                    print(f"{NowDate()}  Кнопка 'Войти в Интернет' не найдена. Скрипт принудительно завершен ")
                    f.write(f"{NowDate()}  Кнопка 'Войти в Интернет' не найдена. Скрипт принудительно завершен \n")
                    return
                else:
                    flag -= 1
                    sleep(3)
                    continue
            # -- Прохождение рекламы
            ButtonX1 = d.xpath(
                '//*[@text="Авторизация Wi-Fi"]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[3]/android.view.View[1]')
            ButtonX2 = d.xpath(
                '//*[@text="Авторизация Wi-Fi"]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]')
            ButtonX3 = d.xpath('// *[ @ resource - id = "app"] / android.view.View[1] / android.view.View[3]')

            sleep(5)
            final_check2 = d(description="cabinet.wi-fi")
            final_check = d.xpath('//*[@text="cabinet.wi-fi"]')
            while not (final_check.exists or final_check2.exists):
                # print(final_check.exists)
                # print(final_check2.exists)
                if ButtonX1.exists:
                    ButtonX1.click_exists(5)
                    print(f"{NowDate()}  Нажат крестик вид №1")
                    f.write(f"{NowDate()}  Нажат крестик вид №1\n")
                    sleep(5)
                elif ButtonX2.exists:
                    if DevicesName == "XiaomiMi9":
                        # ButtonX2.click_exists(5)
                        d.click(954, 354)
                    else:
                        d.click(962, 313)
                    print(f"{NowDate()}  Нажат крестик вид №2")
                    f.write(f"{NowDate()}  Нажат крестик вид №2\n")
                    sleep(5)
                # elif ButtonX3.exists:
                #     ButtonX3.click_exists(5)
                #     print(f"{NowDate()}  Нажат крестик №5 на портале")
                #     f.write(f"{NowDate()}  Нажат крестик №5 на портале\n")
                elif flag2 == 1:
                    print(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен ")
                    f.write(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен \n")
                    SendMessage(f"{DevicesName}: 🔴 {ssid}: Автотест упал")
                    return
                else:
                    flag2 -= 1
                    sleep(5)
                    continue

            # тут пока не трогал
            assert final_check.exists or final_check2.exists or SsidName.exists, f"{NowDate()}  Авторизация не пройдена.Не найдена кнопка на новостном портале"
            if final_check.exists or final_check2.exists:
                print(f"{NowDate()}  Иконка на портале найдена")
                f.write(f"{NowDate()}  Иконка на портале найдена\n")
            else:
                print(f"{NowDate()}  Иконка на портале не найдена")
                f.write(f"{NowDate()}  Иконка на портале не найдена\n")

            # -- На портале
            flagBrowser = 1
            if Functions.CheckInternet.CheckInternet(d, DevicesName):
                print(f"{NowDate()}  Доступ в интернет есть!")
                f.write(f"{NowDate()}  Доступ в интернет есть! \n")
            else:
                print(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен ")
                f.write(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен \n")
                SendMessage(f"{DevicesName}: 🔴 {ssid}: Автотест упал.Доступа в интернет нет!")
                return

            SendMessage(f"{DevicesName}: 📣 {ssid}: Автотест успешно пройден ✅ ")
            print(f"{NowDate()}  Автотест пройден ✅")
            f.write(f"{NowDate()}  Автотест пройден ✅ \n")

        except AssertionError:
            print(f"{NowDate()}  🔴 Автотест упал. Не найдена кнопка на новостном портале")
            f.write(f"{NowDate()}  🔴 Автотест упал. Не найдена кнопка на новостном портале\n")
            SendMessage(f"{DevicesName}: 🔴 {ssid}: Автотест упал")

        finally:
            if flagBrowser == 0:
                if DevicesName == "Samsung A32":
                    SamsungExit(d)
                else:
                    BrowserExit(d)
            sleep(2)
            d.screenrecord.stop()
            d.press("home")
            sleep(2)
            d.shell('svc wifi disable')
            d.shell('input keyevent 26')
            requests.get(f"http://sae.msk.vmet.ro/v1/drop/mac/{MAC}")
            print(f"{NowDate()}  Сессия убита ✅")
            print(f"_____________________________________________________________")
            f.write(f"{NowDate()}  Сессия убита ✅\n")
            sleep(2)
            Send_screencast(f"screencasts/{DevicesName}_{name_video}.mp4", f'Скринкаст авторизация {DevicesName}\n{ssid}')
            sleep(10)
