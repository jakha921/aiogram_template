from typing import Union

from aiogram import Bot
from loguru import logger


# Define an asynchronous function called check_subscriptions
async def check_subscriptions(user_id: int, channel: Union[int, str]):
    """Check subscriptions"""

    # Log a message to indicate that we are checking subscriptions
    logger.info("Checking subscriptions...")

    # Get the current instance of the Bot class
    bot = Bot.get_current()

    # Use the bot instance to get information about a chat member asynchronously
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)

    # Return a boolean indicating whether the user is a chat member
    return member.is_chat_member()
