"""Работа с пользователями"""
import os

from db import db


def check_user(id_user: int):
    user_from_db = db.select_user(id_user)
    if user_from_db is None:
        _add_user(id_user)
    else:
        if user_from_db[0] == int(os.getenv("TELEGRAM_ADMIN_ID")):
            return 'is_admin'
        else:
            return


def _add_user(id_user: int):
    inserted_row_id_user = db.insert("user", {
        "id": id_user,
    })
