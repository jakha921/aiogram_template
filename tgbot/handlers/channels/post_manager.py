from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery

from tgbot.filters.role import AdminFilter
from tgbot.keyboards.callback_data import create_post_callback
from tgbot.keyboards.inline import channel_new_post_or_cancel
from tgbot.misc.states import NewPost
from tgbot.config import Config, CHANNELS


async def new_post(msg: Message):
    await msg.answer("Send me a post to publish in the channel")
    await NewPost.NewMessage.set()


async def enter_message(msg: Message, state: FSMContext):
    await state.update_data(
        text=msg.html_text,
        mention=msg.from_user.get_mention()
    )
    await msg.answer("Are you sure you want send this post to admins for confirmation?",
                     reply_markup=await channel_new_post_or_cancel())
    print('msg.html_text: ', msg.html_text)
    print('mention: ', msg.from_user.get_mention())
    await NewPost.next()


async def confirm_post(call: CallbackQuery, state: FSMContext):
    # import bot
    from bot import bot

    # get data from state
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()

    # msg send to admins and remove buttons
    await call.message.edit_reply_markup()
    await call.message.answer("Post sent to admins for confirmation")

    # send to admins
    config: Config = call.bot.get('config')
    # for admin in config.tg_bot.admins_id:
    admin = config.tg_bot.admins_id[0]
    print('admin: ', admin)
    await bot.send_message(admin, f"New post from {mention}:\n\n")
    await bot.send_message(admin, text, parse_mode="HTML", reply_markup=await channel_new_post_or_cancel())


async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post canceled")


async def press_button(msg: Message):
    await msg.answer("Press confirm or cancel button")


# admin manage posts
async def approve_post(call: CallbackQuery):
    await call.answer("Post approved", show_alert=True)
    target_channel = CHANNELS[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


async def decline_post(call: CallbackQuery):
    await call.answer("Post declined", show_alert=True)
    await call.message.edit_reply_markup()
    await call.message.answer("Post canceled")


def register_new_post(dp):
    dp.register_message_handler(
        new_post,
        commands=["new_post"],
        state="*"
    ),
    dp.register_message_handler(
        enter_message,
        state=NewPost.NewMessage
    ),
    dp.register_callback_query_handler(
        confirm_post,
        create_post_callback.filter(action="post"),
        state=NewPost.Confirm,
    ),
    dp.register_callback_query_handler(
        cancel_post,
        create_post_callback.filter(action="cancel"),
        state=NewPost.Confirm
    ),
    dp.register_message_handler(
        press_button,
        state=NewPost.Confirm
    ),
    dp.register_callback_query_handler(
        approve_post,
        AdminFilter(),
        create_post_callback.filter(action="post")
    ),
    dp.register_callback_query_handler(
        decline_post,
        AdminFilter(),
        create_post_callback.filter(action="cancel")
    )
