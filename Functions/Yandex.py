import requests
import json
import yadisk

# y = yadisk.YaDisk(token="AQAAAABaRy6FAAd_m-5FbN1cO0tlm6zg6uICmd8")
#
# print(y.check_token()) # Проверим токен
def sendYandexScreencast(name_video,video):
    token = "AQAAAABaRy6FAAd_m-5FbN1cO0tlm6zg6uICmd8"
    headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + token
    }

    params = {
        'path': f'Screencasts/{name_video}',
        'overwrite': True
    }

    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    r = requests.get(url=url, params=params, headers=headers)
    res = r.json()
    # print(json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False))
    # Отправляем локальный файл
    upload = requests.put(url=res['href'], data=open(f"C:/Users/v.glagolev/PycharmProjects/pythonProject1/screencasts/{video}", 'rb'), params=params, headers=headers)
    print(f"Статус загрузки видео - {upload.status_code}")


def getHref(video):
    token = "AQAAAABaRy6FAAd_m-5FbN1cO0tlm6zg6uICmd8"
    headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + token
    }

    params = {
        'path': f"Screencasts/{video}"
    }

    url = "https://cloud-api.yandex.net/v1/disk/resources/download"
    r = requests.get(url=url, params=params, headers=headers)
    res = r.json()
    json.dumps(r.json(), sort_keys=True, indent=4, ensure_ascii=False)

    return res['href']



# sendYandexScreencast("XiaomiRedmiNote9_P_cppk_12.11_12_11.mp4", "XiaomiRedmiNote9_P_dit_guest_wifi.mp4")
# # getHref()
