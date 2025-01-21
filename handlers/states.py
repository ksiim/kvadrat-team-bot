from aiogram.fsm.state import State, StatesGroup

class AddPaymentState(StatesGroup):
    waiting_for_contract_number = State()
    waiting_for_screenshot = State()