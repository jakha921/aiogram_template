from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.misc.utils import Map


async def menu_keyboard():
    """Menu inline keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🍣 Sushi"),
            ],
            [
                KeyboardButton(text="🍕 Pizza"),
                KeyboardButton(text="🍔 Burger"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard


async def type_sushi_keyboard():
    """Type of sushi reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🐟 Fish"),
                KeyboardButton(text="🍚 Rice"),
            ],
            [
                KeyboardButton(text="🍗 Chicken"),
                KeyboardButton(text="🥑 Vegetarian"),
                KeyboardButton(text="🥩 Meat"),
            ],
            [
                KeyboardButton(text="📋 Menu"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard


async def phone_number(texts: Map):
    """Phone number inline keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=texts.user.kb.reply.phone, request_contact=True)
            ],
            # location
            [
                KeyboardButton(text="📍 Location", request_location=True)
            ],
            [
                KeyboardButton(text=texts.user.kb.reply.close)
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
