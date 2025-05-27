from aiogram import types, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import get_users, get_schedule, add_schedule, delete_schedule
from database.models import Schedule

async def admin_panel(message: types.Message, bot: Bot):
    if not await is_admin(message.from_user.id):
        await message.answer("У вас нет прав доступа к админ-панели")
        return
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Просмотр пользователей",
        callback_data="admin_view_users")
    )
    builder.add(types.InlineKeyboardButton(
        text="Добавить расписание",
        callback_data="admin_add_schedule")
    )
    builder.add(types.InlineKeyboardButton(
        text="Удалить расписание",
        callback_data="admin_delete_schedule")
    )
    await message.answer("Админ-панель:", reply_markup=builder.as_markup())

async def is_admin(user_id: int) -> bool:
    # Здесь можно добавить проверку на админа (например, из БД или config)
    ADMINS = [123456789]  # Замените на ваш ID
    return user_id in ADMINS

async def handle_admin_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    action = callback.data.split('_')[-1]
    
    if action == "users":
        users = await get_users()
        await callback.message.answer("\n".join([f"{u.id}: {u.username}" for u in users]))
    
    elif action == "add":
        await callback.message.answer("Введите данные в формате: группа, день недели, время")
        await state.set_state("admin_add_schedule")
    
    elif action == "delete":
        schedules = await get_schedule()
        builder = InlineKeyboardBuilder()
        for schedule in schedules:
            builder.add(types.InlineKeyboardButton(
                text=f"{schedule.group} - {schedule.day_week} - {schedule.time}",
                callback_data=f"delete_{schedule.id}")
            )
        await callback.message.answer("Выберите расписание для удаления:", reply_markup=builder.as_markup())
    
    elif callback.data.startswith("delete"):
        schedule_id = int(callback.data.split('_')[1])
        await delete_schedule(schedule_id)
        await callback.message.answer("Расписание удалено")

async def handle_admin_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "admin_add_schedule":
        try:
            group, day_week, time = message.text.split(', ')
            await add_schedule(Schedule(
                group=group.strip(),
                day_week=day_week.strip(),
                time=time.strip()
            ))
            await message.answer("Расписание добавлено")
        except Exception as e:
            await message.answer(f"Ошибка: {e}")
        finally:
            await state.clear()