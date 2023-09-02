# Reply Keyboards

```python
# reply.py

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
```

```python
# handlers/menu.py
from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.reply import menu_keyboard, type_sushi_keyboard


async def show_menu(msg: Message):
    """Bot help handler"""
    await msg.answer("Menu", reply_markup=await menu_keyboard())


async def sushi(msg: Message):
    """Bot help handler"""
    await msg.answer("Good choice!")
    await msg.answer("What kind of sushi do you want?", reply_markup=await type_sushi_keyboard())


async def sushi_type(msg: Message):
    """Bot help handler"""
    await msg.answer("Thanks for your choice!\n"
                     "We will prepare your order as soon as possible",
                     reply_markup=ReplyKeyboardRemove()
                     )


async def fast_food(msg: Message):
    """Bot help handler"""
    await msg.answer("At less 10 minutes\n"
                     "Thanks for your patience",
                     reply_markup=ReplyKeyboardRemove()
                     )


def register_menu(dp: Dispatcher):
    dp.register_message_handler(
        show_menu,
        text=["📋 Menu", "/menu"]
    ),
    dp.register_message_handler(
        sushi,
        text="🍣 Sushi",
    ),
    dp.register_message_handler(
        fast_food,
        text=["🍕 Pizza", "🍔 Burger"]
    ),
    dp.register_message_handler(
        sushi_type,
        text=["🐟 Fish", "🍚 Rice", "🍗 Chicken", "🥑 Vegetarian", "🥩 Meat"]
    ),

```

```python
# bot.py

def register_all_handlers(dp: Dispatcher):
    """Register all handlers"""
    register_admin(dp)
    register_user(dp)
    register_testing(dp)
    register_menu(dp)
    register_echo(dp)
```

