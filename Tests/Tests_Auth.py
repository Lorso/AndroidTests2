
def AutoTest(ser, mac, devices_name, ssid, name_video):
    import uiautomator2 as u2
    from time import sleep
    from time import time
    from datetime import datetime
    import requests
    from Functions.Yandex import sendYandexScreencast
    import Functions.CheckInternet
    from Functions.ClearCookie import XiaomiCl
    from Functions.DataName import NowDate
    from Functions.TelegramApi import SendMessage
    from Functions.TelegramApi import Send_screencast
    from Functions.LockDisplay import Lock
    from Functions.Sumsung import Connect_WiFi
    from Functions.pgconnect import addResult
    from clickhouse_driver import Client



    time_start = time()

    # БД
    client = Client(host='10.1.240.77', port="9000")

    global id
    # id = 6  # Xiaomi 10t pro
    id = 5  # Xiaomi SE9
    #id = 4 # Oneplus 9R
    #id = 3 #Xiaomi 9 pro

    LV = str(client.execute('SELECT LAST_VALUE(ntest) FROM devdb1.auto_tests'))
    global ntest
    ntest = int((LV.partition('(')[2]).partition(',')[0]) + 1
    global dt
    dt = datetime.now().replace(microsecond=0)
    global type
    type = 'Auth'

    d = u2.connect_usb(ser)
    flag = 6
    flag2 = 15
    err400 = False
    check_err = 0
    success = 0
    global err_name
    err_name = ''
    #imTestX = "ScreeX.jpg"

    with open("logs/buttonClick.txt", 'a', encoding='utf-8') as f:
        try:
            print(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Тест запущен📱")
            f.write(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Тест запущен🚀\n")

            if d.info.get('screenOn'):
                d.shell('input keyevent 26')  # Проверка активности экрана. Если вкл, то выкл перед началом теста
            Lock(d)  # Разблокировка экрана

            # Уберет всплывашку от USB подключения для сяоми
            if d(resourceId="miui:id/alertTitle").exists:
                d.click(0.488, 0.902)

            # SAMSUNG
            if devices_name == "Samsung A32":
                Connect_WiFi(d)
            else:
                d.shell("am start -n com.android.settings/com.android.settings.wifi.WifiSettings")  # Переход в настр
                wifi = d(text='Wi-Fi', className='android.widget.TextView')
                wifi.click_exists(3)

            d.shell('svc wifi enable')  # Включение Wi-Fi
            d.screenrecord(f"screencasts/{devices_name}_{name_video}.mp4")  # Запуск записи экрана

            # -- Подключение к SSID
            if devices_name == "Samsung A32":
                ssid_name = d(resourceId="com.android.settings:id/title", text=f"{ssid}")
                ssid_name.wait(True, 60)
                if ssid_name.exists:
                    ssid_name.click_gone(5, 5)
                    sleep(6)
                else:
                    ssid_name.click_gone(5, 5)
                    sleep(6)
            ###################################
            if devices_name == 'OnePlus 9R':
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
                    while d(text='Регистрация в сети').exists:
                        if d(resourceId="android:id/title", text="Дополнительно").exists():
                            d(resourceId="android:id/title", text="Дополнительно").click()
                        sleep(3)
                        if d(resourceId="android:id/title", text="Конфиденциальность").exists():
                            d(resourceId="android:id/title", text="Конфиденциальность").click()
                        sleep(3)
                        if d(resourceId="android:id/text1", text="MAC-адрес устройства").exists():
                            d(resourceId="android:id/text1", text="MAC-адрес устройства").click()
                            sleep(10)
                else:
                    print(f"{NowDate()}  SSID не найден")
                    f.write(f"{NowDate()}  SSID не найден\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}:🔥 SSID не найден")
                    check_err = 1
                    return False
#####################################################################################################################
            # ОСНОВА, BASE, XIAOMI SE
            if devices_name == 'XiaomiSE':
                if d(resourceId="miui:id/buttonPanel").exists:
                    d(resourceId="miui:id/buttonPanel").click_gone()
                ssid_name = d(text=f'{ssid}', className='android.widget.CheckedTextView')
                if ssid == 'sas': # для особенного сида
                    # d.shell("am start -n com.steinwurf.adbjoinwifi/.MainActivity -e ssid '" + ssid + "'")
                    # sleep(10)
                    # d.app_start("com.android.settings", ".Settings$WifiSettings2Activity")
                    # sleep(5)
                    # d(resourceId="com.android.systemui:id/halo").click()
                    # sleep(2)
                    # d(resourceId="com.miui.home:id/icon_icon", description="Настройки").click()
                    # sleep(2)
                    # d.xpath(
                    #     '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]').click()
                    # if ssid_name.exists:
                    #     ssid_name.click_gone(5, 5)
                    # sleep(8)
                    ssid_name.wait(True, 40)
                    if ssid_name.exists:
                        ssid_name.click_gone(5, 5)
                        sleep(8)
                    else:
                        d.shell('svc wifi disable')
                        sleep(2)
                        d.shell('svc wifi enable')
                        ssid_name.wait(True, 20)
                        ssid_name.click_gone(5, 5)
                        sleep(8)
                else:
                    ssid_name.wait(True, 20)
                    if ssid_name.exists:
                        ssid_name.click_gone(5, 5)
                        sleep(10)
                    else:
                        # d(scrollable=True).scroll.to(text=f"{ssid}")
                        d(scrollable=True).scroll.vert.forward(steps=200) # скролл для поиска сида
                        sleep(5)
                        if ssid_name.exists:
                            ssid_name.click_gone(5, 5)
                            sleep(10)
                        else:

                            # d.shell(
                            #     "am start -n com.steinwurf.adbjoinwifi/.MainActivity -e ssid '" + ssid + "'")
                            # sleep(5)
                            # if d(text="Разрешить сейчас").exists:
                            #     d(resourceId="android:id/button1").click()
                            #     d(text="Разрешить сейчас").click()
                            #
                            # d.shell("am start -n com.android.settings/com.android.settings.wifi.WifiSettings")
                            # sleep(2)
                            # d.shell("am force-stop com.steinwurf.adbjoinwifi")  # Отключения АДБджоина

                            sleep(1)
                            d(scrollable=True).scroll.vert.backward(steps=200)
                            ssid_name.wait(True, 20)
                            if ssid_name.exists:
                                ssid_name.click_gone(5, 5)

                            else:
                                print("\033[31m{}\033[0m".format(f"{NowDate()}  SSID не найден.Тест завершен."))
                                f.write(f"{NowDate()}  SSID не найден.Тест завершен.\n")
                                SendMessage(f"{devices_name}: ⛔ {ssid}: SSID не найден")
                                check_err = 1
                                err_name = 'Error: No SSID'
                                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                                # addResult(ssid, devices_name, 3, "SSID not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                                return False


                            sleep(8)




            # -- Проверка не убитой сессии
            if devices_name == 'OnePlus 9R':
                check_connect = d(text="Подключено")
                check_connect2 = d(text='Сохранено')
                check_connect3 = d(text='Подтвердите подключение')
            if devices_name == 'XiaomiSE':
                check_connect = d.xpath('//*[@text="Подключено"]')
                check_connect2 = d(text='Сохранено')
                check_connect3 = d(text='Подтвердите подключение')

            if check_connect.exists and ssid != "_P_ttk_hospitals":
                if Functions.CheckInternet.CheckInternet(d, devices_name):
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен."))
                    f.write(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен.\n")
                    SendMessage(f"{devices_name}: ⛔ {ssid}: Сессия не убита")
                    check_err = 1
                    err_name = 'Error: No kill session'
                    return False



                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # err 0 - не баг \ 900 - ошибка 900 \ 100 - ошибка 100\
                    # addResult(ssid, devices_name, 2, "Active session", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")

                else:
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Кептив не отработал.Тест завершен."))
                    f.write(f"{NowDate()}  Кептив не отработал.Тест завершен.\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Тест упал")
                    check_err = 1
                    err_name = 'Error: No Captive'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Captive not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
            if check_connect2.exists:
                print("\033[31m{}\033[0m".format(f"{NowDate()}  Нет ассоциации с ТД"))
                f.write(f"{NowDate()}  Нет ассоциации с ТД\n")
                SendMessage(f"{devices_name}: ⛔ {ssid}: Нет ассоциации с ТД")
                check_err = 1
                err_name = 'Error: No Association'
                return False
            if check_connect3.exists:
                print(f"{NowDate()}  ТД без доступа к Интернету")
                f.write(f"{NowDate()}  ТД без доступа к Интернету\n")
                SendMessage(f"{devices_name} 🔥 {ssid}: ТД без доступа к Интернету")
                check_err = 1
                err_name = 'Error: ТД без доступа в Интернет, на Авториз не попасть'
                return False


            # -- Проверка взлёта кептива
            if devices_name == "Samsung A32":
                captive = d.xpath('//*[@resource-id="android:id/action_bar"]/android.widget.LinearLayout[1]')

            if devices_name == 'OnePlus 9R':
                captive = d.xpath('//*[@content-desc="Ещё"]')
            else:
                captive = d(text="Подключаться автоматически")

            captive.wait(True, 60)
            if captive.exists:
                print(f"{NowDate()}  SSID найден.Авторизация началась")
                f.write(f"{NowDate()}  SSID найден.Авторизация началась\n")
                print(f"{NowDate()}  Кептив открылся")
                f.write(f"{NowDate()}  Кептив открылся\n")
            elif not ssid_name.exists:
                print("\033[31m{}\033[0m".format(f"{NowDate()}  SSID не найден.Тест завершен."))
                f.write(f"{NowDate()}  SSID не найден.Тест завершен.\n")
                SendMessage(f"{devices_name}: ⛔ {ssid}: SSID не найден")
                check_err = 1
                err_name = 'Error: No SSID'
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 3, "SSID not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False
            else:
                print("\033[31m{}\033[0m".format(f"{NowDate()}  Кептив не отработал.Тест завершен."))
                f.write(f"{NowDate()}  Кептив не отработал.Тест завершен.\n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Тест упал")
                check_err = 1
                err_name = 'Error: Unknown'
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "Captive not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

                # -- Проверка не убитой сессии 2
                if Functions.CheckInternet.CheckInternet(d, devices_name):

                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен."))
                    f.write(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен.\n")
                    SendMessage(f"{devices_name}: ⛔ {ssid}: Сессия не убита")
                    check_err = 1
                    err_name = 'Error: No kill session'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 2, "Active session", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                else:
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Кептив не отработал.Тест завершен."))
                    f.write(f"{NowDate()}  Кептив не отработал.Тест завершен.\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Тест упал")
                    check_err = 1
                    err_name = 'Error: No Captive'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Captive not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Чекер ошибки 400
            if d(text="Error 400: Bad Request").exists:
                print("\033[31m{}\033[0m".format(f"{NowDate()}  Error 400: Bad Request"))
                f.write(f"{NowDate()}  Error 400: Bad Request\n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Error 400: Bad Request")
                err_name = 'Error: 400 Bad Request'
                err400 = True
                check_err = 1
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "err400", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Чекер заглушки
            check_random = d.xpath('//*[@resource-id="changeSettings"]')
            if check_random.exists:
                print("\033[31m{}\033[0m".format(f"{NowDate()} Найдена заглушка для рандомного мас"))
                f.write(f"{NowDate()}  Найдена заглушка для рандомного мас\n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Найдена заглушка для рандомного мас")
                check_err = 1
                err_name = 'Error: Unknown'
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "random mac", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            #Ошибки
            err900 = d.xpath('//*[@text="Ошибка #900"]')
            err432 = d.xpath('//*[@text="Ошибка #432"]')
            err100 = d.xpath('//*[@text="Ошибка #100"]')
            err304 = d.xpath('//*[.="Ошибка #304"]')
            # -- Нажатие на "Войти в интернет"

            open_sixty_min = d.xpath('//*[@text="Войти в Интернет" or @text="Войти на 60 минут" or @text="Internetga kirish"]')
            open_sixty_min.wait(60)
            while flag != 0:
                if open_sixty_min.exists:
                    # кнопка находится но неактивна в течении 5 сек. Нужен кликабле
                    open_sixty_min.click_exists(20)
                    print(f"{NowDate()}  Нажата кнопка 'Войти в Интернет'")
                    f.write(f"{NowDate()}  Нажата кнопка 'Войти в Интернет'\n")
                    time_start_avtoriz = time()
                    flag -= 1
                    break
                if err100.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка 100.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка 100.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 100")
                    check_err = 1
                    err_name = 'Error: 100'
                    return False
                if err304.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка 304.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка 304.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 304")
                    check_err = 1
                    err_name = 'Error: 304'
                if err432.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка 432.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка 432.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 432")
                    check_err = 1
                    err_name = 'Error: 432'
                    return False
                if flag == 1:
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Кнопка 'Войти в Интернет' не найдена. Скрипт принудительно завершен "))
                    f.write(f"{NowDate()}  Кнопка 'Войти в Интернет' не найдена. Скрипт принудительно завершен \n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Кнопка 'Войти в Интернет' не найдена. Скрипт завершен")
                    check_err = 1
                    err_name = 'Error: Unknown'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "button Connect not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                else:
                    flag -= 1
                    sleep(3)
                    continue

            # -- Прохождение рекламы
            button_x1 = d.xpath(
                '//*[@text="Авторизация Wi-Fi"]/android.view.View[2]/android.view.View[1]/android.view.View[3]/android.view.View[1]')
            button_x2 = d.xpath(
                '//*[@text="Авторизация Wi-Fi"]/android.view.View[2]/android.view.View[1]/android.view.View[1]')
            # button_x2 = d.xpath('//*/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[1]')
            button_x3 = d.xpath('//*[@text="Wi-Fi.ru"]/android.view.View[3]/android.view.View[1]')

            errWebStr = d.xpath('//*[@text="Не удалось открыть веб-страницу"]')
            button_continue = d.xpath('//*[@text="Продолжить" or @text="Далее"]')

            # Назначения чекеров для сегментов


            if 'dit' in ssid or ssid == '_P_rtk_hospital' or ssid == '_P_dit_almatel':
                if ssid == '_P_rtk_hospital':

                    final_check = d.xpath('//*[@text="mos.ru – Официальный сайт Мэра Москвы"]')
                    final_check2 = d(text="Главные новости")
                    final_check3 = d.xpath('//*[@text="user"]')

                elif ssid == '_P_dit_almatel':
                    final_check = d.xpath('//*[@content-desc="ОТКРЫТЬ САЙТ ТЕАТРА"]')
                    final_check2 = d.xpath('//*[@content-desc="ОТКРЫТЬ САЙТ ТЕАТРА"]')
                    final_check3 = d.xpath('//*[@text="user"]')

                else:
                    final_check = d.xpath('//*[@text="mos.ru"]')
                    final_check2 = d.xpath('//*[@text="mos.ru"]')
                    final_check3 = d.xpath('//*[@text="user"]')

            elif ssid == '_P_Sola_MT_507':
                final_check = d.xpath('//*[@content-desc="Logo"]')
                final_check2 = d.xpath('//*[@content-desc="Logo"]')
                final_check3 = d.xpath('//*[@text="user"]')
            elif ssid == '_P_metro':
                final_check = d.xpath('//*[@content-desc="cabinet.wi-fi"]')
                final_check2 = d.xpath('//*[@text="Популярные Все"]/android.view.View[1]/android.widget.TextView[1]')
                final_check3 = d.xpath('//*[@text="user"]')
            else:
                final_check2 = d.xpath('//*[@text=""]')
                final_check = d.xpath('//*[@content-desc="cabinet.wi-fi"]')
                final_check3 = d.xpath('//*[@text="user"]')
                

            # Авторизация
            while not (final_check.exists or final_check2.exists or final_check3.exists or ssid_name.exists):
                sleep(5)
                if err900.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка 900.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка 900.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 900")
                    err_name = 'Error: 900'
                    check_err = 1
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Error900", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                if err432.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка 432.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка 432.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 432")
                    err_name = 'Error: 432'
                    check_err = 1
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Error900", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                elif errWebStr.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка Не удалось открыть веб-страницу ERR_TIMED_OUT.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка Не удалось открыть веб-страницу ERR_TIMED_OUT.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка Не удалось открыть веб-страницу ERR_TIMED_OUT")
                    check_err = 1
                    err_name = 'Error: Не удалось открыть веб-страницу ERR_TIMED_OUT'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "err - web page not be opened",
                    #          f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                elif err100.exists:
                    print("\033[31m{}\033[0m".format(f"{NowDate()} Ошибка 100.Скрипт завершен"))
                    f.write(f"{NowDate()} Ошибка 100.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 100")
                    check_err = 1
                    err_name = 'Error: 100'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Error100", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                elif button_continue.exists:
                    button_continue.click(1)
                    print(f"{NowDate()}  Нажата кнопка Продолжить/Далее")
                    f.write(f"{NowDate()}  Нажата кнопка Продолжить/Далее\n")
                    sleep(6)
                # elif d.image.match(imTestX):
                #     d.image.click(imTestX, timeout=1.0)
                #     flag2 -= 1
                #     print(f"{NowDate()}  Нажат крестик вид №3")
                #     f.write(f"{NowDate()}  Нажат крестик вид №3\n")
                #     sleep(6)
                elif button_x1.exists:
                    button_x1.click_exists(5)
                    flag2 -= 1
                    print(f"{NowDate()}  Нажат крестик вид №1")
                    f.write(f"{NowDate()}  Нажат крестик вид №1\n")
                    sleep(6)

                elif button_x2.exists and not button_x3.exists:
                    if devices_name == "XiaomiSE":
                        d.click(0.923, 0.19)
                        #button_x2.click_exists(5)
                        flag2 -= 1
                    if devices_name == "XiaomiRedmiNote9":
                        d.click(0.940, 0.220)
                        # button_x2.click_exists(5)
                        flag2 -= 1
                    if devices_name == "Samsung A32":
                        # d.click(962, 273)
                        button_x2.click_exists(5)
                        flag2 -= 1
                    print(f"{NowDate()}  Нажат крестик вид №2")
                    f.write(f"{NowDate()}  Нажат крестик вид №2\n")
                    sleep(7)
                elif not button_x2.exists and button_x3.exists:
                    if devices_name == "XiaomiSE":
                        d.click(0.923, 0.19)
                        #button_x3.click_exists(5)
                        flag2 -= 1
                    if devices_name == "XiaomiRedmiNote9":
                        # d.click(980, 490)
                        button_x3.click_exists(5)
                        flag2 -= 1
                    if devices_name == "Samsung A32":
                        # d.click(962, 273)
                        button_x3.click_exists(5)
                        flag2 -= 1
                    print(f"{NowDate()}  Нажат крестик вид №3")
                    f.write(f"{NowDate()}  Нажат крестик вид №3\n")
                    sleep(7)
                elif flag2 == 1:
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен "))
                    f.write(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен \n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Портал не прогрузился")
                    check_err = 1
                    err_name = 'Error: Портал не прогрузился'
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 3, "Portal not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                else:
                    flag2 -= 1
                    sleep(5)
                    continue

            # Проверка иконки на портале
            if 'dit' in ssid or ssid == '_P_rtk_hospital' or ssid == '_P_Sola_MT_507':
                if final_check.exists or final_check3.exists or final_check2.exists:
                    print(f"{NowDate()}  Иконка на портале найдена")
                    f.write(f"{NowDate()}  Иконка на портале найдена\n")
                else:
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Иконка на портале не найдена"))
                    f.write(f"{NowDate()}  Иконка на портале не найдена\n")
            else:
                if final_check.exists or final_check2.exists or final_check3.exists:
                    print(f"{NowDate()}  Иконка на портале найдена")
                    f.write(f"{NowDate()}  Иконка на портале найдена\n")
                else:
                    print("\033[31m{}\033[0m".format(f"{NowDate()}  Иконка на портале не найдена"))
                    f.write(f"{NowDate()}  Иконка на портале не найдена\n")

            # -- На портале
            if devices_name != 'Samsung A32':
                tick = d(resourceId="android:id/button2")
                tick.click_exists(10)
                print(f"{NowDate()}  Нажата галочка")
                time_end_avtoriz = time() - time_start_avtoriz
                print(f"Время затраченное на авторизацию: {round(time_end_avtoriz, 2)} сек")
                f.write(f"{NowDate()}  Нажата галочка\n")
            else:
                print(f"{NowDate()}  Кептив закрылся")
                f.write(f"{NowDate()}  Кептив закрылся\n")
                time_end_avtoriz = time() - time_start_avtoriz
                print(f"Время затраченное на авторизацию: {round(time_end_avtoriz, 2)} сек")

            # -- Проверка доступа в интернет
            if Functions.CheckInternet.CheckInternet(d, devices_name):
                print(f"{NowDate()}  Доступ в интернет есть!")
                f.write(f"{NowDate()}  Доступ в интернет есть! \n")
            else:
                print("\033[31m{}\033[0m".format(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен "))
                f.write(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен \n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Доступа в интернет нет!")
                check_err = 1
                err_name = 'Error: No access Internet'
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "Internet offline", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Финиш
            SendMessage(f"{devices_name}: 📣 {ssid}: Тест Авториз успешно пройден ✅ ")
            print("\033[32m{}\033[0m".format(f"{NowDate()}  Тест пройден ✅"))
            f.write(f"{NowDate()}  Тест пройден ✅ \n")
            success = 1
            # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
            # addResult(ssid, devices_name, 0, "PASS", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
            return True


        finally:
            if success==0 and check_err==0:
                print(f"{NowDate()}  Unknown Error")
                f.write(f"{NowDate()}  Unknown Error\n")
                SendMessage(f"{devices_name} 🔥 {ssid}: Unknown Error")
                check_err =1
                err_name = 'Error: Unknown'

            sleep(2)
            if d.screenrecord.stop() == "False":
                print("False")
                print(d.screenrecord.stop())
            if err400 and 'Xiaomi' in devices_name:
                XiaomiCl(d, devices_name)
            d.press("home")
            sleep(2)
            d.shell('svc wifi disable')
            d.shell('input keyevent 26')
            requests.get(
                f"http://10.1.11.2/auth/deauthorize/{mac}") if ssid == '_P_dit_enforta_street' else requests.get(
                f"http://sae.msk.vmet.ro/v1/drop/mac/{mac}")
            print(f"{NowDate()}  Сессия убита ✅")
            #print(id, ntest, dt, ssid, link_video, check_err, err_name)
            time_finish = time() - time_start
            print(f"Время работы скрипта: {round(time_finish, 2)} сек")
            if check_err == 1:
                # sendYandexScreencast(f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4",
                #                      f"{devices_name}_{name_video}.mp4")
                Send_screencast(f"screencasts/{devices_name}_{name_video}.mp4", f'Авторизация {devices_name}\n{ssid}')

            print(f"_____________________________________________________________")
            f.write(f"{NowDate()}  Сессия убита ✅\n")

            f.write(f"_____________________________________________________________\n")
            sleep(10)
            print(id, ntest, dt, ssid, type, check_err, err_name)
            client.execute(
                'INSERT INTO devdb1.auto_tests (id, ntest, dt, ssid, type, err_flags, err_name) VALUES',
                [{'id': id, 'ntest': ntest, 'dt': dt, 'ssid': ssid, 'type': type, 'err_flags': check_err,
                  'err_name': err_name}])
