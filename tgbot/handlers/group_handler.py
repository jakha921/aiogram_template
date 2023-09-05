from aiogram import Dispatcher
from aiogram.types import Message, ContentType


async def echo(msg: Message):
    """Bot echo handler"""
    await msg.answer(msg.text)


async def group_greeting(msg: Message):
    """Greeting new user"""
    await msg.answer(f"Welcome to the group, {msg.new_chat_members[0].full_name}!")


async def group_bye(msg: Message):
    """Greeting new user"""
    if msg.left_chat_member.id == msg.from_user.id:
        await msg.answer(f"Goodbye, {msg.from_user.full_name}!")
    else:
        await msg.answer(f"{msg.left_chat_member.get_mention()} banned by {msg.from_user.full_name}!")


def register_group_handler(dp: Dispatcher):
    dp.register_message_handler(
        echo,
    ),
    dp.register_message_handler(
        group_greeting,
        content_types=ContentType.NEW_CHAT_MEMBERS
    ),
    dp.register_message_handler(
        group_bye,
        content_types=ContentType.LEFT_CHAT_MEMBER
    ),
