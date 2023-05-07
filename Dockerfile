FROM python:3.11-alpine

WORKDIR /var/www/telegram-finance-bot

COPY ./ ./

RUN apk update && apk add --no-cache sqlite
RUN pip install -r requirements.txt

RUN export `cat .env`

WORKDIR /var/www/telegram-finance-bot/telegram-finance-bot

ENTRYPOINT ["python", "main.py"]