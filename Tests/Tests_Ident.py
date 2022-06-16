def AutoTest(ser, mac, devices_name, ssid, name_video):
    import uiautomator2 as u2
    from time import sleep
    from time import time
    from datetime import datetime
    import requests
    import Functions.CheckInternet

    from Functions.OnePlus9R.wificonnect import wificonnect
    from Functions.OnePlus9R.identcall import identcall
    from Functions.OnePlus9R.identsms import identsms
    from Functions.OnePlus9R.resetwifi import resetwifi

    from Functions.DataName import NowDate
    from Functions.TelegramApi import SendMessage2
    from Functions.TelegramApi import Send_screencast2
    from Functions.LockDisplay import Lock
    from Functions.Sumsung import Connect_WiFi
    from Functions.pgconnect import addResult
    from clickhouse_driver import Client



    time_start = time()

    # БД
    client = Client(host='10.1.240.77', port="9000")

    global id
    # id = 7 # Samsung S20 FE
    # id = 6  # Xiaomi 10t pro
    #id = 5  # Xiaomi SE9
    id = 4 # Oneplus 9R
    #id = 3 #Xiaomi 9 pro

    LV = str(client.execute('SELECT LAST_VALUE(ntest) FROM devdb1.auto_tests'))
    global ntest
    ntest = int((LV.partition('(')[2]).partition(',')[0]) + 1
    global dt
    dt = datetime.now().replace(microsecond=0)
    global type
    type = 'Ident'
    global err_name
    err_name = ''


    d = u2.connect_usb(ser) #Подключение телефона к автоматору

    global succes
    succes = 0 # Если доступ в интернет будет после идентификации изменится на 1
    global check_err
    check_err = 0 #Если найдена будет известная ошибка, изменится на 1



    with open("logs/buttonClick.txt", 'a', encoding='utf-8') as f:
        try:
            print(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Тест запущен📱")
            f.write(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Тест запущен🚀\n")

            d.unlock()
            sleep(5)

            d.shell("am start -n com.android.settings/com.android.settings.wifi.WifiSettings")  # Переход в настр
            wifi = d.xpath('//*[@text="Wi-Fi"]')
            wifi.click_exists(3)

            d.shell('svc wifi enable')  # Включение Wi-Fi
            d.screenrecord(f"screencasts/{devices_name}_{name_video}.mp4")  # Запуск записи экрана

            # -- Подключение к SSID

            #########################################################
            if devices_name == 'OnePlus 9R':
                d.press("home")
                sleep(1)
                d(text="Сообщения").click()
                sleep(1)
                d.press('home')
                sleep(1)
                d(text="Телефон").click()
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
                        sleep(1)
                        if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                            d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
                            sleep(10)
                        sleep(3)
                        if d(resourceId="android:id/title", text="Конфиденциальность").exists():
                            d(resourceId="android:id/title", text="Конфиденциальность").click()
                        sleep(2)
                        if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                            d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
                            sleep(10)
                        sleep(3)
                        if d(resourceId="android:id/title", text="Конфиденциальность").exists():
                            d(resourceId="android:id/title", text="Конфиденциальность").click()
                        sleep(1)
                        if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                            d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
                            sleep(10)
                        sleep(2)
                        if d(text='НАСТРОИТЬ WI-FI').exists:
                            print(f"{NowDate()}  Открылась заглушка")
                            f.write(f"{NowDate()}  Открылась заглушка\n")
                            d(resourceId="com.android.systemui:id/back").click()
                            sleep(2)
                            if d(description="Настройки").exists:
                                d(description="Настройки").click()
                                sleep(5)
                        sleep(12)

                    if d(text="Подключено").exists:
                        print(f"{NowDate()}  Сессия не убита")
                        f.write(f"{NowDate()}  Сессия не убита\n")
                        SendMessage2(f"{devices_name} 🔥 {ssid}: Сессия не убита")
                        err_name = 'Error: No kill session'
                        check_err = 1
                        return False

                    if d(text="Без доступа к Интернету").exists or d(text="Нет подключения к Интернету").exists:
                        print(f"{NowDate()}  ТД без доступа к Интернету")
                        f.write(f"{NowDate()}  ТД без доступа к Интернету\n")
                        SendMessage2(f"{devices_name} 🔥 {ssid}: ТД без доступа к Интернету")
                        check_err = 1
                        err_name = 'Error: ТД без доступа в Интернет, на Идент не попасть'
                        return False

                    if d(text="Войти").exists() and d(resourceId="android:id/text1",
                                                      text="MAC-адрес устройства").exists:
                        d(resourceId="com.android.settings:id/button2").click()

                else:
                    sleep(3)
                    if d(text="Сохранено").exists:
                        print(f"{NowDate()}  Нет ассоциации с ТД")
                        f.write(f"{NowDate()}  Нет ассоциации с ТД\n")
                        SendMessage2(f"{devices_name} 🔥 {ssid}: Нет ассоциации с ТД")
                        check_err = 1
                        err_name = 'Error: No Association'
                        return False

                    else:
                        print(f"{NowDate()}  SSID не найден")
                        f.write(f"{NowDate()}  SSID не найден\n")
                        SendMessage2(f"{devices_name} 🔥 {ssid}: SSID не найден")
                        check_err = 1
                        err_name = 'Error: No SSID'
                        return False

###############################################################################
            #УСТРОЙСТВА И ИХ ПЕРЕМЕННЫЕ

            if devices_name == 'OnePlus 9R':
                captive = d.xpath('//*[@content-desc="Ещё"]')

            if captive.exists:
                print(f"{NowDate()}  Кептив открылся")
                f.write(f"{NowDate()}  Кептив открылся\n")
            else:
                print(f"{NowDate()}  Captive не отработал")
                f.write(f"{NowDate()}  Captive не отработал\n")
                SendMessage2(f"{devices_name} 🔥 {ssid}: Captive не отработал")
                check_err = 1
                err_name = 'Error: No Captive'
                return False

            #Страница идентификации
            number_check = d(text="НОМЕР ТЕЛЕФОНА")  # Кнопка номер телефона
            callme = d(text="ПОЗВОНИТЕ МНЕ") #Кнопка позвоните мне по ЗВОНКУ
            getsms = d(text='ПОЛУЧИТЬ КОД') #Получить код по СМС
            sim = '79067810391' #Симка



            # Чекеры финала
            final_check1 = d.xpath('//*[@text="WI-FI.RU"]') #Если кэптив не закрылся
            final_check2 = d.xpath('//*[@text="Chrome"]') #Если кептив закрылся
            final_check3 = d.xpath('//*[@content-desc="wi-fi"]')
            #Если реклама после идента
            button_x1 = d.xpath(
                '//*[@text="Авторизация Wi-Fi"]/android.view.View[2]/android.view.View[1]/android.view.View[3]/android.view.View[1]')
            button_x2 = d.xpath(
                '//*[@text="Авторизация Wi-Fi"]/android.view.View[2]/android.view.View[1]/android.view.View[1]')
            # button_x2 = d.xpath('//*/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]')
            button_x3 = d.xpath('//*[@text="Регистрация"]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]')

            # Идентификация
            while not (final_check1.exists or final_check2.exists or final_check3.exists or button_x1.exists or button_x2.exists or button_x3.exists):
                sleep(15)
                if number_check.exists:
                    print(f"{NowDate()}  Страница идентификации загружена")
                    f.write(f"{NowDate()}  Страница идентификации загружена\n")
                    number_check.click()  # Нажата кнопка Номер телефона
                    print(f"{NowDate()}  Клик по кнопке НОМЕР ТЕЛЕФОНА")
                    f.write(f"{NowDate()}  Клик по кнопке НОМЕР ТЕЛЕФОНА\n")
                    sleep(3)

                    # Ветка по звонку
                    callme.wait(True, 10)
                    if callme.exists():
                        type = 'CALL'
                        print(f"{NowDate()}  Идентификация по звонку")
                        f.write(f"{NowDate()}  Идентификация по звонку\n")
                        d.xpath(
                            '//*[@resource-id="call-phone"]/android.view.View[1]').click()  # Нажато поле ввода телефона
                        print(f"{NowDate()}  Клик по полю ввода")
                        f.write(f"{NowDate()}  Клик по полю ввода\n")
                        sleep(3)
                        d.send_keys(sim, clear=True)  # Вбит номер телефона
                        print(f"{NowDate()}  Ввод номера")
                        f.write(f"{NowDate()}  Ввод номера\n")
                        sleep(3)
                        callme.click()  # Нажата кнопка Позвоните мне
                        print(f"{NowDate()}  Клик позвоните мне")
                        f.write(f"{NowDate()}  Клик позвоните мне\n")
                        sleep(5)
                        if d(text='При подтверждении номера произошла ошибка').exists:
                            print(f"{NowDate()}  При подтверждении номера произошла ошибка")
                            f.write(f"{NowDate()}  При подтверждении номера произошла ошибка\n")
                            SendMessage2(f"{devices_name} 🔥 {ssid}: При подтверждении номера произошла ошибка")
                            check_err = 1
                            err_name = 'Error: При подтверждении номера произошла ошибка'
                            return False

                        sleep(35)
                        d.swipe(0.284, 0.025, 0.575, 0.743)  # Свайп шторки для проверки пропущенного

                        if d.xpath('//*[@text="Телефон"]').exists:  # Проверка пропущенного звонка
                            sleep(3)
                            print(f"{NowDate()}  Звонок поступил")
                            f.write(f"{NowDate()}  Звонок поступил\n")
                            d.xpath('//*[@text="Телефон"]').click()  # переход в журнал
                            sleep(1)
                            d.long_click(0.712, 0.2)  # высветится номер в отдельном окне
                            sleep(2)
                            # Редакт номера
                            d(resourceId="com.google.android.dialer:id/new_call_log_popup_menu_action_item_text",
                              text="Изменить номер и позвонить").click()  # скопируется номер
                            sleep(4)
                            #### Вытащит последние 4 цифры
                            if d(text='+7 985 012-13-22').exists:
                                d.double_click(0.298, 0.972)
                                time.sleep(1)
                                d.click(0.723, 0.969)
                                time.sleep(1)
                                d.click(0.057, 0.458)
                                time.sleep(1)
                                d.click(0.557, 0.316)
                                time.sleep(1)
                                d.send_keys("1322", clear=True)
                                # Вставка когда
                            if d(text='+7 985 012-21-16').exists:
                                d.double_click(0.298, 0.972)
                                time.sleep(1)
                                d.click(0.723, 0.969)
                                time.sleep(1)
                                d.click(0.057, 0.458)
                                time.sleep(1)
                                d.click(0.557, 0.316)
                                time.sleep(1)
                                d.send_keys("2116", clear=True)

                            if d(text='+7 985 012-21-74').exists:
                                d.double_click(0.298, 0.972)
                                time.sleep(1)
                                d.click(0.723, 0.969)
                                time.sleep(1)
                                d.click(0.057, 0.458)
                                time.sleep(1)
                                d.click(0.557, 0.316)
                                time.sleep(1)
                                d.send_keys("2174", clear=True)

                            else:
                                d.click(0.607, 0.484)
                                sleep(1)
                                d.click(0.931, 0.486)
                                sleep(1)
                                for i in range(5):
                                    d.double_click(0.931, 0.486)
                                    sleep(1)
                                d.click(0.517, 0.481)
                                sleep(1)
                                d.click(0.931, 0.486)
                                sleep(1)
                                d.double_click(0.489, 0.476)
                            d(resourceId="android:id/floating_toolbar_menu_item_text", text="Копировать").click()
                            d.double_click(0.298, 0.972)
                            sleep(1)
                            d.click(0.723, 0.969)
                            sleep(1)
                            d.click(0.057, 0.458)
                            sleep(1)
                            d.long_click(0.557, 0.316)
                            d(resourceId="android:id/floating_toolbar_menu_item_text",
                              text="Вставить").click()  # Вставка кода
                            print(f"{NowDate()}  Код Введен")
                            f.write(f"{NowDate()}  Код Введен\n")
                            #######
                            sleep(5)
                            if d.xpath('//*[@text="ВОЙТИ В ИНТЕРНЕТ"]').exists:
                                d.xpath('//*[@text="ВОЙТИ В ИНТЕРНЕТ"]').click()
                                print(f"{NowDate()}  Клик «ВОЙТИ В ИНТЕРНЕТ")
                                f.write(f"{NowDate()}  Клик «ВОЙТИ В ИНТЕРНЕТ\n")
                                sleep(15)
                            else:
                                if d.xpath('//*[@text="Неправильно введён код"]').exists:
                                    check_err = 1
                                    print(f"{NowDate()}  Неправильно введён код")
                                    f.write(f"{NowDate()}  Неправильно введён код\n")
                                    SendMessage2(f"{devices_name}: 🔥 {ssid} Неправильно введён код")
                                    err_name = 'Error: Incorrect Code'
                                    return False
                                else:
                                    check_err = 1
                                    print(f"{NowDate()}  Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась")
                                    f.write(f"{NowDate()}  Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась\n")
                                    SendMessage2(f"{devices_name}: 🔥 {ssid} Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась")
                                    err_name = 'Error: Не прогрузилась кнопка ВОЙТИ В ИНТЕРНЕТ'
                                    return False

                            if d.xpath('//*[@text="Регистрация"]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').exists:
                                d.xpath(
                                    '//*[@text="Регистрация"]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').click()
                                print(f"{NowDate()}  Нажат крестик Рекламы")
                                f.write(f"{NowDate()}  Нажат крестик Рекламы\n")

                            if (final_check1.exists or final_check2.exists or final_check3.exists or button_x1.exists or button_x2.exists or button_x3.exists):
                                print(f"{NowDate()}  Идентификация прошла успешно")
                                f.write(f"{NowDate()}  Идентификация прошла успешно\n")
                                if d.xpath('//*[@content-desc="Ещё"]').exists:  # закрытие кэптива
                                    d.xpath('//*[@content-desc="Ещё"]').click()
                                    sleep(1)
                                    d.xpath(
                                        '//android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()
                            else:
                                if d(text='Войти в Интернет'):
                                    check_err = 1
                                    print(f"{NowDate()}  Вместо портала, страница авторизации")
                                    f.write(f"{NowDate()}  Вместо портала, страница авторизации\n")
                                    SendMessage2(f"{devices_name} 🔥 {ssid}: Вместо портала, страница авторизации")
                                    sleep(12)
                                    err_name = 'Error: Вместо портала, страница авторизации'
                                    return False
                                else:
                                    check_err = 1
                                    print(f"{NowDate()}  Портал не загрузился")
                                    f.write(f"{NowDate()}  Портал не загрузился\n")
                                    SendMessage2(f"{devices_name} 🔥 {ssid}: Портал не загрузился")
                                    sleep(12)
                                    err_name = 'Error: Портал не прогрузился'
                                    return False

                        else:
                            check_err = 1
                            print(f"{NowDate()}  Звонок не поступил")
                            f.write(f"{NowDate()}  Звонок не поступил\n")
                            SendMessage2(f"{devices_name}: 🔥 {ssid} Звонок не поступил")
                            err_name = 'Error: No Call'
                            return False

                    # Ветка по СМС
                    getsms.wait(True, 10)
                    if getsms.exists:
                        type = 'SMS'
                        print(f"{NowDate()}  Идентификация по SMS")
                        f.write(f"{NowDate()}  Идентификация по SMS\n")
                        d.xpath('//*[@resource-id="phone_form"]/android.view.View[1]').click()  # нажато на поле ввода
                        print(f"{NowDate()}  Клик по полю ввода")
                        f.write(f"{NowDate()}  Клик по полю ввода\n")
                        sleep(3)
                        d.send_keys(sim, clear=True)  # Вбит номер телефона
                        print(f"{NowDate()}  Ввод номера")
                        f.write(f"{NowDate()}  Ввод номера\n")
                        sleep(3)
                        getsms.click()  # Клик по получить код
                        print(f"{NowDate()}  Нажата кнока получит КОД")
                        f.write(f"{NowDate()}  Нажата кнока получит КОД\n")
                        sleep(20)
                        d.swipe(0.284, 0.025, 0.575, 0.743)  # Свайп шторки для проверки пропущенного

                        if d.xpath('//*[@text="Сообщения"]').exists:  # Проверка полученного СМС
                            sleep(3)
                            print(f"{NowDate()}  SMS пришла")
                            f.write(f"{NowDate()}  SMS пришла\n")
                            d.xpath('//*[@text="Сообщения"]').click()  # переход в СМС
                            sleep(5)
                            d(text='DIT_MosWiFi').wait(5)
                            if d(text='DIT_MosWiFi').exists:  # откого смс, разные высоты
                                print(f"{NowDate()}  SMS DIT")
                                f.write(f"{NowDate()}  SMS DIT\n")
                                d.long_click(0.402, 0.772)  # Выделение смс
                            else:
                                print(f"{NowDate()}  SMS MT")
                                f.write(f"{NowDate()}  SMS MT\n")
                                d.long_click(0.329, 0.778)
                            sleep(5)
                            d(resourceId="com.google.android.apps.messaging:id/copy_text").click()  # Скопировано смс
                            sleep(1)
                            d.click(0.723, 0.969)
                            sleep(1)
                            d.click(0.057, 0.458)
                            sleep(2)
                            d.long_click(0.557, 0.316)
                            d(resourceId="android:id/floating_toolbar_menu_item_text",
                              text="Вставить").click()  # Вставка кода
                            print(f"{NowDate()}  Код Введен")
                            f.write(f"{NowDate()}  Код Введен\n")
                            sleep(5)

                            if d.xpath('//*[@text="Неправильно введён код"]').exists: # Если выделил выше
                                d(resourceId="com.android.systemui:id/recent_apps").click()
                                sleep(1)
                                d.xpath('//*[@content-desc="Сообщения"]/android.view.View[1]').click()
                                sleep(2)
                                d.long_click(0.519, 0.838)  # Выделение смс
                                sleep(5)
                                d(resourceId="com.google.android.apps.messaging:id/copy_text").click()  # Скопировано смс
                                sleep(1)
                                d.click(0.723, 0.969)
                                sleep(1)
                                d.click(0.057, 0.458)
                                sleep(2)
                                d.long_click(0.557, 0.316)
                                d(resourceId="android:id/floating_toolbar_menu_item_text",
                                  text="Вставить").click()  # Вставка кода
                                print(f"{NowDate()}  Код Введен")
                                f.write(f"{NowDate()}  Код Введен\n")
                                sleep(5)

                            if d.xpath('//*[@text="ВОЙТИ В ИНТЕРНЕТ"]').exists:
                                d.xpath('//*[@text="ВОЙТИ В ИНТЕРНЕТ"]').click()
                                print(f"{NowDate()}  Клик «ВОЙТИ В ИНТЕРНЕТ")
                                f.write(f"{NowDate()}  Клик «ВОЙТИ В ИНТЕРНЕТ\n")
                                sleep(15)
                            else:
                                if d.xpath('//*[@text="Неправильно введён код"]').exists:
                                    check_err = 1
                                    print(f"{NowDate()}  Неправильно введён код")
                                    f.write(f"{NowDate()}  Неправильно введён код\n")
                                    SendMessage2(f"{devices_name}: 🔥 {ssid} Неправильно введён код")
                                    err_name = 'Error: Incorrect Code'
                                    return False
                                else:
                                    check_err = 1
                                    print(f"{NowDate()}  Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась")
                                    f.write(f"{NowDate()}  Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась\n")
                                    SendMessage2(f"{devices_name}: 🔥 {ssid}Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась")
                                    err_name = 'Error: Не прогрузилась кнопка ВОЙТИ В ИНТЕРНЕТ'
                                    return False

                            if d.xpath('//*[@text="Регистрация"]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').exists:
                                d.xpath(
                                    '//*[@text="Регистрация"]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.TextView[1]').click()
                                print(f"{NowDate()}  Нажат крестик Рекламы")
                                f.write(f"{NowDate()}  Нажат крестик Рекламы\n")
                            if button_x3.exists:
                                button_x3.click()
                                print(f"{NowDate()}  Нажат крестик Рекламы")
                                f.write(f"{NowDate()}  Нажат крестик Рекламы\n")

                            sleep(20)
                            if (final_check1.exists or final_check2.exists or final_check3.exists or button_x1.exists or button_x2.exists or button_x3.exists):
                                print(f"{NowDate()}  Идентификация прошла успешно")
                                f.write(f"{NowDate()}  Идентификация прошла успешно\n")
                                if d.xpath('//*[@content-desc="Ещё"]').exists:  # Закрытие кэптива
                                    d.xpath('//*[@content-desc="Ещё"]').click()
                                    sleep(1)
                                    d.xpath(
                                        '//android.widget.ListView/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()
                            else:
                                if d(text='Войти в Интернет'):
                                    check_err = 1
                                    print(f"{NowDate()}  Вместо портала, страница авторизации")
                                    f.write(f"{NowDate()}  Вместо портала, страница авторизации\n")
                                    SendMessage2(f"{devices_name} 🔥 {ssid}: Вместо портала, страница авторизации")
                                    sleep(12)
                                    err_name = 'Error: Вместо портала, страница авторизации'
                                    return False
                                else:
                                    check_err = 1
                                    print(f"{NowDate()}  Портал не загрузился")
                                    f.write(f"{NowDate()}  Портал не загрузился\n")
                                    SendMessage2(f"{devices_name} 🔥 {ssid}: Портал не загрузился")
                                    sleep(12)
                                    err_name = 'Error: Портал не прогрузился'
                                    return False

                        else:
                            check_err = 1
                            print(f"{NowDate()}  SMS не пришла")
                            f.write(f"{NowDate()}  SMS не пришла\n")
                            SendMessage2(f"{devices_name}: 🔥 {ssid} SMS не пришла")
                            err_name = 'Error: No SMS'
                            return False

                else:
                    check_err = 1
                    print(f"{NowDate()}  Страница идентификации не загрузилась")
                    f.write(f"{NowDate()}  Страница идентификации не загрузилась\n")
                    SendMessage2(f"{devices_name} 🔥 {ssid}: Страница идентификации не загрузилась")
                    sleep(12)
                    err_name = 'Error: Страница идентификации не загрузилась'
                    return False

            if Functions.CheckInternet.CheckInternet(d, devices_name):
                print(f"{NowDate()}  Доступ в интернет есть!")
                f.write(f"{NowDate()}  Доступ в интернет есть! \n")
                succes = 1
            else:
                print("\033[31m{}\033[0m".format(
                    f"{NowDate()} Доступа в интернет нет. Скрипт завершен "))
                f.write(f"{NowDate()} Доступа в интернет нет. Скрипт завершен \n")
                SendMessage2(f"{devices_name} 🔥 {ssid}: Доступа в интернет нет")
                check_err = 1
                err_name = 'Error: No access Internet'
                return False



            # -- Финиш, если дойдет, тест пройден успешно
            SendMessage2(f"{devices_name}: 📣 {ssid}: Идент Тест успешно пройден ✅ ")
            print("\033[32m{}\033[0m".format(f"{NowDate()}  Идент Тест пройден ✅"))
            f.write(f"{NowDate()}  Идент Тест пройден ✅ \n")
            # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
            # addResult(ssid, devices_name, 0, "PASS", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
            return True

        finally:
            if succes==0 and check_err==0:
                print(f"{NowDate()}  Unknown Error")
                f.write(f"{NowDate()}  Unknown Error\n")
                SendMessage2(f"{devices_name} 🔥 {ssid}: Unknown Error")
                check_err =1
                err_name = 'Error: Unknown'


            sleep(2)
            if d.screenrecord.stop() == "False":
                print("False")
                print(d.screenrecord.stop())

            resetwifi(d)


            print(f"{NowDate()}  Сеть забыта ✅")
            f.write(f"{NowDate()}  Сеть забыта ✅\n")

            ####################
            d.press("home")
            sleep(2)
            d.shell('svc wifi disable')
            d.shell('input keyevent 26')
            requests.get(
                f"http://userhd.msk.vmet.ro/id/deidentify/{mac}")
            requests.get(
                f"http://sae.msk.vmet.ro/v1/drop/mac/{mac}")

            print(f"{NowDate()}  Сессия и Идент убиты ✅")
            f.write(f"{NowDate()}  Сессия и Идент убиты ✅\n")
            time_finish = time() - time_start
            print(f"Время работы скрипта: {round(time_finish, 2)} сек")
            if check_err == 1:
                Send_screencast2(f"screencasts/{devices_name}_{name_video}.mp4", f'Идентификация {devices_name}\n{ssid}')
            print(f"_________________________________________________________")
            f.write(f"{id, ntest, dt, ssid, type, check_err, err_name}\n")
            f.write(f"_______________________________________________________\n")

            #В БД
            print(id, ntest, dt, ssid, type, check_err, err_name)
            client.execute(
                'INSERT INTO devdb1.auto_tests (id, ntest, dt, ssid, type, err_flags, err_name) VALUES',
                [{'id': id, 'ntest': ntest, 'dt': dt, 'ssid': ssid, 'type': type, 'err_flags': check_err,
                  'err_name': err_name}])
            if type=='SMS':
                sleep(167)
            else:
                sleep(10)





