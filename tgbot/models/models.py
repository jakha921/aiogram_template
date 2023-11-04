from sqlalchemy import (Column, String, BigInteger,
                        insert, update, func, select)
from sqlalchemy.orm import sessionmaker

from tgbot.services.db_base import Base

from tgbot.config import load_config

# load config from bot.ini file
config = load_config("bot.ini")


class TGUser(Base):
    """Telegram user model"""
    __tablename__ = "telegram_users"
    telegram_id = Column(BigInteger, unique=True, primary_key=True)
    firstname = Column(String(length=100))
    lastname = Column(String(length=100))
    username = Column(String(length=100), nullable=True)
    phone = Column(String(length=15), nullable=True)
    lang_code = Column(String(length=10), default='en')

    @classmethod
    async def get_user(cls, db_session: sessionmaker, telegram_id: int) -> 'TGUser':
        """Get user by telegram_id"""
        async with db_session() as session:
            sql = select(TGUser).where(TGUser.telegram_id == telegram_id)
            request = await session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def add_user(cls,
                       db_session: sessionmaker,
                       telegram_id: int,
                       firstname: str,
                       lastname: str,
                       username: str = None,
                       phone: str = None,
                       lang_code: str = None,
                       ) -> 'TGUser':
        """Add new user into DB"""
        async with db_session() as session:
            values = {
                'telegram_id': telegram_id,
                'firstname': firstname,
                'lastname': lastname,
                'username': username,
                'phone': phone,
                'lang_code': lang_code,
            }
            sql = insert(TGUser).values(**values)

            if session.bind.dialect.name == 'sqlite':
                # SQLite specific: Execute the insert and retrieve the last inserted rowid
                result = await session.execute(sql)
                last_row_id = result.lastrowid
            else:
                # For other databases (e.g., PostgreSQL), use RETURNING to get the inserted record
                sql = sql.returning('*')
                result = await session.execute(sql)
                inserted_user = result.fetchone()
                last_row_id = inserted_user.id  # Assuming 'id' is the primary key

            await session.commit()

            # After the insert, retrieve the newly inserted user
            inserted_user = await cls.get_user(db_session, last_row_id)
            return inserted_user

    @classmethod
    async def update_user(cls, db_session: sessionmaker, telegram_id: int, updated_fields: dict) -> 'TGUser':
        """Update user fields"""
        async with db_session() as session:
            # {phone: '+380123456789'}
            sql = update(cls).where(cls.telegram_id == telegram_id).values(**updated_fields)
            result = await session.execute(sql)
            await session.commit()
            return result

    @classmethod
    async def get_all_users(cls, db_session: sessionmaker) -> list:
        """Returns all users from DB"""
        async with db_session() as session:
            # select all coçlumns from table
            sql = select(*cls.__table__.columns).order_by(cls.telegram_id)
            result = await session.execute(sql)
            users: list = result.fetchall()
        return users

    @classmethod
    async def users_count(cls, db_session: sessionmaker) -> int:
        """Counts all users in the database"""
        async with db_session() as session:
            sql = select(func.count(cls.telegram_id))
            request = await session.execute(sql)
            count = request.scalar()
        return count

    @classmethod
    async def get_all_users_by_filter(cls, db_session: sessionmaker):
        """Returns all users from DB"""
        async with db_session() as session:
            # select all coçlumns from table
            sql = select(*TGUser.__table__.columns).where(TGUser.lang_code == 'ru')
            result = await session.execute(sql)
            users: list = result.fetchall()
        return users


    def __repr__(self):
        return f'User (ID: {self.telegram_id} - {self.firstname} {self.lastname})'
