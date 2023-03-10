class HttpResponseError(Exception):
    def __init__(self, response):
        message = (
            f'Эндпоинт: {response.url}, недоступен!',
            f'Код ответа {response.status_code}'
        )
        super().__init__(message)


class ParseError(Exception):
    def __init__(self, text):
        message = (
            f'Парсинг ответа API: {text}'
        )
        super().__init__(message)
