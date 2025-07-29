import asyncio
from collections import OrderedDict
from io import BytesIO
from typing import Literal

from pyrogram import Client
from pyrogram.filters import chat, contact, AndFilter
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from pyro_client.client.single import SingleMeta
from pyro_client.storage import PgStorage

AuthTopic = Literal["phone", "code", "pass"]


def sync_call_async(async_func, *args):
    loop = asyncio.get_event_loop()  # Получаем текущий запущенный цикл
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(async_func(*args), loop)
        return future.result(5)  # Блокируемся, пока корутина не выполнится


class BaseClient(Client, metaclass=SingleMeta):
    storage: PgStorage

    def __init__(self, name: str, api_id, api_hash, *args, **kwargs):
        super().__init__(name, api_id=api_id, api_hash=api_hash, *args, storage_engine=PgStorage(name), **kwargs)

    async def send(
        self,
        txt: str,
        uid: int | str = "me",
        btns: list[InlineKeyboardButton | KeyboardButton] = None,
        photo: bytes = None,
        video: bytes = None,
    ) -> Message:
        ikm = (
            (
                InlineKeyboardMarkup([btns])
                if isinstance(btns[0], InlineKeyboardButton)
                else ReplyKeyboardMarkup([btns], one_time_keyboard=True)
            )
            if btns
            else None
        )
        if photo:
            return await self.send_photo(uid, BytesIO(photo), txt, reply_markup=ikm)
        elif video:
            return await self.send_video(uid, BytesIO(video), txt, reply_markup=ikm)
        else:
            return await self.send_message(uid, txt, reply_markup=ikm)

    async def wait_from(self, uid: int, topic: str, past: int = 0, timeout: int = 10) -> str | None:
        fltr = chat(uid)
        if topic == "phone":
            fltr &= contact
        handler = MessageHandler(self.got_msg, fltr)
        # handler, g = self.add_handler(handler, 1)
        g = 0
        if g not in self.dispatcher.groups:
            self.dispatcher.groups[g] = []
            self.dispatcher.groups = OrderedDict(sorted(self.dispatcher.groups.items()))
        self.dispatcher.groups[g].append(handler)
        #
        while past < timeout:
            if txt := self.storage.session.state.get(uid, {}).pop(topic, None):
                # self.remove_handler(handler)
                self.dispatcher.groups[g].remove(handler)
                #
                return txt
            await asyncio.sleep(1)
            past += 1
        return self.remove_handler(handler, g)

    async def got_msg(self, _, msg: Message):
        if tpc := self.storage.session.state.get(msg.from_user.id, {}).pop("waiting_for", None):
            self.storage.session.state[msg.from_user.id][tpc] = msg.contact.phone_number if tpc == "phone" else msg.text

    def rm_handler(self, uid: int):
        for gi, grp in self.dispatcher.groups.items():
            [self.remove_handler(h, gi) for h in grp if isinstance(h.filters, AndFilter) and uid in h.filters.base]
