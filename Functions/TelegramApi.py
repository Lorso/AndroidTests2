import requests
from time import sleep

#chatId = '-1001007302005'
chatId = '-1001782200645'
#chatId = ' -681115417'
#TOKEN2 = '2072244468:AAEBstS6Ct2i0k4TOIP_AFCbhKwJ7xNdYck'

#TOKEN = '1722725130:AAEMwr-huLcjM-AEvMRzzzVEyeHNOaH_Y78'
TOKEN = '5397195536:AAHFzvc0tO_UxbsWsomlwz5z0jC5C6u440c'


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


