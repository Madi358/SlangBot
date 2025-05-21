from aiogram.fsm.context import FSMContext
from core.states import SlangStates

async def clear_if_slang_state(state: FSMContext):
    state_name = await state.get_state()
    if state_name == SlangStates.waiting_for_slang.state:
        await state.clear() 