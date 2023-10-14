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
