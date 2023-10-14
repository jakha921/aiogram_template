from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from tgbot.config import CHANNELS
from tgbot.misc.subscription import check_subscriptions


class BigBrother(BaseMiddleware):
    """
    Check user subscription
    """

    async def on_pre_process_update(self, update: types.Update, data: dict):
        user = None

        if update.message:
            user = update.message.from_user
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user

        if user is None:
            return  # No user associated with this update, skip processing

        logger.info(f'User {user.id} sent {update}')

        result = "To use this bot, you need to join the following channels: \n\n"
        final_status = True

        for channel in CHANNELS:
            from bot import bot  # You should import bot appropriately in your application

            status = await check_subscriptions(user_id=user.id, channel=channel)
            final_status *= status

            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                result += f"👉 <a href='{invite_link}'>{channel.title}</a>\n\n"

        if not final_status:
            # Ensure you have a message to reply to before attempting to reply
            if update.message:
                await update.message.reply(result, disable_web_page_preview=True)
                raise CancelHandler()

    async def on_post_process_update(self, update: types.Update, result: dict):
        # Handle post-processing here if needed
        pass
