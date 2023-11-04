from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.misc.utils import Map


async def phone_number(texts: Map):
    """Phone number inline keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.user.kb.reply.phone,
                            request_contact=True)],
            [KeyboardButton(text=texts.user.kb.reply.close)],
        ],
        resize_keyboard=True,
    )
    return keyboard


async def phone_and_location():
    """Phone number and location inline keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Send phone number", request_contact=True)
            ],
            [
                KeyboardButton(text="Send location", request_location=True)
            ],
            [KeyboardButton(text="Close")],
        ],
        resize_keyboard=True,
    )
    return keyboard
