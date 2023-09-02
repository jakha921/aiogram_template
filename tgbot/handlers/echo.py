from aiogram import types

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandHelp, Text, Regexp
from aiogram.types import Message
from loguru import logger


async def bot_echo(msg: Message):
    """Bot echo handler"""
    logger.info(f'User {msg.from_user.id} sent message: {msg.text}')

    text = f"Echo: \n{msg.text}"

    print(f'message: {msg}')

    await msg.answer(text)
    # await msg.reply(text)


async def bot_help(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} requested help')
    text = "Help message"
    await msg.answer(text)


async def get_photo(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} send photo')
    await msg.answer("I can`t work with photos yet:(")


async def get_file(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} send file')
    await msg.answer("I can`t work with such files yet:(")


async def greet_user(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} greeted')
    await msg.answer(f"Assalomu alaykum, {msg.from_user.first_name}!")


async def spam(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} spam')
    await msg.answer(f"Spam")

async def get_email(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} send email')
    await msg.answer(f"Now I can`t do smth with emails sorry!")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(
        bot_help,
        CommandHelp(),
        state="*"
    ),
    dp.register_message_handler(
        get_photo,
        content_types=(types.ContentType.PHOTO, types.ContentType.DOCUMENT),
        # content_types=['photo', 'document'],
    ),
    dp.register_message_handler(
        get_file,
        content_types=(types.ContentType.DOCUMENT, types.ContentType.VIDEO, types.Voice),
        # content_types=['document', 'video', 'voice'],
    ),
    dp.register_message_handler(
        greet_user,
        Text(equals="Assalomu alaykum"),
        Text(contains="salom")
    ),
    dp.register_message_handler(
        spam,
        Text(endswith="spam"),
        Text(contains="spam"),
        Text(startswith="spam"),
    ),
    dp.register_message_handler(
        get_email,
        Regexp(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")
    ),
    dp.register_message_handler(
        bot_echo,
        state="*",  # for all states
    )
