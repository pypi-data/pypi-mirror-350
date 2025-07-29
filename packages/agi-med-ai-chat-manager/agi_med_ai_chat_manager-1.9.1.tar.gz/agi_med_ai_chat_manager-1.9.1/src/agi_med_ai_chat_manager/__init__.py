__version__ = "1.9.1"

from .base_chat import AbstractEntryPoint  # noqa: F401
from .open_router_entrypoint import OpenRouterEntryPoint
from .airi_entrypoint import AiriChatEntryPoint
from .yandex_gpt_entrypoint import YandexGPTEntryPoint
from .gigachat_censored_entrypoint import GigaChatCensoredEntryPoint
from .gigachat_entrypoint import GigaChatEntryPoint
from .gigachat_plus_entrypoint import GigaPlusEntryPoint
from .gigachat_max_entrypoint import GigaMaxEntryPoint, GigaMax2EntryPoint

ENTRYPOINTS: dict[str, str] = {
    "airi": AiriChatEntryPoint,
    "giga": GigaChatEntryPoint,
    "giga-max": GigaMaxEntryPoint,
    "giga-max-2": GigaMax2EntryPoint,
    "giga-plus": GigaPlusEntryPoint,
    "giga-cencored": GigaChatCensoredEntryPoint,
    "open-router": OpenRouterEntryPoint,
    "yandex": YandexGPTEntryPoint,
}


def create_entrypoint(entrypoint_name: str, entrypoint_args: dict[str, any]):
    entrypoint_class = ENTRYPOINTS.get(entrypoint_name)
    if entrypoint_class is None:
        err = f"Not found entrypoint for entrypoint_name={entrypoint_name}"
        raise ValueError(err)
    return entrypoint_class(**entrypoint_args)
