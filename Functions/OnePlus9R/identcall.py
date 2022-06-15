from time import sleep

from Functions.DataName import NowDate
from Functions.TelegramApi import SendMessage

def identcall(callme, f, d, devices_name, ssid, sim, final_check1, final_check2, final_check3, button_x1, button_x2, button_x3):
    callme.wait(True, 10)
    if callme.exists():
        type = 'CALL'
        print(f"{NowDate()}  Идентификация по звонку")
        f.write(f"{NowDate()}  Идентификация по звонку\n")
        d.xpath('//*[@resource-id="call-phone"]/android.view.View[1]').click()  # Нажато поле ввода телефона
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
        sleep(40)
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
            sleep(3)
            #### Вытащит последние 4 цифры
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
            d(resourceId="android:id/floating_toolbar_menu_item_text", text="Вставить").click()  # Вставка кода
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
                    SendMessage(f"{devices_name}: 🔥 {ssid} Неправильно введён код")
                    err_name = 'Error: Incorrect Code'
                    return False
                else:
                    check_err = 1
                    print(f"{NowDate()}  Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась")
                    f.write(f"{NowDate()}  Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась\n")
                    SendMessage(f"{devices_name}: 🔥 {ssid}Кнопка «ВОЙТИ В ИНТЕРНЕТ не прогрузилась")
                    err_name = 'Error: Не прогрузилась кнопка ВОЙТИ В ИНТЕРНЕТ'
                    return False

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
                    SendMessage(f"{devices_name} 🔥 {ssid}: Вместо портала, страница авторизации")
                    sleep(12)
                    err_name = 'Error: Вместо портала, страница авторизации'
                    return False
                else:
                    check_err = 1
                    print(f"{NowDate()}  Портал не загрузился")
                    f.write(f"{NowDate()}  Портал не загрузился\n")
                    SendMessage(f"{devices_name} 🔥 {ssid}: Портал не загрузился")
                    sleep(12)
                    err_name = 'Error: Портал не прогрузился'
                    return False

        else:
            check_err = 1
            print(f"{NowDate()}  Звонок не поступил")
            f.write(f"{NowDate()}  Звонок не поступил\n")
            SendMessage(f"{devices_name}: 🔥 {ssid}Звонок не поступил")
            err_name = 'Error: No Call'
            return False