from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.handler import ctx_data

from loguru import logger

from tgbot.filters.private import PrivateChatFilter
from tgbot.keyboards.inline import choose_language, cd_choose_lang
from tgbot.keyboards.reply import phone_number
from tgbot.middlewares.translate import TranslationMiddleware
from tgbot.models.models import TGUser
from tgbot.misc.utils import Map, find_button_text
from tgbot.services.database import AsyncSession


# deep_linking
async def user_start(msg: Message, texts: Map):
    """User start command handler"""
    logger.info(f'User {msg.from_user.id} in private chat started the bot')

    # use deep_linking to get deep link data
    deep_link = msg.get_args()

    text = texts.user.hi.format(mention=msg.from_user.get_mention())
    if deep_link:
        text += f'\n\nYou came with deep link: {deep_link}'
    await msg.reply(text)


async def user_me(msg: Message, db_user: TGUser, texts: Map):
    """User me command handler"""
    logger.info(f'User {msg.from_user.id} requested his info')
    await msg.reply(texts.user.me.format(
        telegram_id=db_user.telegram_id,
        firstname=db_user.firstname,
        lastname=db_user.lastname,
        username=db_user.username,
        phone=db_user.phone,
        lang_code=db_user.lang_code))


async def user_close_reply_keyboard(msg: Message, texts: Map):
    """User close reply keyboard button handler"""
    logger.info(f'User {msg.from_user.id} closed reply keyboard')
    await msg.reply(texts.user.close_reply_keyboard, reply_markup=ReplyKeyboardRemove())


async def user_phone(msg: Message, texts: Map):
    """User phone command handler"""
    logger.info(f'User {msg.from_user.id} requested phone number')
    await msg.reply(texts.user.phone, reply_markup=await phone_number(texts))


async def user_phone_sent(msg: Message, texts: Map, db_user: TGUser, db_session: AsyncSession):
    """User contact phone receiver handler"""
    logger.info(f'User {msg.from_user.id} sent phone number')

    number = msg.contact.phone_number

    # if number not start with +, add +
    if not number.startswith('+'):
        number = '+' + number

    # updating user's phone number
    await TGUser.update_user(db_session,
                             telegram_id=db_user.telegram_id,
                             updated_fields={'phone': number})
    await msg.reply(texts.user.phone_saved, reply_markup=ReplyKeyboardRemove())


async def user_lang(msg: Message, texts: Map):
    """User lang command handler"""
    logger.info(f'User {msg.from_user.id} requested language')
    await msg.reply(texts.user.lang, reply_markup=await choose_language(texts))


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


def register_user(dp: Dispatcher):
    # dp.register_message_handler(
    #     user_start,
    #     PrivateChatFilter(),
    #     # CommandStart()
    #     # commands=["/start"],
    #     # commands=["start"],
    #     # state="*",
    # )
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
