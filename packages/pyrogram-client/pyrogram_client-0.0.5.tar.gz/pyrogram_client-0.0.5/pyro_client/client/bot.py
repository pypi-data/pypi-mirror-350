from x_auth.models import Session

from pyro_client.client.base import BaseClient, AuthTopic


class BotClient(BaseClient):
    def __init__(self, sess: Session, _=None):
        super().__init__(sess.id, sess.api.id, sess.api.hsh, bot_token=f"{sess.id}:{sess.is_bot}")

    async def wait_auth_from(self, uid: int, topic: AuthTopic, past: int = 0, timeout: int = 60) -> str:
        return await super().wait_from(uid, topic, past, timeout)
