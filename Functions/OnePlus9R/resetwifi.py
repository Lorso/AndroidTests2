from time import sleep

def resetwifi(d):
    # Чистка вкладок приложений
    d(resourceId="com.android.systemui:id/recent_apps").click()
    sleep(4)
    d(resourceId="net.oneplus.launcher:id/clear_all_button").click()
    sleep(4)

    # СБРОС НАСТРОЕК ВИФИ
    sleep(2)
    d.press("home")
    sleep(5)
    d(text="Настройки").click()
    sleep(2)
    d(resourceId="com.android.settings:id/action_search").click()
    sleep(2)
    d(resourceId="android:id/title").click()
    sleep(2)
    d(resourceId="android:id/title", text="Сбросить настройки Wi-Fi, мобильного Интернета и Bluetooth").click()
    sleep(2)
    d.xpath(
        '//*[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click()
    sleep(2)
    d(resourceId="com.android.settings:id/initiate_reset_network").click()
    sleep(2)
    d(resourceId="com.android.settings:id/execute_reset_network").click()
    sleep(10)