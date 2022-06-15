from time import sleep

from Functions.DataName import NowDate
from Functions.TelegramApi import SendMessage

def identsms(getsms, f, d, devices_name, ssid, sim, final_check1, final_check2, final_check3, button_x1, button_x2, button_x3):
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
            sleep(10)
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
            print(f"{NowDate()}  SMS не пришла")
            f.write(f"{NowDate()}  SMS не пришла\n")
            SendMessage(f"{devices_name}: 🔥 {ssid} SMS не пришла")
            err_name = 'Error: No SMS'
            return False