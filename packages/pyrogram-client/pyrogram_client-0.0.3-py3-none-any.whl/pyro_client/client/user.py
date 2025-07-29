import logging
from json import load
from os.path import dirname

from pydantic import BaseModel, Field
from pyrogram import enums
from pyrogram.enums import ClientPlatform
from pyrogram.errors import BadRequest, SessionPasswordNeeded, AuthKeyUnregistered, Unauthorized
from pyrogram.session import Auth, Session as PyroSession
from pyrogram.types import Message, User, SentCode, InlineKeyboardButton, KeyboardButton
from x_auth.models import Session, Username, Proxy

from pyro_client.client.base import BaseClient, AuthTopic
from pyro_client.client.bot import BotClient
from pyro_client.loader import WSToken

vers: dict[ClientPlatform, str] = {
    ClientPlatform.IOS: "18.5",
    ClientPlatform.ANDROID: "16",
}


class Prx(BaseModel):
    scheme: str = "socks5"
    hostname: str = Field(validation_alias="host")
    port: int
    username: str
    password: str


class UserClient(BaseClient):
    bot: BotClient

    def __init__(self, sess: Session, bot):
        self.bot = bot
        super().__init__(
            sess.id,
            sess.api.id,
            sess.api.hsh,
            device_model="iPhone 16e",
            app_version=sess.api.ver,
            system_version=vers.get(sess.api.platform),
            client_platform=sess.api.platform,
            proxy=sess.proxy and sess.proxy.dict(),
        )

    async def start(self, use_qr: bool = False, except_ids: list[int] = None):
        if not self.bot.is_connected:
            await self.bot.start()
        # dcs = await self.bot.invoke(GetConfig())
        try:
            await super().start(use_qr=use_qr, except_ids=except_ids or [])
            await self.send("im ok")
        except AuthKeyUnregistered as e:
            await self.storage.session.delete()
            raise e
        except (AuthKeyUnregistered, Unauthorized) as e:
            raise e

    async def ask_for(
        self, topic: AuthTopic, question: str, btns: list[InlineKeyboardButton, KeyboardButton] = None
    ) -> str:
        if topic == "phone":
            btns = btns or [] + [KeyboardButton("Phone", True)]
        await self.receive(question, btns)
        uid = int(self.storage.name)
        self.bot.storage.session.state[uid] = {"waiting_for": topic}
        return await self.bot.wait_auth_from(uid, topic)

    async def receive(
        self,
        txt: str,
        btns: list[InlineKeyboardButton | KeyboardButton] = None,
        photo: bytes = None,
        video: bytes = None,
    ) -> Message:
        return await self.bot.send(txt, int(self.storage.name), btns, photo, video)

    def get_dc(self):
        if not self.phone_number:
            return 2
        with open(f"{dirname(__file__)}/dc.json", "r") as file:
            jsn = load(file)
        for k, v in jsn.items():
            if self.phone_number.startswith(k):
                return v
        return 2

    async def authorize(self, sent_code: SentCode = None) -> User:
        sent_code_desc = {
            enums.SentCodeType.APP: "Telegram app",
            enums.SentCodeType.SMS: "SMS",
            enums.SentCodeType.CALL: "phone call",
            enums.SentCodeType.FLASH_CALL: "phone flash call",
            enums.SentCodeType.FRAGMENT_SMS: "Fragment SMS",
            enums.SentCodeType.EMAIL_CODE: "email code",
        }
        # Step 1: Phone
        if not self.phone_number:
            user = await Username[self.storage.session.id]
            if not (user.phone and (phone := str(user.phone))):
                phone = await self.ask_for("phone", "Phone plz")
                user.phone = phone
                await user.save()
            self.phone_number = phone
            if (dc := self.get_dc()) != 2:
                await self.session_update(dc)
            if not self.phone_number:
                await self.authorize()
            try:
                # user.phone = int(self.phone_number.strip("+ ").replace(" ", ""))
                sent_code = await self.send_code(self.phone_number, True, False, True, False, True)
            except BadRequest as e:
                await self.send(e.MESSAGE)
                self.phone_number = None
                return await self.authorize(sent_code)
        # Step 2: Code
        if not self.phone_code:
            if code := await self.ask_for("code", f"Code from {sent_code_desc[sent_code.type]}"):
                self.phone_code = code.replace("_", "")
                try:
                    signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
                except BadRequest as e:
                    await self.receive(e.MESSAGE)
                    self.phone_code = None
                    return await self.authorize(sent_code)
                except SessionPasswordNeeded:
                    # Step 2.1?: Cloud password
                    while True:
                        self.password = await self.ask_for(
                            "pass", f"Enter pass: (hint: {await self.get_password_hint()})"
                        )
                        try:
                            signed_in = await self.check_password(self.password)
                            break
                        except BadRequest as e:
                            await self.send(e.MESSAGE)
                            self.password = None
            else:
                raise Exception("User does not sent code")
            if isinstance(signed_in, User):
                await self.send("✅", self.bot.me.id)
                await self.storage.save()
                return signed_in

            if not signed_in:
                await self.receive("No registered such phone number")

    async def stop(self, block: bool = True):
        await super().stop(block)
        await self.bot.stop(block)

    async def session_update(self, dc: int):
        await self.session.stop()

        await self.storage.dc_id(dc)
        await self.storage.auth_key(
            await Auth(self, await self.storage.dc_id(), await self.storage.test_mode()).create()
        )
        self.session = PyroSession(
            self, await self.storage.dc_id(), await self.storage.auth_key(), await self.storage.test_mode()
        )
        if not self.proxy and not self.storage.session.proxy:
            await Proxy.load_list(WSToken)
            prx: Proxy = await Proxy.filter(valid=True).order_by("-updated_at").first()
            self.storage.session.proxy = prx
            await self.storage.session.save()
            self.proxy = prx.dict()
        await self.session.start()


async def main():
    from x_auth import models
    from x_model import init_db

    from pyro_client.loader import WSToken, PG_DSN

    _ = await init_db(PG_DSN, models, True)

    logging.basicConfig(level=logging.INFO)

    await models.Proxy.load_list(WSToken)
    # session = await models.Session.filter(is_bot__isnull=True).order_by("-date").prefetch_related("proxy").first()
    bc: BotClient = await BotClient("xyncnetbot")
    uc: UserClient = await UserClient(5547330178, bc)
    # try:
    await uc.start()
    # except Exception as e:
    #     print(e.MESSAGE)
    #     await uc.send(e.MESSAGE)
    #     await uc.storage.session.delete()
    # finally:
    await uc.stop()


if __name__ == "__main__":
    from asyncio import run

    run(main())
