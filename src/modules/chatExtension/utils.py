from enum import Enum
import os
import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import PATH_TO_CHATS
from modules.modules import modules_config
from modules.chatExtension.api import openai, oobabooga

class Providers(Enum):
    OOBABOOGA = 0
    AI_HORDE = 1
    OPENROUTER = 2
    OPENAI = 3
    AI21 = 4

class Modes(Enum):
    CHAT = 0
    COMPLETION = 1

class States(StatesGroup):
    idle = State()
    chat = State()

def get_chat_menu_keyboard() -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(text="Начать", callback_data="start_chat")
    btn2 = InlineKeyboardButton(text="Настройки", callback_data="chat_settings")
    btn3 = InlineKeyboardButton(text="Выход", callback_data="end_chat")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2, btn3]])
    return keyboard

def get_chat_settings_keyboard() -> InlineKeyboardMarkup:
    btn1 = InlineKeyboardButton(text="Изменить провайдера", callback_data="change_provider")
    btn2 = InlineKeyboardButton(text="Настройки провайдера", callback_data="provider_settings")
    btn3 = InlineKeyboardButton(text="Назад", callback_data="back_to_chat")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2], [btn3]])
    return keyboard

async def create_new_chat(user_name: str, state: FSMContext) -> None:
    chats_list = get_chats_list()
    chat_id = 0
    if chats_list != []:
        chat_id = max(chats_list) + 1
    with open(f"{PATH_TO_CHATS}{chat_id}.jsonl", "w") as f:
        json.dump({"user_name": user_name}, f, ensure_ascii=False)
        f.write("\n")
    await state.update_data(chat_id=chat_id)

async def update_chat(state: FSMContext, message: str) -> str:
    chat_id = (await state.get_data())["chat_id"]
    with open(f"{PATH_TO_CHATS}{chat_id}.jsonl", "r") as f: #TODO Error handling
        chats = [json.loads(line) for line in f]
        add_message_to_chat(chat_id, {"role": "user", "content": message})
        message = await get_answer_from_chat(message, chat_id)
        add_message_to_chat(chat_id, {"role": "bot", "content": message})
        return message
    

async def get_answer_from_chat(message, chat_id) -> str:
    settings = get_chat_settings()
    provider: Providers = settings["provider"]
    mode: Modes = settings["mode"]
    #Тут асинхронный запрос, вывод сообщения "Ожидайте ответа" или что-то в этом роде + отображение статуса "Печатает..."
    if provider == Providers.OOBABOOGA:
        if mode == Modes.COMPLETION:

            json = {
                "prompt": message,
                "max_tokens": settings["max_tokens"],
                "temperature": settings["temperature"],
                "top_p": settings["top_p"],
            }
            #Добавить другие настройки и доделать вызов
            return (await oobabooga.completion(json=json))['choices'][0]['text'] # type: ignore
        elif mode == Modes.CHAT:
            messages = get_chat_messages(chat_id)
            if messages is not None:
                messages.append({"role": "user", "content": message})
            else:
                raise RuntimeError("Messages is None") #TODO
            json = {
                "messages": messages,
                "max_tokens": settings["max_tokens"],
                "temperature": settings["temperature"],
                "top_p": settings["top_p"],
                "mode": "instruct",
                "instruction_template": "Alpaca",
            }
            return (await oobabooga.chat_completion(json=json))['choices'][0]['message']['content'] # type: ignore
    return "" #TODO
    

def get_chat_messages(chat_id: str) -> list|None:
    try:
        with open(f"{PATH_TO_CHATS}/{chat_id}.jsonl", "r") as f:
            next(f)
            messages = [json.loads(line) for line in f]
            return messages
    except Exception as e:
        print(e)

def add_message_to_chat(chat_id: str, message: dict) -> None:
    try:
        with open(f"{PATH_TO_CHATS}/{chat_id}.jsonl", "a") as f:
            json.dump(message, f, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        print(f"add_message_to_chat: {e}")

def get_chats_list() -> list[int]:
    return [int(x.replace(".jsonl", "")) for x in os.listdir(PATH_TO_CHATS) if ".jsonl" in x]
            

def get_chat_settings() -> dict:
    #TODO
    return {
        "provider": Providers.OOBABOOGA,
        "mode": Modes.CHAT,
        "max_tokens": 96,
        "temperature": 0.7,
        "top_p": 1,
    }
