from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter


class PrivateChatFilter(BoundFilter):
    """Filter for checking if message is from private chat"""

    async def check(self, message: Message):
        # return message.chat.type == 'private'
        return message.chat.type == ChatType.PRIVATE
