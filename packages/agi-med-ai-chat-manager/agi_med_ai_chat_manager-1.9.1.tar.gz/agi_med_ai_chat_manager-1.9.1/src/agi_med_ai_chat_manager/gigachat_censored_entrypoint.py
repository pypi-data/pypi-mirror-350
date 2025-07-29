from gigachat import GigaChat
from .gigachat_entrypoint import GigaChatEntryPoint


class GigaChatCensoredEntryPoint(GigaChatEntryPoint):
    def __init__(
        self, client_id: str, client_secret: str, model_id: str = "GigaChat-Pro", warmup: bool = False
    ) -> None:
        super().__init__(client_id, client_secret, warmup=False)
        self._model = GigaChat(
            credentials=self._creds,
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            scope="GIGACHAT_API_CORP",
            model=model_id,
            verify_ssl_certs=False,
            profanity_check=True,
        )
        if warmup:
            self.warmup()
