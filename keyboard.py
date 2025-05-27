from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Посмотреть событие"), KeyboardButton(text="Удалить событие")],
        [KeyboardButton(text="Добавить событие")], [KeyboardButton(text="Ближайшее событие")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)