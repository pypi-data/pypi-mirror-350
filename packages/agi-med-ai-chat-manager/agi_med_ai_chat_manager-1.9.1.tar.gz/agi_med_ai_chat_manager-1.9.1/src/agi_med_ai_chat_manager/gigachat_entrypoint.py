import contextlib
from base64 import b64encode
from time import sleep
from typing import Literal

from gigachat.models import Embedding, UploadedFile
from gigachat import GigaChat
from gigachat._types import FileTypes

from .base_chat import AbstractEntryPoint


class GigaChatEntryPoint(AbstractEntryPoint):
    def __init__(
        self, client_id: str, client_secret: str, model_id: str = "GigaChat-Pro", warmup: bool = False, temperature=0.0
    ) -> None:
        self._creds: str = b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
        self._model = GigaChat(
            credentials=self._creds,
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            scope="GIGACHAT_API_CORP",
            model=model_id,
            verify_ssl_certs=False,
            profanity_check=False,
        )
        self._DIM: int = 1024
        self._ZEROS: list[float] = [0.0 for _ in range(self._DIM)]
        self._ERROR_MESSAGE: str = ""
        self.temperature = temperature
        if warmup:
            self.warmup()

    def __call__(self) -> GigaChat:
        return self._model

    def get_response(self, sentence: str) -> str:
        with contextlib.suppress(Exception):
            return self._model.chat(sentence).choices[0].message.content
        return self._ERROR_MESSAGE

    def get_response_by_payload(self, payload: list[dict[str, str]]) -> str:
        """payload: [{"role": "system", "content": system}, {"role": "user", "content": replica}]"""
        with contextlib.suppress(Exception):
            return self._model.chat({"messages": payload, "temperature": self.temperature}).choices[0].message.content
        return self._ERROR_MESSAGE

    def get_embedding(self, sentence: str) -> list[float]:
        with contextlib.suppress(Exception):
            return self._model.embeddings([sentence]).data[0].embedding
        return self._ZEROS

    def get_embeddings(self, sentences: list[str], request_limit=50) -> list[list[float]]:
        embeddings: list[list[float]] | None = None
        counter: int = 0
        while embeddings is None and counter < request_limit:
            with contextlib.suppress(Exception):
                items: list[Embedding] = self._model.embeddings(sentences).data
                embeddings = [item.embedding for item in items]
                break
            sleep(0.1)
            counter += 1
        if embeddings is not None:
            return embeddings
        return [self._ZEROS for _ in sentences]

    def upload_file(
        self,
        file: FileTypes,
        purpose: Literal["general", "assistant"] = "general",
    ) -> UploadedFile:
        return self._model.upload_file(file, purpose)
