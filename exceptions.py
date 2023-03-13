class HttpResponseError(Exception):
    def status_code(self, text):
        return(
            f'Эндпоинт, недоступен!',
            f'Код ответа {text}'
        )


class ParseError(Exception):
    def message_answer(self, text):
        return f'Парсинг ответа API: {text}'
