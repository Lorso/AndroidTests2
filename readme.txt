pytest -s Test_MT.py::TestOther::test_cppk - запуск определенного теста
pytest -s Test_MT.py::TestOther - запуск определенного класса тестов ( ЕОС или Other)
pytest -s Test_MT.py - запуск всех тестов


pytest -s Test_MT.py::TestEOS::test_eos_enforta

pytest --count=5 -s Test_MT.py::TestOther::test_metroм - запуск определенного теста c количеством повторов 5 раз
pytest --reruns 1 -s Test_MT.py - запуск всех тестов + перезапуск n раз при падении теста

pytest --reruns 2 -s Test_MT.py::TestOther::test_bus


pytest --reruns 1 -s --alluredir results Test_MT.py - запуск всех тестов + формирование отчета allure + перезапуск при падении теста
pytest --reruns 1 -s --alluredir results Test_MT.py::TestEOS::test_eos_beeline



Построение отчета
В павершеле
cd C:\Users\v.glagolev\PycharmProjects\pythonProject1 - перейти в папку проекта
https://scoop.sh/
allure serve results - команда формирования отчета

pytest --count=5 -s --alluredir results Test_MT.py::TestOther::test_mcc