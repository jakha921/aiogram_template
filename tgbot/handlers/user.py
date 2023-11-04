from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.handler import ctx_data

from loguru import logger

from tgbot.keyboards.inline import choose_language, cd_choose_lang
from tgbot.keyboards.reply import phone_number, phone_and_location
from tgbot.middlewares.translate import TranslationMiddleware
from tgbot.models.models import TGUser
from tgbot.misc.utils import Map, find_button_text
from tgbot.services.database import AsyncSession


async def user_start(msg: Message, db_session: AsyncSession, texts: Map):
    """User start command handler"""
    try:
        logger.info(f'User {msg.from_user.id} started the bot')

        # Register in the database if not registered
        db_user = await TGUser.get_user(db_session, telegram_id=msg.from_user.id)
        print('db_user', db_user)
        print('user', msg.from_user)

        if not db_user:
            logger.info('User not found in the database. Registering...')
            user = await TGUser.add_user(
                db_session=db_session,
                telegram_id=msg.from_user.id,
                firstname=msg.from_user.first_name,
                lastname=msg.from_user.last_name,
                username=msg.from_user.username,
                lang_code=msg.from_user.language_code
            )

            print('user', user)

            # Get total users count
            total = await TGUser.users_count(db_session)
            print('total', total)

            # Notify admin about the new registration
            config = msg.bot.get('config')
            for admin in config.tg_bot.admins_id:
                await msg.bot.send_message(admin, f"New user has been registered: {msg.from_user.get_mention()}")
                await msg.bot.send_message(admin, f"Total users: {total}")

        await msg.reply(f"Sava, {msg.from_user.get_mention()}")

    except Exception as e:
        logger.error(f"An error occurred in user_start: {e}")


async def user_me(m: Message, db_user: TGUser, texts: Map):
    """User me command handler"""
    logger.info(f'User {m.from_user.id} requested his info')
    await m.reply(texts.user.me.format(
        telegram_id=db_user.telegram_id,
        firstname=db_user.firstname,
        lastname=db_user.lastname,
        username=db_user.username,
        phone=db_user.phone,
        lang_code=db_user.lang_code))


async def user_close_reply_keyboard(m: Message, texts: Map):
    """User close reply keyboard button handler"""
    logger.info(f'User {m.from_user.id} closed reply keyboard')
    await m.reply(texts.user.close_reply_keyboard, reply_markup=ReplyKeyboardRemove())


async def user_phone(m: Message, texts: Map):
    """User phone command handler"""
    logger.info(f'User {m.from_user.id} requested phone number')
    await m.reply(texts.user.phone, reply_markup=await phone_number(texts))


async def user_phone_sent(m: Message, texts: Map, db_user: TGUser, db_session: AsyncSession):
    """User contact phone receiver handler"""
    logger.info(f'User {m.from_user.id} sent phone number')

    number = m.contact.phone_number

    # if number not start with +, add +
    if not number.startswith('+'):
        number = '+' + number

    # updating user's phone number
    await TGUser.update_user(db_session,
                             telegram_id=db_user.telegram_id,
                             updated_fields={'phone': number})
    await m.reply(texts.user.phone_saved, reply_markup=ReplyKeyboardRemove())


async def user_lang(m: Message, texts: Map):
    """User lang command handler"""
    logger.info(f'User {m.from_user.id} requested language')
    await m.reply(texts.user.lang, reply_markup=await choose_language(texts))


async def user_lang_choosen(cb: CallbackQuery, callback_data: dict,
                            texts: Map, db_user: TGUser, db_session: AsyncSession):
    """User lang choosen handler"""
    logger.info(f'User {cb.from_user.id} choosed language')
    code = callback_data.get('lang_code')
    await TGUser.update_user(db_session,
                             telegram_id=db_user.telegram_id,
                             updated_fields={'lang_code': code})

    # manually load translation for user with new lang_code
    texts = await TranslationMiddleware().reload_translations(cb, ctx_data.get(), code)
    btn_text = await find_button_text(cb.message.reply_markup.inline_keyboard, cb.data)
    await cb.message.edit_text(texts.user.lang_choosen.format(lang=btn_text), reply_markup='')


async def bar(msg: Message):
    """Bar command handler"""
    await msg.reply("Bar", reply_markup=await phone_and_location())


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start,
        commands=["start"],
        state="*"
    )
    dp.register_message_handler(
        user_me,
        commands=["me"],
        state="*"
    )
    dp.register_message_handler(
        user_phone,
        commands=["phone"],
        state="*"
    )
    dp.register_message_handler(
        user_lang,
        commands=["lang"],
        state="*"
    )
    dp.register_message_handler(
        user_close_reply_keyboard,
        is_close_btn=True,
        state="*"
    )
    dp.register_message_handler(
        user_phone_sent,
        content_types=["contact"],
        state="*"
    )
    dp.register_callback_query_handler(
        user_lang_choosen,
        cd_choose_lang.filter(),
        state="*",
    )
    dp.register_message_handler(
        bar,
        commands=["foo"],
        state="*",
    )
