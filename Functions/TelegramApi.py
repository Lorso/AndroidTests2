import requests
from time import sleep


chatId = '-1001782200645'
chatId2 = '-1001746920431'

TOKEN = '5397195536:AAHFzvc0tO_UxbsWsomlwz5z0jC5C6u440c'

#Авториз
def SendMessage (text):
    requests.get(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chatId}&text={text}')
    sleep(1)


def Send_screencast (video, text):
    files = {'video': open(video, 'rb')}
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendVideo?chat_id={chatId}&caption={text}', files=files)
    sleep(30)


def Send_File (txt):
    files = {'document': open(txt, 'rb')}
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={chatId}', files=files)
    sleep(2)


#ИДент
def SendMessage2 (text):
    requests.get(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chatId2}&text={text}')
    sleep(1)


def Send_screencast2 (video, text):
    files = {'video': open(video, 'rb')}
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendVideo?chat_id={chatId2}&caption={text}', files=files)
    sleep(30)


def Send_File2 (txt):
    files = {'document': open(txt, 'rb')}
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={chatId2}', files=files)
    sleep(2)


