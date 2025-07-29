from .gigachat_entrypoint import GigaChatEntryPoint


class GigaPlusEntryPoint(GigaChatEntryPoint):
    def __init__(
        self, client_id: str, client_secret: str, model_id: str = "GigaChat-Plus", warmup: bool = False
    ) -> None:
        super().__init__(client_id=client_id, client_secret=client_secret, model_id=model_id, warmup=warmup)
