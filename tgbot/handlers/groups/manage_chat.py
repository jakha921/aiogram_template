import io

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import Message

from tgbot.filters.group import GroupChatFilter
from tgbot.filters.role import AdminFilter


async def start(msg: Message):
    """Bot start handler"""
    await msg.answer(f"Hello, {msg.from_user.full_name}, Welcome to the group!")


async def set_new_photo(msg: Message):
    """Bot set new photo handler"""

    # Get the message to which the user is replying (the source message)
    source_message = msg.reply_to_message

    # Check if there is no source message to reply to
    if not source_message:
        await msg.answer("Reply to a message with a photo")
        return

    # Get the last (largest) photo in the source message
    photo = source_message.photo[-1]

    # Download the photo and store it in a BytesIO object
    photo = await photo.download(destination=io.BytesIO())

    # Create an InputFile from the downloaded photo
    input_file = types.InputFile(photo)

    # Set the chat's photo to the downloaded photo
    await msg.chat.set_photo(input_file)


async def set_new_title(msg: Message):
    """Bot set new title handler"""

    # Get the message to which the user is replying (the source message)
    source_message = msg.reply_to_message

    # Check if there is no source message to reply to
    if not source_message:
        await msg.answer("Reply to a message with a title")
        return

    # Get the text of the source message
    title = source_message.text

    # Set the chat's title to the text of the source message
    await msg.chat.set_title(title)


async def set_new_description(msg: Message):
    """Bot set new description handler"""

    # Get the message to which the user is replying (the source message)
    source_message = msg.reply_to_message

    # Check if there is no source message to reply to
    if not source_message:
        await msg.answer("Reply to a message with a description")
        return

    # Get the text of the source message
    description = source_message.text

    # Set the chat's description to the text of the source message
    await msg.chat.set_description(description)


def register_manage_chat(dp: Dispatcher):
    dp.register_message_handler(
        start,
        GroupChatFilter(),
        CommandStart()
    )
    dp.register_message_handler(
        set_new_photo,
        GroupChatFilter(),
        Command("set_new_photo", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
    dp.register_message_handler(
        set_new_title,
        GroupChatFilter(),
        Command("set_new_title", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
    dp.register_message_handler(
        set_new_description,
        GroupChatFilter(),
        Command("set_new_description", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
