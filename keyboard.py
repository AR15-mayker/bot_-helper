from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get_groups_keyboard():
    groups = ["Группа 1", "Группа 2", "Группа 3"]
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.add(types.InlineKeyboardButton(
            text=group,
            callback_data=f"group_{group}")
        )
    builder.adjust(2)
    return builder.as_markup()

def get_days_keyboard():
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    builder = InlineKeyboardBuilder()
    for day in days:
        builder.add(types.InlineKeyboardButton(
            text=day,
            callback_data=f"day_{day}")
        )
    builder.adjust(2)
    return builder.as_markup()