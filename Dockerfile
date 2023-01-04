FROM python:3.11

WORKDIR /var/www/telegram-finance-bot

COPY ./ ./

RUN apt update && apt install sqlite3
RUN pip install -r requirements.txt

WORKDIR /var/www/telegram-finance-bot/telegram-finance-bot

ENTRYPOINT ["python", "main.py"]
