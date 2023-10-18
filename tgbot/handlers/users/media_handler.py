from pathlib import Path

from aiogram import Dispatcher
from aiogram import types

download_path = Path().joinpath("downloads", "media")  # template/downloads/media
download_path.mkdir(parents=True, exist_ok=True)  # create folder if not exists


async def get_photo(msg: types.Message):
    await msg.photo[-1].download(destination_dir=download_path)
    await msg.answer("I got your photo!")


async def get_file(msg: types.Message):
    await msg.document.download(destination_dir=download_path)
    await msg.answer("I got your file!")


async def get_audio(msg: types.Message):
    await msg.audio.download(destination_dir=download_path)
    await msg.answer("I got your audio!")


async def get_video(msg: types.Message):
    await msg.video.download(destination_dir=download_path)
    await msg.answer("I got your video!")


async def get_any(msg: types.Message):
    await msg.answer("I got your, " + msg.content_type + "!")


def register_media(dp: Dispatcher):
    dp.register_message_handler(
        get_photo,
        # content_types=types.ContentType.PHOTO
        content_types='photo'
    )
    dp.register_message_handler(
        get_file,
        content_types=types.ContentType.DOCUMENT,
        # content_types='document'
    )
    dp.register_message_handler(
        get_audio,
        content_types=types.ContentType.AUDIO,
        # content_types='audio'
    )
    dp.register_message_handler(
        get_video,
        content_types=types.ContentType.VIDEO,
        # content_types='video'
    )
    dp.register_message_handler(
        get_any,
        content_types=types.ContentType.ANY,
        # content_types='any'
    )
