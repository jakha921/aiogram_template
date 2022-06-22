from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.handler import ctx_data

from loguru import logger

from tgbot.keyboards.inline import choose_language, cd_choose_lang
from tgbot.keyboards.reply import phone_number
from tgbot.middlewares.translate import TranslationMiddleware
from tgbot.models.users import User
from tgbot.misc.utils import Map, find_button_text
from tgbot.services.database import AsyncSession


async def user_start(m: Message, texts: Map):
    await m.reply(texts.user.hi.format(mention=m.from_user.get_mention()))


async def user_me(m: Message, db_user: User, texts: Map):
    await m.reply(texts.user.me.format(
        telegram_id=db_user.telegram_id,
        firstname=db_user.firstname,
        lastname=db_user.lastname,
        username=db_user.username,
        phone=db_user.phone,
        lang_code=db_user.lang_code))


async def user_close_reply_keyboard(m: Message, texts: Map):
    await m.reply(texts.user.close_reply_keyboard, reply_markup=ReplyKeyboardRemove())


async def user_phone(m: Message, texts: Map):
    await m.reply(texts.user.phone, reply_markup=await phone_number(texts))


async def user_phone_sent(m: Message, texts: Map, db_user: User, db_session: AsyncSession):
    number = m.contact.phone_number

    if not number.startswith('+'):
        number = '+' + number

    await User.update_user(db_session,
                           telegram_id=db_user.telegram_id,
                           updated_fields={'phone': number})
    await m.reply(texts.user.phone_saved, reply_markup=ReplyKeyboardRemove())


async def user_lang(m: Message, texts: Map):
    await m.reply(texts.user.lang, reply_markup=await choose_language(texts))


async def user_lang_choosen(cb: CallbackQuery, callback_data: dict,
                            texts: Map, db_user: User, db_session: AsyncSession):
    code = callback_data.get('lang_code')
    await User.update_user(db_session,
                           telegram_id=db_user.telegram_id,
                           updated_fields={'lang_code': code})
    texts = await TranslationMiddleware().reload_translations(cb, ctx_data.get(), code)
    btn_text = await find_button_text(cb.message.reply_markup.inline_keyboard, cb.data)
    await cb.message.edit_text(texts.user.lang_choosen.format(lang=btn_text), reply_markup='')


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
