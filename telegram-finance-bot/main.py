"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import aiogram.utils.markdown as style


from db import db
from middlewares.middlewares import AccessMiddleware
from repositories import budgets, expenses, exceptions, tips, users
from repositories.categories import Categories


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение"""
    users.check_user(message.from_user["id"])
    await message.answer(
        "<b>Бот для учёта финансов</b>\n\n"
        "\U00002757Чтобы продолжить, установите свой ежемесячный лимит -> /limits",
        parse_mode="HTML")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """Отправляет помощь по боту"""
    await message.answer(
        "Добавить расход: 250 такси\n"
        "Лайфхаки: /tips\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Установить ежемесячный лимит: /limits\n"
        "Категории трат: /categories\n\n")


class NewTipState(StatesGroup):
    body_tip = State()


# only for admin
@dp.message_handler(commands=['new_tip'])
async def add_new_tip(message: types.Message):
    """Добавление нового лайфхака"""
    flag = users.check_user(message.from_user["id"])
    if flag == 'is_admin':
        await message.answer("Введите текст:")
        await NewTipState.body_tip.set()
    else:
        pass


@dp.message_handler(state=NewTipState.body_tip)
async def get_limit(message: types.Message, state: FSMContext):
    await state.update_data(body_tip=message.text)
    data = await state.get_data()
    answer_message = tips.add_new_tip(message.text)
    await message.answer(answer_message, parse_mode="HTML")
    await state.finish()


@dp.message_handler(commands=['tips'])
async def send_tips(message: types.Message):
    """Отправляет рандомный лайфхак"""
    answer_message = tips.get_random_tip()
    await message.answer(answer_message, parse_mode="HTML")


class LimitState(StatesGroup):
    limit = State()


@dp.message_handler(commands=['limits'])
async def add_limits(message: types.Message):
    """Добавляет ежемесячный лимит"""
    await message.answer("Введите сумму:")
    await LimitState.limit.set()

@dp.message_handler(state=LimitState.limit)
async def get_limit(message: types.Message, state: FSMContext):
    if message.text.isdigit() is False:
        await message.answer("Введите корректную сумму:")
    else:
        await state.update_data(limit=message.text)
        data = await state.get_data()
        answer_message = budgets.add_monthly_budget(limit=data['limit'], id_user=message.from_user["id"])
        await message.answer(answer_message)
        await state.finish()
        await send_help(message)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалено"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "<b>Категории трат</b>\n\n" +\
            "Базовые\n" +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories if c.is_base_expense==1])) +\
            "\n\nОстальные\n" +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories if c.is_base_expense==0]))
    await message.answer(answer_message, parse_mode="HTML")


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics(id_user=message.from_user["id"])
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics(id_user=message.from_user["id"])
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last(id_user=message.from_user["id"])
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(raw_message=message.text, id_user=message.from_user["id"])
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics(id_user=message.from_user['id'])}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
