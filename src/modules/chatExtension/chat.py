from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from modules.chatExtension.utils import get_chat_menu_keyboard, create_new_chat, update_chat, States

router = Router(name="chatExtension")

@router.message(Command("chat"))
async def chat_menu_handler(event: types.Message):
    await event.answer("Don't use this module. It's not implemented yet.\n"
                       "Не используйте этот модуль. Он еще не реализован.\n"
                       "Привет! Я чат-бот. Выбери необходимые настройки и начинай диалог.", reply_markup=get_chat_menu_keyboard())

@router.message(States.chat and Command("end"))
async def end_handler(event: types.Message, state: FSMContext):
    await state.set_state(States.idle)
    await event.answer("Диалог завершен!")

@router.callback_query(lambda event: event.data == "end_chat")
async def end_chat_callback_handler(event: types.CallbackQuery, state: FSMContext):
    await event.answer("Диалог завершен!")

@router.message(States.chat, flags={"operation_type": "typing"})
async def chat_handler(event: types.Message, state: FSMContext):
    try:
        if event.text is not None:
            message: str = await update_chat(state, event.text)
            if message == "":
                message = "Something went wrong. Please, try again."
            await event.answer(message)
    except FileNotFoundError:
        await event.answer("Случилась ошибка с файлом диалога. Попробуйте начать диалог заново.")

@router.callback_query(lambda event: event.data == "start_chat")
async def start_chat_callback_handler(
        event: types.CallbackQuery,
        state: FSMContext,
        bot: Bot
) -> None:
    await bot.send_message(event.from_user.id, 'Начат новый диалог с ботом!')
    await state.set_state(States.chat)
    await create_new_chat(event.from_user.first_name, state)
    await event.answer()

#TODO Callbacks start_chat, chat_settings, change_provider, provider_settings, back_to_chat