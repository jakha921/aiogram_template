from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.callback_data import sub_menu_callback, sushi_type_callback
from tgbot.misc.utils import Map

cd_choose_lang = CallbackData("choosen_language", "lang_code")


async def choose_language(texts: Map):
    """Choose language inline keyboard"""
    # get languages from translation texts
    langs: Map = texts.user.kb.inline.languages
    keyboard = []
    for k, v in langs.items():
        keyboard.append(InlineKeyboardButton(
            v.text, callback_data=cd_choose_lang.new(lang_code=k)))
    return InlineKeyboardMarkup(
        inline_keyboard=[keyboard], row_width=len(langs.items())
    )


# 1 method
async def new_menu_keyboard():
    """Course menu inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📋 Our menu", callback_data="sub_menu"),
            InlineKeyboardButton("📣 Discounts", callback_data="discounts"),
        ],
        [
            InlineKeyboardButton("🌐 Our site", url="https://www.google.com"),
        ],
        [
            InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat=""),
        ],
        [
            InlineKeyboardButton("📨 Send feedback", switch_inline_query="Good bot!"),
        ],
        [
            InlineKeyboardButton("📸 Get logo", callback_data="get_logo"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# 2 method
async def discounts_keyboard():
    """Course menu inline keyboard"""
    menu_keyboards = InlineKeyboardMarkup(row_width=1)
    menu_keyboards.add(
        InlineKeyboardButton("20%", callback_data="20"),
        InlineKeyboardButton("30%", callback_data="30"),
        InlineKeyboardButton("40%", callback_data="40"),
        InlineKeyboardButton("50%", callback_data="50"),
        InlineKeyboardButton("🔙 Back", callback_data="cancel")
    )
    return menu_keyboards


# 3 method
async def sub_menu_keyboard():
    """Course menu inline keyboard"""

    products = [
        {'text': '🍣 Sushi', 'callback_data': 'sushi'},
        {'text': '🍕 Pizza', 'callback_data': 'pizza'},
        {'text': '🍔 Burger', 'callback_data': 'burger'},
        {'text': '🍟 French fries', 'callback_data': 'french_fries'},
        {'text': '🥗 Salad', 'callback_data': 'salad'},
        {'text': '🍦 Ice cream', 'callback_data': 'ice_cream'},
        {'text': '🍩 Donut', 'callback_data': 'donut'},
        {'text': '🍫 Chocolate', 'callback_data': 'chocolate'},
        {'text': '🍭 Lollipop', 'callback_data': 'lollipop'},
        {'text': '🍿 Popcorn', 'callback_data': 'popcorn'},
        {'text': '🍪 Cookies', 'callback_data': 'cookies'},
        {'text': '🍩 Donut', 'callback_data': 'donut'},
        {'text': '🍫 Chocolate', 'callback_data': 'chocolate'}
    ]
    menu_keyboards = InlineKeyboardMarkup(row_width=3)
    for product in products:
        menu_keyboards.insert(
            InlineKeyboardButton(
                text=product['text'],
                callback_data=sub_menu_callback.new(product_name=product['callback_data']))
        )

    menu_keyboards.insert(
        InlineKeyboardButton("🔙 Back", callback_data="cancel")
    )
    return menu_keyboards


async def type_sushi_keyboard():
    """Course menu inline keyboard"""
    menu_keyboards = InlineKeyboardMarkup(row_width=2)
    menu_keyboards.add(
        InlineKeyboardButton("🐟 Fish", callback_data=sushi_type_callback.new(from_sushi='fish')),
        InlineKeyboardButton("🍚 Rice", callback_data="type_sushi:rice"),
        InlineKeyboardButton("🍗 Chicken", callback_data="type_sushi:chicken"),
        InlineKeyboardButton("🥑 Vegetarian", callback_data="type_sushi:vegetarian"),
        InlineKeyboardButton("🥩 Meat", callback_data="type_sushi:meat"),
    )
    return menu_keyboards


async def check_button():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Confirm", callback_data='check_subs')
    )
    return keyboard
