import requests
from requests.adapters import HTTPAdapter
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from urllib3 import Retry

from config import BOT_TOKEN


def get_json(adress):
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    server_address = 'https://geocode-maps.yandex.ru/1.x/?'
    geocoder_request = f'{server_address}apikey={api_key}&geocode={adress}&format=json'
    response = requests.get(geocoder_request)
    return response


def get_response_map(ll):
    server_address = "https://static-maps.yandex.ru/v1"
    apikey = '0eea7a3e-806e-4b45-8976-3c543752e89c'
    map_params = {
        'll': ll,
        'apikey': apikey,
        'pt': ll,
        'z': 15
    }
    session = requests.Session()
    retry = Retry(total=10, connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    response = requests.get(server_address, params=map_params)
    return response


async def start(update, context):
    await update.message.reply_text('Это Бот-геокодер\nВведите адрес объекта, который вы хотите увидеть на карте')


async def search_geo(update, context):
    res = get_json(update.message.text)
    if res.status_code != 200:
        return await update.message.reply_text(
            f'Ошибка на сервере поробуйте повторить запрос позже\nКод ошибки {res.status_code}')

    res = res.json()['response']['GeoObjectCollection']['featureMember']
    if not res:
        return await update.message.reply_text(
            'Неверно указан адрес, попробуйте указать его сново, проверив правильность написания')
    point = ','.join(res[0]['GeoObject']['Point']['pos'].split(' '))

    map = get_response_map(point)
    if map.status_code != 200:
        return await update.message.reply_text(
            f'Ошибка на сервере поробуйте повторить запрос позже\nКод ошибки {map.status_code}')
    caption = f"На карте показан объект - {res[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']}"
    await update.message.reply_photo(photo=map.content, caption=caption)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_geo))

    application.run_polling()


if __name__ == '__main__':
    main()
