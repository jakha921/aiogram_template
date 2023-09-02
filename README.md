# Filters(Deep link, Command, CommandStart, CommandHelp, ContentType, Text, Regexp)

## Deep link

### Deep link to a specific filter

```text
https://t.me/test921_python_bot?start=aiogram-lessons
```

```python
# user.py
from aiogram.dispatcher.filters import CommandStart


# deep_linking
async def user_start(msg: Message, texts: Map):
    """User start command handler"""
    logger.info(f'User {msg.from_user.id} started the bot')

    # use deep_linking to get deep link data
    deep_link = msg.get_args()

    text = texts.user.hi.format(mention=msg.from_user.get_mention())
    if deep_link:
        text += f'\n\nYou came with deep link: {deep_link}'
    await msg.reply(text)


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start,
        CommandStart(),
        # commands=["/start"],
        # commands=["start"],
        state="*",
    )
```

```python
# echo.py

from aiogram import types

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandHelp, Text, Regexp
from aiogram.types import Message
from loguru import logger


async def bot_echo(msg: Message):
    """Bot echo handler"""
    logger.info(f'User {msg.from_user.id} sent message: {msg.text}')

    text = f"Echo: \n{msg.text}"

    print(f'message: {msg}')

    await msg.answer(text)
    # await msg.reply(text)


async def bot_help(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} requested help')
    text = "Help message"
    await msg.answer(text)


async def get_photo(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} send photo')
    await msg.answer("I can`t work with photos yet:(")


async def get_file(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} send file')
    await msg.answer("I can`t work with such files yet:(")


async def greet_user(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} greeted')
    await msg.answer(f"Assalomu alaykum, {msg.from_user.first_name}!")


async def spam(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} spam')
    await msg.answer(f"Spam")

async def get_email(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} send email')
    await msg.answer(f"Now I can`t do smth with emails sorry!")


def register_echo(dp: Dispatcher):
    dp.register_message_handler(
        bot_help,
        CommandHelp(),
        state="*"
    ),
    dp.register_message_handler(
        get_photo,
        content_types=(types.ContentType.PHOTO, types.ContentType.DOCUMENT),
        # content_types=['photo', 'document'],
    ),
    dp.register_message_handler(
        get_file,
        content_types=(types.ContentType.DOCUMENT, types.ContentType.VIDEO, types.Voice),
        # content_types=['document', 'video', 'voice'],
    ),
    dp.register_message_handler(
        greet_user,
        Text(equals="Assalomu alaykum"),
        Text(contains="salom")
    ),
    dp.register_message_handler(
        spam,
        Text(endswith="spam"),
        Text(contains="spam"),
        Text(startswith="spam"),
    ),
    dp.register_message_handler(
        get_email,
        Regexp(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")
    ),
    dp.register_message_handler(
        bot_echo,
        state="*",  # for all states
    )
```

```python
# bot.py

def register_all_handlers(dp: Dispatcher):
    """Register all handlers"""
    register_admin(dp)
    register_user(dp)
    register_echo(dp)
```