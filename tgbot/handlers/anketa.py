import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from loguru import logger

from tgbot.misc.states import Test


async def start_testing(msg: Message):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} started testing')
    await msg.answer(f"Testing started.\n"
                     "Please, answer the questions.\n"
                     "1. What is your name?"
                     )

    await Test.Q1.set()
    # await Test.first()


async def first_question(msg: Message, state: FSMContext):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} answered the first question')

    # Check answer length (not less than 3 symbols) and if it's ok ask next question
    if len(msg.text) < 3:
        await msg.answer("Your name is too short.\n"
                         "Please, try again."
                         )
        return

    # Check for numbers in the answer
    if any(map(str.isdigit, msg.text)):
        await msg.answer("Your name is not valid.\n"
                         "Name can't contain numbers.\n"
                         "Please, try again."
                         )
        return

    # Save answer
    await state.update_data(name=msg.text)
    # await state.update_data(
    #     {
    #         "name": msg.text
    #     }
    # )

    await msg.answer(f"How old are you, {msg.text}?")

    # Go to the next question
    await Test.Q2.set()
    # await Test.next()


async def second_question(msg: Message, state: FSMContext):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} answered the second question')

    # check answer
    if not msg.text.isdigit():
        await msg.answer("Your age is not valid.\n"
                         "Age can contain only numbers.\n"
                         "Please, try again."
                         )
        return

    # Save answer
    await state.update_data(age=msg.text)

    # Get name
    data = await state.get_data()
    name = data.get("name")

    await msg.answer(f"Ok, {name}.\n"
                     f"Now You need to send me your email."
                     )

    # Go to the next question
    await Test.Q3.set()


async def third_question(msg: Message, state: FSMContext):
    """Bot help handler"""
    logger.info(f'User {msg.from_user.id} answered the third question')

    # Get previous answer
    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")

    # Check answer
    if not re.match(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", msg.text):
        await msg.answer("Your email is not valid.\n"
                         "Please, try again."
                         )
        return

    # Send message with all answers
    await msg.answer(f"Thank you for your answers.\n")
    await msg.answer(f"{name}, We will send you a letter to {msg.text}.\n"
                     f"We will not tell anyone that you are {age} years old."
                     )
    await msg.answer("That's all. Thank you for testing.")

    # Finish conversation
    await state.finish()  # finish the current state
    # await state.reset_state() # finish all states and reset data
    # await state.reset_state(with_data=False) # finish all states but don't reset data


def register_testing(dp: Dispatcher):
    dp.register_message_handler(
        start_testing,
        Command("test"),
        state=None
    )
    dp.register_message_handler(
        first_question,
        state=Test.Q1
    )
    dp.register_message_handler(
        second_question,
        state=Test.Q2
    )
    dp.register_message_handler(
        third_question,
        state=Test.Q3
    )
