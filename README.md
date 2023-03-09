
# Описание

Эта программа позволяет обновлять фотографии товаров на Wildberries. Вы можете легко загружать фотографии из папки NEW и обновлять товары на Wildberries с помощью этой программы.

# Установка

Для использования этой программы вам понадобится установить несколько библиотек. Вы можете установить их из файла `requirements.txt`, выполнив команду:

Copy code

`pip install -r requirements.txt` 

# Как пользоваться

1.  Клонируйте репозиторий на свой локальный компьютер `git clone https://github.com/Mulhern1231/UploadImageWB.git`
2. Вписать внутри файла  `main.py`  артикул товара `articul` Вместо `API_KEY` вставьте свой API ключ для Wildberries.

3.  Поместите фотографии, которые вы хотите загрузить, в папку `NEW`
5.  Запустите файл `main.py`

Программа загрузит все фотографии из папки `NEW` на ваш товар на Wildberries. Программа также сохранит все описания и характеристики товара, так что вам не нужно беспокоиться о потере информации.