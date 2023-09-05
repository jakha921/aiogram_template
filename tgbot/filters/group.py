from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class GroupChatFilter(BoundFilter):
    """Filter for checking if message is from group"""

    async def check(self, message: Message):
        return message.chat.type in ['group', 'supergroup']
