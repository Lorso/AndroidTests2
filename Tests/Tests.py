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


    time_start = time()

    d = u2.connect_usb(ser)
    flag = 6
    flag2 = 15
    err400 = False
    check_err = False

    with open("logs/buttonClick.txt", 'a', encoding='utf-8') as f:
        try:
            print(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Автотест запущен📱")
            f.write(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Автотест запущен🚀\n")

            if d.info.get('screenOn'):
                d.shell('input keyevent 26')  # Проверка активности экрана. Если вкл, то выкл перед началом теста
            Lock(d)  # Разблокировка экрана

            # Уберет всплывашку от USB подключения
            if d(resourceId="miui:id/alertTitle").exists:
                d.click(0.488, 0.902)

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
            else:
                if d(resourceId="miui:id/buttonPanel").exists:
                    d(resourceId="miui:id/buttonPanel").click_gone()
                ssid_name = d(text=f'{ssid}', className='android.widget.CheckedTextView')
                if ssid == 'p_mvf_bus':
                    ssid_name.wait(True, 40)
                ssid_name.wait(True, 20)
                if ssid_name.exists:
                    ssid_name.click_gone(5, 5)
                    sleep(8)
                else:
                    # d(scrollable=True).scroll.to(text=f"{ssid}")
                    d(scrollable=True).scroll.vert.forward(steps=200)
                    ssid_name.click_gone(5, 5)
                    sleep(8)

            # -- Проверка не убитой сессии
            check_connect = d.xpath('//*[@text="Подключено"]')
            if check_connect.exists and ssid != "_P_ttk_hospitals":
                print(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен.")
                f.write(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен.\n")
                SendMessage(f"{devices_name}: ⛔ {ssid}: Сессия не убита")
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # err 0 - не баг \ 900 - ошибка 900 \ 100 - ошибка 100\
                # addResult(ssid, devices_name, 2, "Active session", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Проверка взлёта кептива
            if devices_name == "Samsung A32":
                captive = d.xpath('//*[@resource-id="android:id/action_bar"]/android.widget.LinearLayout[1]')
            else:
                captive = d(text="Подключаться автоматически")

            captive.wait(True, 60)
            if captive.exists:
                print(f"{NowDate()}  SSID найден.Авторизация началась")
                f.write(f"{NowDate()}  SSID найден.Авторизация началась\n")
                print(f"{NowDate()}  Кептив открылся")
                f.write(f"{NowDate()}  Кептив открылся\n")
            elif not ssid_name.exists:
                print(f"{NowDate()}  SSID не найден.Тест завершен.")
                f.write(f"{NowDate()}  SSID не найден.Тест завершен.\n")
                SendMessage(f"{devices_name}: ⛔ {ssid}: SSID не найден")
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 3, "SSID not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False
            else:
                # -- Проверка не убитой сессии 2
                if Functions.CheckInternet.CheckInternet(d, devices_name):
                    print(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен.")
                    f.write(f"{NowDate()}  Предыдущая сессия не убита.Тест завершен.\n")
                    SendMessage(f"{devices_name}: ⛔ {ssid}: Сессия не убита")
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 2, "Active session", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                else:
                    print(f"{NowDate()}  Кептив не отработал.Тест завершен.")
                    f.write(f"{NowDate()}  Кептив не отработал.Тест завершен.\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Автотест упал")
                    check_err = True
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Captive not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Чекер ошибки 400
            if d(text="Error 400: Bad Request").exists:
                print(f"{NowDate()}  Error 400: Bad Request")
                f.write(f"{NowDate()}  Error 400: Bad Request\n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Error 400: Bad Request")
                err400 = True
                check_err = True
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "err400", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Чекер заглушки
            check_random = d.xpath('//*[@resource-id="changeSettings"]')
            if check_random.exists:
                print(f"{NowDate()} Найдена заглушка для рандомного мас")
                f.write(f"{NowDate()}  Найдена заглушка для рандомного мас\n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Найдена заглушка для рандомного мас")
                check_err = True
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "random mac", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

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
                if flag == 1:
                    print(f"{NowDate()}  Кнопка 'Войти в Интернет' не найдена. Скрипт принудительно завершен ")
                    f.write(f"{NowDate()}  Кнопка 'Войти в Интернет' не найдена. Скрипт принудительно завершен \n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Кнопка 'Войти в Интернет' не найдена. Скрипт завершен")
                    check_err = True
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
            err900 = d.xpath('//*[@text="Ошибка #900"]')
            err100 = d.xpath('//*[@text="Ошибка #100"]')
            errWebStr = d.xpath('//*[@text="Не удалось открыть веб-страницу"]')
            button_continue = d.xpath('//*[@text="Продолжить" or @text="Далее"]')

            # Назначения чекеров для сегментов
            if 'dit' in ssid or ssid == '_P_ttk_hospitals':
                if ssid == '_P_ttk_hospitals':
                    final_check = d(text="mos.ru – Официальный сайт Мэра Москвы")
                    final_check2 = d(text="mos.ru – Официальный сайт Мэра Москвы")
                else:
                    final_check = d.xpath('//*[@content-desc="www.mos"]')
                    final_check2 = d.xpath('//*[@content-desc="www.mos"]')
            elif ssid == '_P_Sola_MT_507':
                final_check = d.xpath('//*[@content-desc="Logo"]')
                final_check2 = d.xpath('//*[@content-desc="Logo"]')
            else:
                final_check2 = d.xpath('//*[@text=""]')
                final_check = d.xpath('//*[@content-desc="cabinet.wi-fi"]')

            # Авторизация
            while not (final_check.exists or final_check2.exists or ssid_name.exists):
                if err900.exists:
                    print(f"{NowDate()} Ошибка 900.Скрипт завершен")
                    f.write(f"{NowDate()} Ошибка 900.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 900")
                    check_err = True
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Error900", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                elif errWebStr.exists:
                    print(f"{NowDate()}  Ошибка Не удалось открыть веб-страницу.Скрипт завершен")
                    f.write(f"{NowDate()}  Ошибка Не удалось открыть веб-страницу.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка Не удалось открыть веб-страницу")
                    check_err = True
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "err - web page not be opened",
                              f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                elif err100.exists:
                    print(f"{NowDate()} Ошибка 100.Скрипт завершен")
                    f.write(f"{NowDate()} Ошибка 100.Скрипт завершен\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Ошибка 100")
                    check_err = True
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 1, "Error100", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                elif button_continue.exists:
                    button_continue.click(1)
                    print(f"{NowDate()}  Нажата кнопка Продолжить/Далее")
                    f.write(f"{NowDate()}  Нажата кнопка Продолжить/Далее\n")
                    sleep(6)
                elif button_x1.exists:
                    button_x1.click_exists(5)
                    flag2 -= 1
                    print(f"{NowDate()}  Нажат крестик вид №1")
                    f.write(f"{NowDate()}  Нажат крестик вид №1\n")
                    sleep(6)
                elif button_x2.exists and not button_x3.exists:
                    if devices_name == "XiaomiMi9":
                        # d.click(954, 500)
                        button_x2.click_exists(5)
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
                elif button_x2.exists and button_x3.exists:
                    if devices_name == "XiaomiMi9":
                        # d.click(954, 500)
                        button_x3.click_exists(5)
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
                    print(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен ")
                    f.write(f"{NowDate()}  Иконка на портале не найдена. Скрипт принудительно завершен \n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}: Неизвестная ошибка")
                    check_err = True
                    # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                    # addResult(ssid, devices_name, 3, "Portal not found", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                    return False
                else:
                    flag2 -= 1
                    sleep(5)
                    continue

            # Надо как то упростить
            if 'dit' in ssid or ssid == '_P_ttk_hospitals' or ssid == '_P_Sola_MT_507':
                assert final_check.exists or ssid_name.exists, f"{NowDate()}  Авторизация не пройдена.Не найдена " \
                                                               f"кнопка на новостном портале "
                if final_check.exists:
                    print(f"{NowDate()}  Иконка на портале найдена")
                    f.write(f"{NowDate()}  Иконка на портале найдена\n")
                else:
                    print(f"{NowDate()}  Иконка на портале не найдена")
                    f.write(f"{NowDate()}  Иконка на портале не найдена\n")
            else:
                assert final_check.exists or final_check2.exists or ssid_name.exists, f"{NowDate()}  Авторизация не " \
                                                                                      f"пройдена.Не найдена кнопка на" \
                                                                                      f" новостном портале "
                if final_check.exists or final_check2.exists:
                    print(f"{NowDate()}  Иконка на портале найдена")
                    f.write(f"{NowDate()}  Иконка на портале найдена\n")
                else:
                    print(f"{NowDate()}  Иконка на портале не найдена")
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
                print(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен ")
                f.write(f"{NowDate()} Доступа в интернет нет! Скрипт принудительно завершен \n")
                SendMessage(f"{devices_name}: 🔥 {ssid}: Доступа в интернет нет!")
                check_err = True
                # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
                # addResult(ssid, devices_name, 1, "Internet offline", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
                return False

            # -- Финиш
            SendMessage(f"{devices_name}: 📣 {ssid}: Автотест успешно пройден ✅ ")
            print(f"{NowDate()}  Автотест пройден ✅")
            f.write(f"{NowDate()}  Автотест пройден ✅ \n")
            # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
            # addResult(ssid, devices_name, 0, "PASS", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")
            return True

        except AssertionError:
            check_err = True
            print(f"{NowDate()}  🔴 Автотест упал. Не найдена кнопка на новостном портале")
            f.write(f"{NowDate()}  🔴 Автотест упал. Не найдена кнопка на новостном портале\n")
            SendMessage(f"{devices_name}: 🔥 {ssid}: Автотест упал")
            # result 0 - успешно \ 1 - ошибка \ 2 - сессия не убита \ 3 - падение теста
            # addResult(ssid, devices_name, 3, "AssertionError", f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4")


        finally:
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
            time_finish = time() - time_start
            print(f"Время работы скрипта: {round(time_finish, 2)} сек")
            if check_err:
                sendYandexScreencast(f"{devices_name}_{name_video}_{datetime.now().strftime('%d.%m|%H_%M')}.mp4",
                                     f"{devices_name}_{name_video}.mp4")
                Send_screencast(f"screencasts/{devices_name}_{name_video}.mp4", f'Авторизация {devices_name}\n{ssid}')
            print(f"_____________________________________________________________")
            f.write(f"{NowDate()}  Сессия убита ✅\n")
            f.write(f"_____________________________________________________________\n")
            sleep(10)
