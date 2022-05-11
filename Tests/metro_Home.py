def AvtoTest(ser, MAC, DevicesName):
    import uiautomator2 as u2
    from time import sleep
    import Functions.CheckInternet
    from Functions.DataName import NowDate
    from Functions.DataName import NowDateVideo
    from Functions.TelegramApi import SendMessage
    from Functions.TelegramApi import Send_screencast
    from Functions.TelegramApi import Send_File
    from Functions.LockDisplay import Lock

    ssid = '_P_metro'
    name_video = 'P_metro'
    p = NowDateVideo()
    d = u2.connect_usb(ser)
    flag = 5

    flag2 = 10
    f = open("logs/buttonClick.txt", 'w', encoding='utf-8')

    try:
        print(f"{NowDate()}  {DevicesName}: 📣Автотест запущен📱")
        f.write(f"{NowDate()}  {DevicesName}: 📣Автотест запущен🚀\n")
        # Functions.TelegramApi.SendMessage(
        #     f"{DevicesName}: 📣Автотест запущен📱")  # Отправка сообщения в телеграмм канал
        if d.info.get('screenOn'):
            d.shell(
                'input keyevent 26')  # Проверка активности экрана. Если активен, то выключится перед началом теста
        Lock(d)  # Разблокировка экрана
        d.screenrecord(f"screencasts/{DevicesName}_{name_video}.mp4")  # Запуск записи экрана

        # -- Подключение к ssid
        d.shell("am start -a android.intent.action.VIEW  https://auth.wi-fi.ru/?segment=metro")
        sleep(5)
        # -- Нажатие на "Войти в интернет"
        while flag != 0:
            OpenSixtyMin = d(text='Войти на 60 минут')
            if OpenSixtyMin.exists:
                sleep(2)
                # кнопка находится но неактивна в течении 5 сек. Нужен кликабле
                OpenSixtyMin.click(2)
                print(f"{NowDate()}  Нажата кнопка 'Войти в интернет'")
                f.write(f"{NowDate()}  Нажата кнопка 'Войти в интернет'\n")
                sleep(3)
                break
            if flag == 1:
                print(f"{NowDate()}  Кнопка 'Войти в интернет' не найдена. Скрипт принудительно завершен ")
                f.write(f"{NowDate()}  Кнопка 'Войти в интернет' не найдена. Скрипт принудительно завершен \n")
                quit()
            else:
                flag -= 1
                sleep(3)
                continue
        # -- Прохождение рекламы
        ButtonX1 = d.xpath(
            '//*[@text="Авторизация Wi-Fi"]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[3]/android.view.View[1]')
        ButtonX2 = d.xpath(
            '//*[@text="Авторизация Wi-Fi"]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]')
        ButtonX3 = d.xpath('// *[ @ resource - id = "app"] / android.view.View[1]/android.view.View[3]')
        # d.xpath('//*[@text=""]')
        Next = d(text="Продолжить", className='android.widget.Button')
        Continue = d(text="Далее", className='android.widget.Button')

        for i in range(20):
            if Next.exists or Continue.exists:
                break
            if ButtonX1.exists:
                ButtonX1.click_exists(5)
                print(f"{NowDate()}  Нажат крестик вид №1")
                f.write(f"{NowDate()}  Нажат крестик вид №1\n")
                sleep(5)
            elif ButtonX2.exists:
                ButtonX2.click_exists(5)
                print(f"{NowDate()}  Нажат крестик вид №2")
                f.write(f"{NowDate()}  Нажат крестик вид №2\n")
                sleep(5)
            elif flag2 == 1:
                print(f"{NowDate()} Кнопка 'Далее или Продолжить' не найдена. Скрипт принудительно завершен ")
                f.write(f"{NowDate()} Кнопка 'Далее или Продолжить' не найдена. Скрипт принудительно завершен\n")
                SendMessage(f"{DevicesName}: 🔥 {ssid}: Автотест упал")
                quit()
            else:
                flag2 -= 1
                sleep(3)
                continue

        if Next.exists:
            Next.click(1)
            print(f"{NowDate()}  Нажата кнопка Продолжить")
            f.write(f"{NowDate()}  Нажата кнопка Продолжить\n")
        else:
            Continue = d(text="Далее", className='android.widget.Button')
            Continue.click()
            print(f"{NowDate()}  Нажата кнопка Далее")
            f.write(f"{NowDate()}  Нажата кнопка Далее\n")

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
                    d.click(987, 271) # redmi9 после смены масштаба
                print(f"{NowDate()}  Нажат крестик вид №2")
                f.write(f"{NowDate()}  Нажат крестик вид №2\n")
                sleep(5)
            elif ButtonX3.exists:
                ButtonX3.click_exists(5)
                print(f"{NowDate()}  Нажат крестик №5 на портале")
                f.write(f"{NowDate()}  Нажат крестик №5 на портале\n")
            elif flag2 == 1:
                print(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен ")
                f.write(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен \n")
                SendMessage(f"{DevicesName}: 🔴 {ssid}: Автотест упал")
                quit()
            else:
                flag2 -= 1
                sleep(5)
                continue

        # тут пока не трогал
        assert final_check.exists or final_check2.exists, f"{NowDate()}  Авторизация не пройдена.Не найдена кнопка на новостном портале"

        # -- На портале
        # Functions.CheckInternet.CheckInternet(d)
        if Functions.CheckInternet.CheckInternet(d):
            print(f"{NowDate()}  Доступ в интернет есть!")
            f.write(f"{NowDate()}  Доступ в интернет есть! \n")
        else:
            print(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен ")
            f.write(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен \n")
            SendMessage(f"{DevicesName}: 🔴 {ssid}: Автотест упал.Доступа в интернет нет!")
            quit()

        SendMessage(f"{DevicesName}: 📣 {ssid}: Автотест успешно пройден ✅ ")
        print(f"{NowDate()}  Автотест пройден ✅")
        f.write(f"{NowDate()}  Автотест пройден ✅ \n")

    except AssertionError:
        print(f"{NowDate()}  🔴 Автотест упал. Не найдена кнопка на новостном портале")
        f.write(f"{NowDate()}  🔴 Автотест упал. Не найдена кнопка на новостном портале\n")
        SendMessage(f"{DevicesName}: 🔴 {ssid}: Автотест упал")

    finally:
        sleep(2)
        d.press("home")
        d.screenrecord.stop()
        Send_screencast(f"screencasts/{DevicesName}_{name_video}.mp4", f'Скринкаст авторизация {DevicesName}\n{ssid}')
        d.shell('input keyevent 26')
        f.close()
        Send_File("logs/buttonClick.txt")
