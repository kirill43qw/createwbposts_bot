import re

from aiogram import F, Router
from aiogram.filters import BaseFilter
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text
from aiogram.utils.media_group import MediaGroupBuilder
from emoji import emojize

from pars_api import parse

"""
прописать состояние
прописать фильтр на хэндлер
оптимизировать код, потому что на хуйню похоже
"""


router = Router()


access_users: list[int] = [338735083]


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# @router.message(lambda msg: msg.text in ("/start", "/help"))
@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    text = Text(
        "Hello, ", Bold(message.from_user.full_name), emojize(" :rainbow_flag:")
    )
    await message.answer(**text.as_kwargs())


@router.message(IsAdmin(access_users), F.text)
async def create_media_group(message: Message):
    articles = re.split(r"[.,\s;]+", message.text.strip())
    all_item = [parse(i) for i in articles]  # можно тут проверку parse(i)

    # это временное решение
    all_item = [i for i in all_item if i is not None]

    # попробовать заменить на генератор, просто поменять ()
    group_art = [all_item[i : i + 9] for i in range(0, len(all_item), 9)]
    for post in group_art:
        if len(post) == 9:
            text = emojize(
                f"""
:keycap_1: <b><a href='{post[0].item_url}'>{post[0].id}</a> - </b><i>{post[0].total}</i> ₽
:keycap_2: <b><a href='{post[1].item_url}'>{post[1].id}</a> - </b><i>{post[1].total}</i> ₽
:keycap_3: <b><a href='{post[2].item_url}'>{post[2].id}</a> - </b><i>{post[2].total}</i> ₽
:keycap_4: <b><a href='{post[3].item_url}'>{post[3].id}</a> - </b><i>{post[3].total}</i> ₽
:keycap_5: <b><a href='{post[4].item_url}'>{post[4].id}</a> - </b><i>{post[4].total}</i> ₽
:keycap_6: <b><a href='{post[5].item_url}'>{post[5].id}</a> - </b><i>{post[5].total}</i> ₽
:keycap_7: <b><a href='{post[6].item_url}'>{post[6].id}</a> - </b><i>{post[6].total}</i> ₽
:keycap_8: <b><a href='{post[7].item_url}'>{post[7].id}</a> - </b><i>{post[7].total}</i> ₽
:keycap_9: <b><a href='{post[8].item_url}'>{post[8].id}</a> - </b><i>{post[8].total}</i> ₽
\n\n<ins><i>кликай на артикул и забирай товар</i></ins>
    """
            )
            album_builder = MediaGroupBuilder(caption=text)
            for url in post:
                album_builder.add_photo(media=url.image_url)

            await message.answer_media_group(
                media=album_builder.build(), allow_sending_without_reply=True
            )
        else:
            n = 9 - (len(post) % 9)
            free_arts = " ".join([str(i.id) for i in post])
            await message.answer(text=f"не хватает {n}, вот сдача:\n{free_arts}")