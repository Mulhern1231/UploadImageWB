import uuid
import requests
import simplejson as json

import os
from shutil import copyfile

#Артикул
articul = 8567702

#задаем значение для запроса на сервер
#Код авторизации
headers = {
    'accept': 'application/json',
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImViMmU1NGRjLTdkN2YtNDc5MS1hYWVjLTkxYjZhZTBhMmIzNCJ9.bNOPD9lahEA3HgUeJ-kT7b4QdRFj57vfasFSJopGobk'
}
#ЮРЛ для получения товара по артиклу
url = 'https://suppliers-api.wildberries.ru/card/list'
#JSON словарь для отправки на сервер (фильтр для поиска по артиклу)
data = {
  "id": 1,
  "jsonrpc": "2.0",
  "params": {
      "card": {
          "nomenclatures": [
              {
                  "nmId": articul,
              }
          ]
      }
  }
}

#Запрос на сервер и получение ответа
response = requests.post(url, headers=headers, data=json.dumps(data) )
d = json.loads(str(response.text))

#Запрос на сервер для получения imtID
url = 'https://suppliers-api.wildberries.ru/card/cardByImtID'
data = {
            "id": 1,
            "jsonrpc": "2.0",
            "params": {
                 "imtID": d["result"]["cards"][0]["imtId"]
             }
         }

response = requests.post(url, headers=headers, data=json.dumps(data))
templat = json.loads(str(response.text))
#################################

#Загрзка JSON файла (шаблона)
with open('data1.json') as f:
    newJSONFile = json.load(f)
newJSONFile = dict(newJSONFile)

#Загрузка в шаблон нужные значения для обновления карточки
newJSONFile["params"]["card"]["id"] = templat["result"]["card"]["id"]
newJSONFile["params"]["card"]["imtId"] = templat["result"]["card"]["imtId"]
newJSONFile["params"]["card"]["countryProduction"] = templat["result"]["card"]["countryProduction"]
newJSONFile["params"]["card"]["object"] = templat["result"]["card"]["object"]
newJSONFile["params"]["card"]["addin"] = templat["result"]["card"]["addin"]

newJSONFile["params"]["card"]["nomenclatures"][0]["nmId"] = templat["result"]["card"]["nomenclatures"][0]["nmId"]
newJSONFile["params"]["card"]["nomenclatures"][0]["vendorCode"] = templat["result"]["card"]["nomenclatures"][0]["vendorCode"]
newJSONFile["params"]["card"]["nomenclatures"][0]["addin"] = templat["result"]["card"]["nomenclatures"][0]["addin"]


loop = False

#Цикл проходящий по директории OLD
for i in os.listdir('OLD'):
#   Создание UID
    uid = uuid.uuid4()
    uid = str(uid).upper()
#    Копирование всех файлов с новым названием
    copyfile(f"OLD/{i}", f'NEW/{i}')
    os.rename(f'NEW/{i}', f"NEW/{uid}.jpeg")
#    Удаление старых фото из шаблона
    if loop == False:
        for i in newJSONFile["params"]["card"]["nomenclatures"][0]["addin"]:
            if "Фото" == i["type"]:
                i["params"].clear()
        loop = True
#    Переменная в которую загружается информация по фото
    newData = {'value': str(uid), 'units': 'images/jpeg'}
#    Добавление фото в шаблон
    for i in newJSONFile["params"]["card"]["nomenclatures"][0]["addin"]:
            if "Фото" == i["type"]:
                i["params"].append(newData)
#    Загрузка фото на сервер
    url = 'https://suppliers-api.wildberries.ru/card/upload/file/multipart'
    files = {
        'uploadfile': (f'NEW/{uid}.jpeg', open(f'NEW/{uid}.jpeg', 'rb')),
    }
    HEADERS = {
        'accept': 'application/json',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImViMmU1NGRjLTdkN2YtNDc5MS1hYWVjLTkxYjZhZTBhMmIzNCJ9.bNOPD9lahEA3HgUeJ-kT7b4QdRFj57vfasFSJopGobk',
        'X-File-id': str(uid),
    }
    response = requests.post(url, headers=HEADERS, files=files)

    print(response.text)

#обновление самой карточки 
url = 'https://suppliers-api.wildberries.ru/card/update'
response = requests.post(url, headers=headers, data=json.dumps(newJSONFile))
print(response.text)

