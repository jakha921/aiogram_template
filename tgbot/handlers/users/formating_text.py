from aiogram import Dispatcher
from aiogram.types import Message


async def show_formatting_text(msg: Message):
    """Formatting text on HTML"""
    await msg.answer(
        "Bold: <b>bold</b>\n"
        "Italic: <i>italic</i>\n"
        "Underline: <u>underline</u>\n"
        "Strikethrough: <s>strikethrough</s>\n"
        "Inline fixed-width code: <code>inline <b>bold</b> fixed-width code</code>\n"
        "Pre-formatted fixed-width code block: <pre>pre-formatted <b>bold</b> fixed-width"
        " code block</pre>\n"
        "Inline URL: <a href='https://google.com'>inline URL</a>\n",
        parse_mode="HTML"
    )


async def show_formatting_text_markdown(msg: Message):
    """Formatting text on Markdown"""
    await msg.answer(
        "Bold: *bold text*\n"
        "Italic: _italic text_\n"
        "Inline code: `inline fixed-width code`\n"
        "Block code:\n"
        "```"
        "pre-formatted fixed-width code block\n"
        "```"
        "Link: [inline URL](https://www.google.com/)\n",
        parse_mode="Markdown"
    )


def register_formatting_text(dp: Dispatcher):
    dp.register_message_handler(
        show_formatting_text,
        text=["/html", "HTML"]
    ),
    dp.register_message_handler(
        show_formatting_text_markdown,
        text=["/markdown", "Markdown"]
    ),
