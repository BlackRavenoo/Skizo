import os
import aiohttp
from aiogram import types, Router, Bot
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv
from modules.translateExtension import googletranslate

router = Router(name="geoExtension")
load_dotenv()
translator = googletranslate.GoogleTranslate()

#Temporary Config
#You can find your location here:
#https://www.meteosource.com/client/interactive-documentation
location = "Yelabuga"
zone = "Europe/Moscow"
language = "en"
meteoKey = os.getenv('METEO_API')
currencyKey = os.getenv('CURRENCY_API')

#Function to get the weather
#Command: /weather
#     or  /weather <day>
#Input: <day> - How many days before you need to know the weather (optional)
#Output: weather data or error message
@router.message(Command("weather"))
async def meteo_handler(event: types.Message,
                        command: CommandObject) -> None:
    try:
        ar = command.args.split()
        day = int(ar[0])
    except (AttributeError, ValueError):
        day = 0
    url = f'https://www.meteosource.com/api/v1/free/point?place_id={location}&sections=daily&timezone={zone}&language={language}&units=metric&key={meteoKey}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            result = translator.translate(data.get('daily').get('data')[day].get('summary'), target_language='ru')
            if(day == 0):
                await event.answer(f"**Ваш прогноз погоды на сегодня**:\n{result}", 
                    parse_mode='Markdown')
            else:
                await event.answer(f"**Через {day} дней ожидается следующая погода**:\n{result}", 
                    parse_mode='Markdown')

#Function to get the currency
#Command: /currency <cur0> <cur1> <amount>
#     or  /currency <cur0> <cur1>    
#Input: <cur0> - currency to convert, <cur1> - currency to convert to, 
# <amount> - amount of currency to convert (optional)
@router.message(Command("currency"))
async def currency_handler(event: types.Message,
                           command: CommandObject) -> None:
    try:
        ar = command.args.split()
        cur0 = ar[0]
        cur1 = ar[1]
    except Exception:
        await event.answer("Пожалуйста, введите команду в формате \n/currency <валюта1> <валюта2>.")
        return
    amount = 1
    if(len(ar) > 2):
        try:
            amount = int(ar[2])
        except(ValueError):
            await event.answer("Пожалуйста, введите команду в формате \n/currency <валюта1> <валюта2> <число>.")
            return
    if(len(cur0) != 3 or len(cur1) != 3):
        await event.answer("Пожалуйста, введите две валюты в формате \n/currency <валюта1> <валюта2>.")
        return
    url = f'https://v6.exchangerate-api.com/v6/{currencyKey}/pair/{cur0}/{cur1}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if(data['result'] == 'success'):
                await event.answer(f"При текущем курсе валют {amount} {cur0} равняется {data['conversion_rate'] * amount} {cur1}.")
            else:
                await event.answer("Сожалею, произошла ошибка при попытке получить курс валюты.")