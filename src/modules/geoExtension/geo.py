import os
import aiohttp
from aiogram import types, Router
from aiogram.filters import Command

router = Router(name="geoExtension")

#Temporary Config
location = "Moscow"
zone = "EET"
language = "en"
meteoKey = os.getenv('METEO_API')

#Function to get the weather
@router.message(Command("meteo"))
async def meteo_handler(event: types.Message) -> None:
    url = f'https://www.meteosource.com/api/v1/free/point?place_id={location}&sections=daily&timezone={zone}&language={language}&units=metric&key={meteoKey}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            await event.answer(f"{data}")