import pytest
from Functions.TelegramApi import Send_File
from Functions.TelegramApi import SendMessage
from Functions.DataName import NowDate
from Tests.Tests_Auth import AutoTest
import allure
import time


#XiaomiRedmiNote9
# number = "a3f47191"
# mac = '18-87-40-45-D2-9B'
# name = 'XiaomiRedmiNote9'

#Xiaomi SE (Розовый)
number = "be11611b"
mac = '60-ab-67-f7-1d-a0'
name = 'XiaomiSE'

#Xiaomi 10t pro
# number = "87a7c836"
# mac = ''
# name = 'Xiaomi10tPro'

# OnePlus 9R
# number = "c21e8c42"
# mac = 'ac-d6-18-60-36-6c'
# name = 'OnePlus 9R'

@pytest.fixture(autouse=True, scope="session")
def begin ():
    print(f"{NowDate()}  📣 : Тесты запущены📱")
    SendMessage(f"Тесты Авториз Android запущены 📱")  # Отправка сообщения в телеграмм канал
    print(f"_____________________________________________________________")
    f = open('logs/buttonClick.txt', 'w', encoding='utf-8')
    f.close()
    yield
    SendMessage(f"✅Тесты Android завершены 📴")  # Отправка сообщения в телеграмм канал
    Send_File("logs/buttonClick.txt")
    print(f"{NowDate()}  📣 :Android  Тесты завершены📱")


@allure.suite("Тесты сегментов ЕОС")
class TestEOS:
    # @pytest.mark.skip('Ведутся работы с ТД')
    # @allure.feature("Тест авторизации")
    # @allure.story("Авторизация _P_dit_snb")
    # def test_eos_snb (self):
    #     assert AutoTest(number, mac, name, '_P_dit_snb', 'snb') == True, "Ошибка в ходе выполнения" \
    #                                                                      " теста _P_dit_snb"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_dit_enforta_street")
    def test_eos_enforta (self):
        assert AutoTest(number, mac, name, '_P_dit_enforta_street', 'enforta') == True, "Ошибка в ходе выполнения" \
                                                                                        " теста _P_dit_enforta_street"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_dit_akado")
    def test_eos_akado (self):
        assert AutoTest(number, mac, name, '_P_dit_akado', 'akado') == True, "Ошибка в ходе выполнения" \
                                                                             " теста _P_dit_akado"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_dit_guest_wifi")
    def test_eos_guest (self):
        assert AutoTest(number, mac, name, '_P_dit_guest_wifi', 'guest') == True, "Ошибка в ходе выполнения" \
                                                                                  " теста _P_dit_guest_wifi"

    @pytest.mark.skip('Ведутся работы с ТД')
    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_dit_Nauka 3")
    def test_eos_nauka (self):
        assert AutoTest(number, mac, name, '_P_dit_Nauka 3', 'nauka') == True, "Ошибка в ходе выполнения" \
                                                                               " теста _P_dit_Nauka 3"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_dit_almatel")
    def test_eos_almatel (self):
        assert AutoTest(number, mac, name, '_P_dit_almatel', 'almatel') == True, "Ошибка в ходе выполнения" \
                                                                                 " теста _P_dit_almatel"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_dit_beeline")
    def test_eos_beeline (self):
        assert AutoTest(number, mac, name, '_P_dit_beeline', 'beeline') == True, "Ошибка в ходе выполнения" \
                                                                                 " теста _P_dit_beeline"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_rtk_hospital")
    def test_eos_hospitals (self):
        assert AutoTest(number, mac, name, '_P_rtk_hospital', 'hospitals') == True, "Ошибка в ходе выполнения" \
                                                                                     " теста _P_ttk_hospitals"


@allure.suite("Тесты основных сегментов сети МТ")
class TestOther:
    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_metro")
    def test_metro (self):
        assert AutoTest(number, mac, name, '_P_metro', 'metro') == True, "Ошибка в ходе выполнения теста _P_metro"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_cppk")
    def test_cppk (self):
        assert AutoTest(number, mac, name, '_P_cppk', 'cppk') == True, "Ошибка в ходе выполнения теста _P_cppk"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_MCC_incarnet")
    def test_mcc (self):
        assert AutoTest(number, mac, name, '_P_MCC_incarnet', 'mcc') == True, "Ошибка в ходе выполнения теста " \
                                                                              "_P_MCC_incarnet"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_aeroexpress")
    def test_aeroexpress (self):
        assert AutoTest(number, mac, name, '_P_aeroexpress', 'aeroexpress') == True, "Ошибка в ходе выполнения" \
                                                                                     " теста _P_aeroexpress"

    # @allure.feature("Тест авторизации")
    # @allure.story("Авторизация _P_Sola_MT_507")
    # def test_sola (self):
    #     assert AutoTest(number, mac, name, '_P_Sola_MT_507', 'sola') == True, "Ошибка в ходе выполнения " \
    #                                                                           "теста _P_Sola_MT_507"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_mvf_bus")
    def test_bus154(self):
        assert AutoTest(number, mac, name, '_P_mvf_bus', 'bus154') == True, "Ошибка в ходе выполнения теста bus154"

    @allure.feature("Тест авторизации")
    @allure.story("Авторизация _P_TTM_v5")
    def test_bus207(self):
        assert AutoTest(number, mac, name, '_P_TTM_v5', 'bus207') == True, "Ошибка в ходе выполнения теста bus207"

