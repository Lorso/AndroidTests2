import pytest
from Functions.TelegramApi import Send_File
from Functions.TelegramApi import SendMessage
from Functions.DataName import NowDate
from Tests.Tests_frame_version import AutoTest

# XiaomiRedmiNote9
number = "a3f47191"
mac = '18-87-40-45-D2-9B'
name = 'XiaomiRedmiNote9'


@pytest.fixture(autouse=True, scope="class")
def begin ():
    print(f"{NowDate()}  📣 :  Автотесты запущены📱")
    print(f"_____________________________________________________________")
    f = open('logs/buttonClick.txt', 'w', encoding='utf-8')
    f.close()
    yield
    # SendMessage(f"✅Автотесты завершены 📴")  # Отправка сообщения в телеграмм канал
    # Send_File("logs/buttonClick.txt")
    print(f"{NowDate()}  📣 :  Автотесты завершены📱")


class TestEOS():
    def test_eos_enforta (self):
        assert AutoTest(number, mac, name, '_P_dit_enforta_street', 'enforta') == True, "Ошибка в ходе выполнения" \
                                                                                        " теста _P_dit_enforta_street"

    def test_eos_akado (self):
        assert AutoTest(number, mac, name, '_P_dit_akado', 'akado') == True, "Ошибка в ходе выполнения" \
                                                                             " теста _P_dit_akado"

    def test_eos_guest (self):
        assert AutoTest(number, mac, name, '_P_dit_guest_wifi', 'guest') == True, "Ошибка в ходе выполнения" \
                                                                                  " теста _P_dit_guest_wifi"

    def test_eos_nauka (self):
        assert AutoTest(number, mac, name, '_P_dit_Nauka 3', 'nauka') == True, "Ошибка в ходе выполнения" \
                                                                               " теста _P_dit_Nauka 3"

    def test_eos_almatel (self):
        assert AutoTest(number, mac, name, '_P_dit_almatel', 'almatel') == True, "Ошибка в ходе выполнения" \
                                                                                 " теста _P_dit_almatel"

    def test_eos_beeline (self):
        assert AutoTest(number, mac, name, '_P_dit_beeline', 'beeline') == True, "Ошибка в ходе выполнения" \
                                                                                 " теста _P_dit_beeline"

    def test_eos_hospitals (self):
        assert AutoTest(number, mac, name, '_P_ttk_hospitals', 'hospitals') == True, "Ошибка в ходе выполнения" \
                                                                                     " теста _P_ttk_hospitals"
