Telegram бот для учёта личных расходов и ведения бюджета, запоминает ваш месячный лимит, присылает полезные подсказки по экономии бюджета.


В переменных окружения надо проставить API токен бота, id администратора бота.

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_ADMIN_ID` — id администратора бота

Предварительно заполните .env файл переменными, указанные выше. SQLite база данных будет лежать в папке проекта `db/finance.db`.

Команды для развертывания:

```
docker build -t tg-finance-bot .

docker run -d --name tg-finance-bot --env-file .env -v ${PWD}:/var/www/telegram-finance-bot tg-finance-bot
```
-------
[Пример развернутого Телеграм бота](https://t.me/suren_finance_bot)
