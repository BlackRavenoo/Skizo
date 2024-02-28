from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from config import bot_config

class IsOwnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]],Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.from_user and event.from_user.id != bot_config["owner_id"]:
            return True
        if isinstance(event, CallbackQuery) and event.from_user.id != bot_config["owner_id"]:
            return True
        return await handler(event, data)