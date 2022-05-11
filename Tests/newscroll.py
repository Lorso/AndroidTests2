def AutoTest (ser, mac, devices_name, ssid):
    import uiautomator2 as u2
    from time import sleep
    from time import time
    import requests
    import Functions.CheckInternet
    from Functions.ClearCookie import XiaomiCl
    from Functions.DataName import NowDate
    from Functions.TelegramApi import SendMessage
    from Functions.TelegramApi import Send_screencast
    from Functions.LockDisplay import Lock
    from Functions.Sumsung import Connect_WiFi
    from Functions.FindSsid import scroll

    time_start = time()
    if devices_name == "Samsung A32" and ssid == 'MT_FREE':
        ssid = ssid
        name_video = ssid
    else:
        ssid = ssid
        name_video = ssid[1::]

    d = u2.connect_usb(ser)
    flag = 6
    flag2 = 12
    err400 = False
    check_err = False

    try:
        print(f"{NowDate()}  {devices_name}: 📣 {ssid}:  Автотест запущен📱")

        if d.info.get('screenOn'):
            d.shell('input keyevent 26')  # Проверка активности экрана. Если вкл, то выкл перед началом теста
        Lock(d)  # Разблокировка экрана

        if devices_name == "Samsung A32":
            Connect_WiFi(d)
        else:
            d.shell("am start -n com.android.settings/com.android.settings.wifi.WifiSettings")  # Переход в настр
            wifi = d(text='Wi-Fi', className='android.widget.TextView')
            wifi.click_exists(3)

        d.shell('svc wifi enable')  # Включение Wi-F
        sleep(5)

        # -- Подключение к SSID

        if devices_name == "Samsung A32":
            ssid_name = d(resourceId="com.android.settings:id/title", text=f"{ssid}")
            ssid_name.wait(True, 60)
            if ssid_name.exists:
                ssid_name.click_gone(5, 5)
                sleep(6)

        else:
            if d(resourceId="miui:id/buttonPanel").exists:
                d(resourceId="miui:id/buttonPanel").click_gone()
            ssid_name = d(text=f'{ssid}', className='android.widget.CheckedTextView')
            print("Тут должен быть скролл")
            d(scrollable=True).scroll.vert.forward(steps=200)
            ssid_name.wait(True, 20)
            if ssid_name.exists:
                ssid_name.click_gone(5, 5)
                sleep(7)

    finally:
        sleep(2)
        if err400 and 'Xiaomi' in devices_name:
            XiaomiCl(d, devices_name)
        d.press("home")
        sleep(2)
        d.shell('svc wifi disable')
        d.shell('input keyevent 26')
        time_finish = time() - time_start
        print(f"Время работы скрипта: {round(time_finish, 2)} сек")
        print(f"_____________________________________________________________")
        sleep(2)


number2 = "a3f47191"
MAC2 = '18-87-40-45-D2-9B'
Name2 = 'XiaomiRedmiNote9'
AutoTest(number2, MAC2, Name2, '_P_aeroexpress')
