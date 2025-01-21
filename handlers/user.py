from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, FSInputFile
)

from bot import dp, bot

from models.dbs.orm import Orm
from models.dbs.models import *

from .callbacks import *
from .markups import *
from .states import *

@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()
    
    await Orm.create_user(message)
    await send_start_message(message)
    
async def send_start_message(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=await generate_start_text(message),
        reply_markup=start_markup
    )
    
@dp.callback_query(F.data == 'add_payment')
async def add_payment_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text="Введите порядковый номер договора",
    )
    
    await state.set_state(AddPaymentState.waiting_for_contract_number)
    
@dp.message(AddPaymentState.waiting_for_contract_number)
async def waiting_for_contract_number_handler(message: Message, state: FSMContext):
    await state.update_data(contract_number=message.text)
    
    await message.answer(
        text="Совершите перевод по реквизитам 89058083899 Тинькофф Банк\nПолучатель Александр Викторович М\n\nи отправьте скриншот оплаты",
    )
    
    await state.set_state(AddPaymentState.waiting_for_screenshot)
    
@dp.message(AddPaymentState.waiting_for_screenshot)
async def waiting_for_screenshot_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    
    contract_number = data.get('contract_number')
    
    screenshot = message.photo[-1].file_id
    
    await message.answer(
        text="Платеж успешно добавлен",
        reply_markup=start_markup
    )
    
    await send_message_to_admins(contract_number, screenshot)
    
    await state.clear()
    
async def send_message_to_admins(contract_number, screenshot):
    admins = await Orm.get_all_admins()
    
    for admin in admins:
        await bot.send_photo(
            chat_id=admin.telegram_id,
            photo=screenshot,
            caption=f"Поступил новый платеж по договору {contract_number}"
        )