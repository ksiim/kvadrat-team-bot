from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


async def generate_start_text(message):
    return f"Привет, {message.from_user.full_name}! Я - бот, который будет следить за твоими платежами"

start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Добавить платеж",
            callback_data="add_payment"
        )]
    ]
)