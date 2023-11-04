from aiogram import types
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.models import TGUser


class DbMiddleware(LifetimeControllerMiddleware):
    """Middleware for adding user into DB if he/she not exists"""

    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        # If user not exists in DB, add him/her
        db_session = obj.bot.get('db')

        data['db_session'] = db_session  # add user object to data
