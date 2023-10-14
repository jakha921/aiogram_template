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
