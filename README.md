# Group bot

## Description

This is a bot that can be used to manage groups in a Telegram chat.

## Usage

```python
# handles/group_handler.py

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

```

```python
def register_all_handlers(dp: Dispatcher):
    """Register all handlers"""
    register_admin(dp)
    register_user(dp)
    register_testing(dp)
    register_menu(dp)
    register_new_menu(dp)
    register_formatting_text(dp)
    register_group_handler(dp)
    register_echo(dp)
```

## Filters

```python
# filters/role.py

# filters/group.py

from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class GroupChatFilter(BoundFilter):
    """Filter for checking if message is from group"""

    async def check(self, message: Message):
        return message.chat.type in ['group', 'supergroup']


# filters/private.py

from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class PrivateChatFilter(BoundFilter):
    """Filter for checking if message is from private chat"""

    async def check(self, message: Message):
        return message.chat.type == 'private'
```

```python
# handlers/group_manager.py

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
```

```python

# handlers/user.py

...

def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start,
        PrivateChatFilter(), <- filter
        CommandStart()
        # commands=["/start"],
        # commands=["start"],
        # state="*",
    )
```

```python
# bot.py
# register filters

def register_all_filters(dp: Dispatcher):
    """Register all filters"""
    dp.filters_factory.bind(role.AdminFilter)
    dp.filters_factory.bind(GroupChatFilter)
    dp.filters_factory.bind(PrivateChatFilter)
    dp.filters_factory.bind(reply_kb.CloseBtn)

```

## Moderator bot

```python
import asyncio
import datetime
import re

import aiogram
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from tgbot.filters.group import GroupChatFilter
from tgbot.filters.role import AdminFilter


# /ro oki !ro (read-only) komandalari uchun handler
# foydalanuvchini read-only ya'ni faqat o'qish rejimiga o'tkazib qo'yamiz.
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5

    """
    !ro 
    !ro 5 
    !ro 5 test
    !ro test
    !ro test test test
    /ro 
    /ro 5 
    /ro 5 test
    /ro test
    """
    # 5-minutga izohsiz cheklash
    # !ro 5
    # command='!ro' time='5' comment=[]

    # 50 minutga izoh bilan cheklash
    # !ro 50 reklama uchun ban
    # command='!ro' time='50' comment=['reklama', 'uchun', 'ban']

    time = int(time)

    # Ban vaqtini hisoblaymiz (hozirgi vaqt + n minut)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    try:
        await message.chat.restrict(user_id=member_id, can_send_messages=False, until_date=until_date)
        await message.reply_to_message.delete()
    except aiogram.utils.exceptions.BadRequest as err:
        await message.answer(f"Error: {err.args}")
        return

    # Пишем в чат
    await message.answer(
        f"User {message.reply_to_message.from_user.full_name} was deprived of the right to write {time} minutes.\n")
    if comment: await message.answer(f"Comment: {comment}")

    service_message = await message.reply("The message goes out after 5 seconds.")
    # 5 sekun kutib xabarlarni o'chirib tashlaymiz
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


# read-only holatdan qayta tiklaymiz
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )
    service_message = await message.reply("The message goes out after 5 seconds.")

    await asyncio.sleep(5)
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    await message.reply(f"User {member.full_name} restored")

    # xabarlarni o'chiramiz
    await message.delete()
    await service_message.delete()


# Foydalanuvchini banga yuborish (guruhdan haydash)
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)

    await message.answer(f"User {message.reply_to_message.from_user.full_name} expelled from the group")
    service_message = await message.reply("The message goes out after 5 seconds.")

    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


# Foydalanuvchini bandan chiqarish, foydalanuvchini guruhga qo'sha olmaymiz (o'zi qo'shilishi mumkin)
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.unban(user_id=member_id)
    await message.answer(f"User {message.reply_to_message.from_user.full_name} out of the band")
    service_message = await message.reply("The message goes out after 5 seconds.")

    await asyncio.sleep(5)

    await message.delete()
    await service_message.delete()


def register_group_moderator(dp: Dispatcher):
    dp.register_message_handler(
        read_only_mode,
        GroupChatFilter(),
        Command("ro", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
    dp.register_message_handler(
        undo_read_only_mode,
        GroupChatFilter(),
        Command("unro", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
    dp.register_message_handler(
        ban_user,
        GroupChatFilter(),
        Command("ban", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
    dp.register_message_handler(
        unban_user,
        GroupChatFilter(),
        Command("unban", prefixes="!/"),
        AdminFilter(is_admin=True)
    )
```

```python
# bot.py

...


def register_all_handlers(dp: Dispatcher):
    """Register all handlers"""
    register_admin(dp)
    register_user(dp)
    register_testing(dp)
    register_menu(dp)
    register_new_menu(dp)
    register_formatting_text(dp)
    register_manage_chat(dp)
    register_group_moderator(dp)
    register_group_handler(dp)
    register_echo(dp)
```