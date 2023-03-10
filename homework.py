import logging
import sys
import time
from http import HTTPStatus

import requests
import telegram

from config import bot_token, id_chat, practicum_token
from exceptions import HttpResponseError, ParseError

PRACTICUM_TOKEN = practicum_token
TELEGRAM_TOKEN = bot_token
TELEGRAM_CHAT_ID = id_chat

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка наличия переменных окружения."""
    return all([
        PRACTICUM_TOKEN,
        TELEGRAM_TOKEN,
        TELEGRAM_CHAT_ID
    ])


def check_response_ok(response):
    """Проверка статуса ответа от API."""
    if response.status_code != HTTPStatus.OK:
        logging.error('Статус код API не является ожидаемым!')
        raise HttpResponseError


def get_api_answer(timestamp):
    """Создание get-запроса к API."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
        check_response_ok(response)

    except Exception as error:
        logging.error(f'Эндпоинт {ENDPOINT}, недоступен! Ошибка: {error}.')
        raise HttpResponseError

    return response.json()


def check_response(response):
    """Проверка ответа API на наличие нужных ключей и типов данных."""
    logging.info('Проверка ответа API')

    if not isinstance(response, dict):
        message = 'Ответ API не являтеся словарем!'
        logging.error(message)
        raise TypeError(message)

    if 'homeworks' not in response and 'current_date' not in response:
        message = 'Нет нужного ключа в ответе API!'
        logging.error(message)
        raise KeyError(message)

    homeworks = response.get('homeworks')

    if not isinstance(homeworks, list):
        message = 'Формат данных по ключу "homeworks", не является списком!'
        logging.error(message)
        raise TypeError(message)

    return homeworks


def check_homework_name(homework):
    """Проверка на налчие ключа 'homework_name'."""
    try:
        homework_name = homework['homework_name']
        return homework_name

    except KeyError as error_key:
        message = (f'В ответе API нет ключа "homework_name". '
                   f'{error_key}-{homework}')
        logging.error(message)
        raise KeyError(message)


def check_homework_status(homework):
    """Проверка на налчие ключа 'status'.."""
    try:
        status_work = homework['status']
        logging.debug(f'Найден статус работы: {status_work}')
        return status_work

    except KeyError:
        message = 'Статус домашней работы отсутствует.'
        logging.error(message)
        raise KeyError(message)


def check_homework_verdict(status_work):
    """Проверка на налчие статуса в словаре 'HOMEWORK_VERDICTS'."""
    try:
        verdict = HOMEWORK_VERDICTS[status_work]
        logging.debug('Найден статус домашней работы!')
        return verdict

    except KeyError:
        message = f'Неизвестный статус домашней работы: {status_work}'
        logging.error(message)
        raise KeyError(message)


def parse_status(homework):
    """
    Парсим статус домашней работы.
    Содержащий один из вердиктов словаря HOMEWORK_VERDICTS.
    """
    try:
        homework_name = check_homework_name(homework)
        status_work = check_homework_status(homework)
        verdict = check_homework_verdict(status_work)
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'

    except KeyError:
        raise ParseError


def send_message(bot, message):
    """Отправка сообщения в Telegram."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        logging.debug(f'Сообщение - "{message}", отправлено успешно')
        return True

    except telegram.error.TelegramError as error:
        message = f'Не удалось отправить сообщение из-за ошибки {error}'
        logging.error(message)


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical(
            'Отсутствуют переменные окружения',
            'Прогрмма принудительно остановлена!'
        )
        exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = 0
    old_status_homework = ''
    old_exception = ''

    while True:

        try:
            response_get_api = get_api_answer(timestamp)
            homeworks = check_response(response_get_api)[0]

            if not homeworks:
                logging.error('Нет домашних работ')
                raise IndexError('Нет домашних работ')

            else:
                new_status_homework = parse_status(homeworks)

            if new_status_homework != old_status_homework:
                message = new_status_homework
                send_message(bot, message)
                old_status_homework = new_status_homework

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            new_exception = message
            if new_exception != old_exception:
                send_message(bot, message)
                old_exception = new_exception

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
        stream=sys.stdout
    )
    main()
