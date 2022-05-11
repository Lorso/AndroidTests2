from time import sleep
import schedule
from Functions.TelegramApi import Send_File
from Functions.TelegramApi import SendMessage
from Functions.DataName import NowDate
from Tests.Tests import AutoTest


if __name__ == "__main__":
    print(f"{NowDate()}  📣 :  Автотесты запущены📱")
    print(f"_____________________________________________________________")
    with open("logs/buttonClick.txt", 'w', encoding='utf-8') as f:
        f.write(f"{NowDate()}  📣 :  Автотесты запущены🚀\n")
        f.write(f"_____________________________________________________________\n")

    # XiaomiRedmiNote9
    number2 = "a3f47191"
    MAC2 = '18-87-40-45-D2-9B'
    Name2 = 'XiaomiRedmiNote9'

    SendMessage(f"Автотесты запущены 📱")  # Отправка сообщения в телеграмм канал

    # Устренние тесты

    # @repeat(every(1).minutes, number2, MAC2, Name2)
    def startTestsXiaomiRedmi(number, mac, name):
        AutoTest(number, mac, name, '_P_metro', 'metro')
        AutoTest(number, mac, name, '_P_cppk', 'cppk')
        AutoTest(number, mac, name, '_P_MCC_incarnet', 'mcc')
        AutoTest(number, mac, name, '_P_aeroexpress', 'aeroexpress')
        AutoTest(number, mac, name, 'p_mvf_bus', 'bus')
        AutoTest(number, mac, name, '_P_Sola_MT_507', 'sola')
        # # ЕОС
        AutoTest(number, mac, name, '_P_dit_enforta_street', 'enforta')
        AutoTest(number, mac, name, '_P_dit_akado', 'akado')
        AutoTest(number, mac, name, '_P_dit_guest_wifi', 'guest')
        AutoTest(number, mac, name, '_P_dit_Nauka 3', 'nauka')
        # AutoTest(number, mac, name, '_P_dit_snb', 'snb')
        AutoTest(number, mac, name, '_P_dit_almatel', 'almatel')
        AutoTest(number, mac, name, '_P_dit_beeline', 'beeline')
        AutoTest(number, mac, name, '_P_ttk_hospitals', 'hospitals')
        # AutoTest(number, mac, name, '_P_dit_mts_vdnh', 'mts_vdnh')



    startTestsXiaomiRedmi(number2, MAC2, Name2)

    SendMessage(f"✅Автотесты завершены 📴")  # Отправка сообщения в телеграмм канал
    Send_File("logs/buttonClick.txt")
    print(f"{NowDate()}  📣 :  Автотесты завершены📱")

    # schedule.every(3).minutes.do(startTestsXiaomiRedmi(number2, MAC2, Name2))

    # while True:
    #     schedule.run_pending()
    #     sleep(1)
