from time import sleep


def BrowserMiuiExit(d):
    d.click(1000, 200)
    sleep(1)
    clouseAll = d(resourceId="com.mi.globalbrowser:id/nav_close_all")
    if clouseAll.exists:
        clouseAll.click(2)
        sleep(1)
        clouseButton = d(resourceId="android:id/button1")
        if clouseButton.exists:
            assert clouseButton, "Не найдена кнопка подтвержения закрытия вкладок браузера"
            clouseButton.click(2)
            sleep(1)
    d.press("home")


def BrowserChromeExit(d):
    #Чистка куки
    but1 = d(resourceId="com.android.chrome:id/menu_button_wrapper")
    but2 = d(resourceId="com.android.chrome:id/menu_item_text", text="История")
    but3 = d(resourceId="com.android.chrome:id/clear_browsing_data_button")
    but4 = d(resourceId="com.android.chrome:id/clear_button")
    but5 = d(resourceId="com.android.chrome:id/close_menu_id")

    if but1.exists:
        but1.click()
    sleep(1)
    if but2.exists:
        but2.click()
    sleep(1)
    if but3.exists:
        but3.click()
    sleep(1)
    if but4.exists:
        but4.click()
    sleep(1)
    if but5.exists:
        but5.click()
    sleep(1)

    #Чистка вкладок
    button01 = d(resourceId="com.android.chrome:id/tab_switcher_button") # [1]
    button02 = d(resourceId="com.android.chrome:id/menu_anchor") # 3 точки
    button03 = d(resourceId="com.android.chrome:id/menu_item_text", text="Закрыть все вкладки") #закрыть все вкладки с крестом
    button04 = d(resourceId="com.android.chrome:id/positive_button") #Закрыть все вкладки синяя
    if button01.exists:
        button01.click()
        sleep(1)
    if button02.exists:
        button02.click()
        sleep(1)
    if button03.exists:
        button03.click()
        sleep(1)
    if button04.exists:
        button04.click()
        sleep(1)


    d.press("home")
