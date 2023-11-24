import aiohttp
from aiogram import types, Router, Bot
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv
from modules.translateExtension import googletranslate
import os

router = Router(name="translateExtension")
load_dotenv()
translator = googletranslate.GoogleTranslate()

#Function to translate the message or file
#Command: /translate <lang> <text>
#     or  /translate <lang> <file>
#Input: <lang> - language to translate, <text/file> - text to translate
#Output: translated text or error message
@router.message(Command("translate"))
async def translate_handler(event: types.Message,
                           command: CommandObject,
                           bot: Bot) -> None:
    #Getting base parameters
    if not(txt := command.args):
        await event.answer("Пожалуйста, введите команду в формате \n/translate <язык> <текст>.")
        return
    try:
        msg = txt[3:len(txt)]
        lang = txt[0:2]
    except(IndexError):
        await event.answer("Пожалуйста, введите команду в формате \n/translate <язык> <текст>.")
        return
    
    #If user send file
    try:
        if event.document is not None:
            try:
                file_extension = event.document.file_name.rsplit('.', 1)[1]
            except(IndexError):
                file_extension = "txt"
            file_id = event.document.file_id
            file_path = (await bot.get_file(file_id)).file_path
            await bot.download_file(file_path, f"{file_id}.{file_extension}")
            async with aiohttp.ClientSession():
                result = translator.translate_file(file_path=f"{file_id}.{file_extension}", target_language=lang)
                await event.answer(result)
                os.remove(f"{file_id}.{file_extension}")
    except(UnicodeDecodeError):
        await event.answer("Кто... кто здесь!?\nЯ не могу распознать этот файл!")
        return
    
    #If user send text
    result = translator.translate(msg, target_language=lang)
    await event.answer(result)