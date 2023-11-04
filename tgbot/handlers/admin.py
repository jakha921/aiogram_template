from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from tgbot.services.database import AsyncSession
from tgbot.models.models import TGUser
from tgbot.misc.broadcast import broadcast
from tgbot.misc.utils import Map


async def admin_start(msg: Message, texts: Map):
    """Admin start command handler"""
    logger.info(f'Admin {msg.from_user.id} opened admin panel')
    await msg.reply(texts.admin.hi)


async def admin_stats(m: Message, db_session: AsyncSession, texts: Map):
    """Admin stats command handler"""
    logger.info(f'Admin {m.from_user.id} requested stats')
    count = await TGUser.users_count(db_session)
    await m.reply(texts.admin.total_users.format(count=count))


async def admin_broadcast(m: Message, db_session: AsyncSession, texts: Map):
    """Admin broadcast command handler"""
    logger.info(f'Admin {m.from_user.id} requested broadcast')
    broadcast_text = m.text.replace("/broadcast", "")
    if not broadcast_text:
        # there must be some text after command for broadcasting
        await m.reply(texts.admin.no_broadcast_text)
        return
    users = await TGUser.get_all_users(db_session)
    try:
        await m.reply(texts.admin.broadcast_started)
        logger.success(f'Broadcast started.')
        await broadcast(broadcast_text, users)
        logger.success(f'Broadcast finished.')
        await m.reply(texts.admin.broadcast_ended)
    except Exception as e:
        await m.reply(texts.admin.broadcast_error.format(err=e))
        logger.error("Error while broadcasting!")
        logger.exception(e)


async def admin_send_message(msg: Message, db_session: AsyncSession):
    """
    Admin send message command handler
    get reply message and send it to all users
    """
    logger.info(f'Admin {msg.from_user.id} requested send message')
    users = await TGUser.get_all_users(db_session)
    try:
        post = msg.reply_to_message
        if not post:
            await msg.reply("Reply to message for sending to users")
            return
        await msg.reply("Sending message...")
        for user in users:
            try:
                if user.telegram_id == msg.from_user.id:
                    continue
                await post.copy_to(user.telegram_id)
            except Exception as e:
                logger.exception(e)
                logger.error(f"Error while sending message to user {user.telegram_id}")
        await msg.reply("Message sent!")
    except Exception as e:
        await msg.reply(f"Error while sending message: {e}")
        logger.error("Error while sending message!")
        logger.exception(e)


async def send_to_en_users(msg: Message, db_session: AsyncSession):
    eng_post = msg.reply_to_message

    if not eng_post:
        await msg.reply("Reply to message for sending to users")
        return

    en_users = await TGUser.get_all_users_by_filter(db_session)
    print('en_users', en_users)

    for user in en_users:
        try:
            if user.telegram_id == msg.from_user.id:
                continue
            await eng_post.copy_to(user.telegram_id)
        except Exception as e:
            logger.exception(e)
            logger.error(f"Error while sending message to user {user.telegram_id}")
    await msg.reply("Message sent!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start,
        commands=["admin"],
        state="*",
        is_admin=True
    )
    dp.register_message_handler(
        admin_stats,
        commands=["stats"],
        state="*",
        is_admin=True
    )
    dp.register_message_handler(
        admin_broadcast,
        commands=["broadcast"],
        state="*",
        is_admin=True
    )
    dp.register_message_handler(
        admin_send_message,
        commands=["send_post"],
        state="*",
        is_admin=True
    )
    dp.register_message_handler(
        send_to_en_users,
        commands=['en_post'],
        state='*',
        is_admin=True
    )
