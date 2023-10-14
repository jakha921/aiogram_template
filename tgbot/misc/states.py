from aiogram.dispatcher.filters.state import State, StatesGroup


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


class NewPost(StatesGroup):
    NewMessage = State()
    Confirm = State()
