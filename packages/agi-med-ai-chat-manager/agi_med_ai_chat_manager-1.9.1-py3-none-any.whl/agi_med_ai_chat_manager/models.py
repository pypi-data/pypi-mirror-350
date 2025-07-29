class ServiceUnavailableException(Exception):
    def __init__(self, message="Сервис недоступен. Возможно, требуется включить VPN или сервис не запущен."):
        super().__init__(message)


class UnsupportedModelException(Exception):
    def __init__(self, model_names, message="Модель недоступна. Список доступных моделей - {model_names}"):
        super().__init__(message.format(model_names=model_names))
