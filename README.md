# Telegram-bot

## Описание
Данный телеграм бот создан, для того чтобы ускорить процесс проверки статуса сдачи проекта после ревью. Бот раз в 10 
минут отправляет запрос к API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы, при 
обновлении статуса он отправляет вам соответствующее уведомление в Telegram. Так же бот логирует свою работу и сообщает
вам о важных проблемах сообщением в Telegram.
## Технологии

```
Python 3.9
python-telegram-bot
```

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:NikolayPetrow23/homework_bot.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv

python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Запустить бота:

```
python homework.py 
```

### Автор

```
Николай Петров
```

