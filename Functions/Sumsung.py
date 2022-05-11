def Connect_WiFi(d):
    d.shell("am start -a android.settings.WIRELESS_SETTINGS")
    WIFI = d(resourceId="android:id/title", text="Wi-Fi")
    WIFI.click_exists(2)