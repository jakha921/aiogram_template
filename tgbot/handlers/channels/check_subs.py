from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.config import CHANNELS
from tgbot.filters.private import PrivateChatFilter
from tgbot.keyboards.inline import check_button
from tgbot.misc.subscription import check_subscriptions


async def show_channels(msg: Message):
    from bot import bot

    channel_format = str()

    # load from bot config
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()

        channel_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"

    await msg.answer(f"To use this bot, you need to join the following channels: \n\n"
                     f"{channel_format}",
                     disable_web_page_preview=True,
                     reply_markup=await check_button())


async def checker(call: CallbackQuery):
    from bot import bot
    await call.answer()
    result = str()

    for channel in CHANNELS:
        status = await check_subscriptions(user_id=call.from_user.id,
                                           channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"✅ You are subscribed to the channel: {channel.title}\n"
        else:
            invite_link = await channel.export_invite_link()
            result += f"❌ You are not subscribed to the channel: \n" \
                      f"👉 <a href='{invite_link}'>{channel.title}</a>\n\n"

    await call.message.answer(result, disable_web_page_preview=True)


def register_subscription(dp: Dispatcher):
    dp.register_message_handler(
        show_channels,
        PrivateChatFilter(),
        commands=["start"],
        state="*"
    )
    dp.register_callback_query_handler(
        checker,
        text="check_subs"
    )
