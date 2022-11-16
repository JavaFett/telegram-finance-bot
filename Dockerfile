FROM python:3.11

WORKDIR /var/www/telegram-finance-bot

RUN apt update && apt install sqlite3
RUN pip install -r requirements.txt

COPY ./ ./

RUN export `cat .env`

ENTRYPOINT ["python", "main.py"]
