import random
from db import db


def add_new_tip(text):
    inserted_row_id = db.insert("tip", {
        "body": text
    })
    return "\U00002705 Лайфхак добавлен:\n" \
           f"{text}"


def get_random_tip() -> str:
    cursor = db.get_cursor()
    cursor.execute("SELECT body FROM tip")
    all_tips_from_db = cursor.fetchall()
    random_tip = random.choice(all_tips_from_db)[0]
    return random_tip
