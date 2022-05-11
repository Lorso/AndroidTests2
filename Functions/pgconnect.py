import psycopg2
from psycopg2 import Error


def addResult (ssid, devices, result, err_check, video_href):
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="2812",
                                      host="localhost",
                                      port="5432",
                                      database="AvtoTests")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f""" INSERT INTO public."Tests"("SSID", devices, result, err_check,video_href) VALUES ('{ssid}', '{devices}', {result},'{err_check}','{video_href}');"""
        cursor.execute(insert_query)
        connection.commit()
        print("запись успешно вставлена")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с PostgreSQL закрыто")


# addResult("metro", "xiaomi", 1, "ss", "")
def updateResult(video_href):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="2812",
                                      host="localhost",
                                      port="5432",
                                      database="AvtoTests")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Выполнение SQL-запроса для вставки данных в таблицу
        insert_query = f""" UPDATE public."Tests" SET video_href='{video_href}'	WHERE id=(SELECT MAX(id) FROM public."Tests");"""
        cursor.execute(insert_query)
        connection.commit()
        print("запись успешно обновлена")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с PostgreSQL закрыто")
