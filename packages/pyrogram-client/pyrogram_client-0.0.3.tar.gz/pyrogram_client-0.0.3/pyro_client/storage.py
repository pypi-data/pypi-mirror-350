import time
from typing import Any, Literal

from pyrogram import raw, utils
from pyrogram.storage import Storage
from x_auth.models import Username, Version, Session, Peer, UpdateState


def get_input_peer(peer_id: int, access_hash: int, peer_type: Literal["user", "bot", "group", "channel", "supergroup"]):
    if peer_type in ["user", "bot"]:
        return raw.types.InputPeerUser(user_id=peer_id, access_hash=access_hash)

    if peer_type == "group":
        return raw.types.InputPeerChat(chat_id=-peer_id)

    if peer_type in ["channel", "supergroup"]:
        return raw.types.InputPeerChannel(channel_id=utils.get_channel_id(peer_id), access_hash=access_hash)

    raise ValueError(f"Invalid peer type: {peer_type}")


class PgStorage(Storage):
    VERSION = 1
    USERNAME_TTL = 8 * 60 * 60
    session: Session
    # me_id: int

    async def open(self):
        # self.me_id = int((uid_dc := self.name.split("_")).pop(0))
        self.session = await Session[self.name]

    async def save(self):
        await self.date(int(time.time()))

    async def close(self): ...

    async def delete(self):
        await Session.filter(id=self.name).delete()

    async def update_peers(self, peers: list[tuple[int, int, str, str]]):
        for peer in peers:
            uid, ac_hsh, typ, phn = peer
            un, _ = await Username.get_or_create(phn and {"phone": phn}, id=uid)
            await Peer.update_or_create(
                {"username": un, "type": typ, "phone_number": phn}, session_id=self.name, id=ac_hsh
            )

    async def update_usernames(self, usernames: list[tuple[int, list[str]]]):
        for telegram_id, user_list in usernames:
            for username in user_list:
                await Username.update_or_create({"username": username}, id=telegram_id)

    async def get_peer_by_id(self, peer_id_or_username: int | str):
        attr = "id" if isinstance(peer_id_or_username, int) else "username"
        if not (peer := await Peer.get_or_none(session_id=self.name, **{"username__" + attr: peer_id_or_username})):
            raise KeyError(f"User not found: {peer_id_or_username}")
        if peer.last_update_on:
            if abs(time.time() - peer.last_update_on.timestamp()) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {peer_id_or_username}")
        return get_input_peer(peer.username_id, peer.id, peer.type)

    async def get_peer_by_username(self, username: str):
        return await self.get_peer_by_id(username)

    async def update_state(self, value: tuple[int, int, int, int, int] = object):
        if value is None:
            return await UpdateState.filter(session_id=self.name)
        elif isinstance(value, int):
            await UpdateState.filter(session_id=self.name, id=value).delete()
        else:
            sid, pts, qts, date, seq = value
            await UpdateState.get_or_create(
                {"pts": pts, "qts": qts, "date": date, "seq": seq}, session_id=self.name, id=sid
            )

    async def get_peer_by_phone_number(self, phone_number: str):
        if not (
            peer := await Peer.filter(session_id=self.name, phone_number=phone_number).values_list(
                "id", "access_hash", "type"
            )
        ):
            raise KeyError(f"Phone number not found: {phone_number}")
        return get_input_peer(*peer)

    async def _get(self, attr: str):
        return await Session.get(id=self.name).values_list(attr, flat=True)

    async def _set(self, attr: str, value):
        # if "__" in attr:
        #     table, attr = attr.split("__")
        #     rel = await self.session.__getattribute__(table)
        #     rel.__setattr__(attr, value)
        #     await rel.save()
        # else:
        await Session.update_or_create({attr: value}, id=self.name)

    async def _accessor(self, attr: str, value: Any = object):
        if value is object:
            return await self._get(attr)
        else:
            await self._set(attr, value)

    async def dc_id(self, value: int = object):
        return await self._accessor("dc_id", value)

    async def api_id(self, value: int = object):
        return await self._accessor("api_id", value)

    async def test_mode(self, value: bool = object):
        return await self._accessor("test_mode", value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor("auth_key", value)

    async def date(self, value: int = object):
        return await self._accessor("date", value)

    async def user_id(self, value: int = object):
        return await self._accessor("user_id", value)

    async def is_bot(self, value: bool = object):
        return await self._accessor("is_bot", value)

    @staticmethod
    async def version(value: int = object):
        if value is object:
            ver = await Version.first()
            return ver.number
        else:
            await Version.update_or_create(id=value)
