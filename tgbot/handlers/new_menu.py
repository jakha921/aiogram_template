from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_data import sub_menu_callback, sushi_type_callback
from tgbot.keyboards.inline import new_menu_keyboard, sub_menu_keyboard, discounts_keyboard, type_sushi_keyboard


async def new_menu(msg: Message):
    """Bot help handler"""
    await msg.answer("Menu", reply_markup=await new_menu_keyboard())


async def discount(call: CallbackQuery):
    """Bot help handler"""
    # await call.message.edit_reply_markup()
    await call.message.delete()
    await call.message.answer("Discount", reply_markup=await discounts_keyboard())
    await call.answer(cache_time=60)


async def sub_menu(call: CallbackQuery):
    """Bot help handler"""
    # print(f'call: {call}')
    # print(f'call.data: {call.data}')
    await call.message.delete()
    await call.message.answer("Sub menu", reply_markup=await sub_menu_keyboard())
    await call.answer(cache_time=60)


async def sushi(call: CallbackQuery, callback_data: dict):
    """Bot help handler"""
    # print(f'call: {call}')
    # print(f'call.data: {call.data}')
    print(f'callback_data: {callback_data}')
    await call.message.delete()
    await call.message.answer("Good choice!")
    await call.message.answer("What kind of sushi do you want?", reply_markup=await type_sushi_keyboard())
    await call.answer(cache_time=60)


async def other_food(call: CallbackQuery, callback_data: dict):
    """Bot help handler"""
    # print(f'call: {call}')
    # print(f'call.data: {call.data}')
    print(f'callback_data: {callback_data}')
    await call.answer(f"{callback_data.get('product_name').capitalize()} is started to prepare\n"
                      "It will take about 10 minutes\n"
                      "Thanks for your patience",
                      show_alert=False)  # show_alert=True - show alert on user's device even if bot is in background


async def sushi_type(call: CallbackQuery, callback_data: dict):
    """Bot help handler"""
    # print(f'call: {call}')
    # print(f'call.data: {call.data}')
    print(f'callback_data: {callback_data}')
    await call.message.delete()
    await call.message.answer("Thanks for your choice!\n"
                              "We will prepare your order as soon as possible"
                              )
    await call.answer(cache_time=60)


async def cancel(call: CallbackQuery):
    """Bot help handler"""
    await call.message.edit_reply_markup(reply_markup=await new_menu_keyboard())
    await call.answer()


async def send_logo(call: CallbackQuery):
    """Bot help handler"""
    await call.message.answer_photo(
        photo="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
    )
    await call.answer()


def register_new_menu(dp: Dispatcher):
    dp.register_message_handler(
        new_menu,
        text=["📋 New menu", "/new_menu"]
    ),
    dp.register_callback_query_handler(
        discount,
        text="discounts"
    )
    dp.register_callback_query_handler(
        sub_menu,
        text="sub_menu"
    )
    dp.register_callback_query_handler(
        sushi,
        sub_menu_callback.filter(product_name="sushi")
    )
    dp.register_callback_query_handler(
        other_food,
        sub_menu_callback.filter(
            product_name=[
                "pizza", "burger", "french_fries", "salad", "popcorn",
                "ice_cream", "donut", "chocolate", "lollipop", "cookies"
            ]
        )
    )
    dp.register_callback_query_handler(
        sushi_type,
        sushi_type_callback.filter(from_sushi=["fish", "rice", "chicken", "vegetarian", "meat"])
    ),
    dp.register_callback_query_handler(
        cancel,
        text="cancel"
    )
    dp.register_callback_query_handler(
        send_logo,
        text="get_logo"
    )
