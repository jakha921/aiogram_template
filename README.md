# Inline keyboards

## Simple inline keyboard

```python
# reply.py

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
            ],
            [
                KeyboardButton(text="📋 New menu"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard
```

```python
# new_menu.py

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_data import sub_menu_callback, sushi_type_callback
from tgbot.keyboards.inline import new_menu_keyboard, sub_menu_keyboard, discounts_keyboard, type_sushi_keyboard


async def new_menu(msg: Message):
    """Bot help handler"""
    await msg.answer("Menu", reply_markup=await new_menu_keyboard())


def register_new_menu(dp: Dispatcher):
    dp.register_message_handler(
        new_menu,
        text=["📋 New menu", "/new_menu"]
    ),
```

```python
# inline.py


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

```

```python
# new_menu.py

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
```

```python
# inline.py


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


# callback_data.py
from aiogram.utils.callback_data import CallbackData

sub_menu_callback = CallbackData("sub_menu", "product_name")
sushi_type_callback = CallbackData("type_sushi", "from_sushi")


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

```

```python
# new_menu.py


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

```

```python
# bot.py

def register_all_handlers(dp: Dispatcher):
    """Register all handlers"""
    register_admin(dp)
    register_user(dp)
    register_testing(dp)
    register_menu(dp)
    register_new_menu(dp)
    register_echo(dp)
```