"""Работа с бюджетом, добавление, редактирование"""
from datetime import datetime
from calendar import monthrange

from db import db


def add_monthly_budget(limit: int, id_user: int) -> str:
    inserted_row_id = db.insert("budget", {
        "monthly_limit": limit,
        "id_user": id_user
    })
    return f"\U00002705 Лимит {limit} сохранен"


def get_daily_budget_limit(id_user) -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    monthly_budget = int(get_monthly_budget_limit(id_user) / get_days_in_month_count())
    return monthly_budget


def get_monthly_budget_limit(id_user: int) -> int:
    """Возвращает месячный лимит трат для основных базовых трат"""
    cursor = db.get_cursor()
    cursor.execute(f"SELECT * FROM budget WHERE id_user={id_user}")
    result = cursor.fetchall()[-1][1]
    return result


def get_days_in_month_count() -> int:
    """Возвращает количество дней в текущем месяце"""
    current_year = datetime.now().year
    current_month = datetime.now().month

    days = monthrange(current_year, current_month)[1]
    return days
