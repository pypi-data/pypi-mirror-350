from tortoise.functions import Count
from x_auth.models import Proxy, Session, Username, App

from pyro_client.loader import WSToken


class SingleMeta(type):
    _instances = {}

    async def __call__(cls, uid: int | str, bot=None):
        if cls not in cls._instances:
            prx = ...
            bt = None
            if isinstance(uid, str):
                if len(ub := uid.split(":")) == 2:
                    uid, bt = ub
                    prx = None
                if uid.isnumeric():
                    uid = int(uid)
            sess = await cls._sess(uid, bt, prx)
            cls._instances[cls] = super().__call__(sess, bot)
        return cls._instances[cls]

    async def _sess(self, uid: int | str, bt: str = None, px: Proxy | None = ..., dc: int = 2) -> Session:
        username, _ = await Username.get_or_create(**{"id" if isinstance(uid, int) else "username": uid})
        if not (
            session := await Session.get_or_none(user=username, api__dc=dc) or await Session.get_or_none(id=username.id)
        ):
            if px is Ellipsis:
                await Proxy.load_list(WSToken)
                # await Proxy.get_replaced(WSToken)
                px = await Proxy.annotate(sc=Count("sessions")).filter(valid=True).order_by("sc", "-updated_at").first()
            if username.phone:
                # noinspection PyUnresolvedReferences
                dc = dc or self.get_dc()
            session = await Session.create(
                id=username.id, api=await App[20373304], user=username, dc_id=dc, proxy=px, is_bot=bt
            )
        await session.fetch_related("proxy", "api")
        return session
