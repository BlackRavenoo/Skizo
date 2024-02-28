from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

class ActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        operation_type = get_flag(data, "operation_type")

        if not operation_type:
            return await handler(event, data)
        
        if event.bot is None:
            print("Something went wrong")
            return await handler(event, data)

        async with ChatActionSender(
            action=operation_type,
            chat_id=event.chat.id,
            bot=event.bot,
        ):
            return await handler(event, data)