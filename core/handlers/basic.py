from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery
from core.keyboards.main_menu import main_menu_keyboard, get_random_slang_inline_keyboard, post_random_slang_keyboard, mode_button, mode_menu_keyboard, modes_inline_keyboard, post_answer_inline_keyboard
from core.keyboards.stickers import STICKER_DICE, STICKER_HOURGLASS
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.utils.llm_format import clean_llm_response
from core.services.openrouter import get_openrouter_explanation, get_random_slang_openrouter
from core.utils.text import split_queries, format_ai_answer, format_urban_answer, format_arena_answer, format_api_error
from core.services.urban import get_urban_definition_with_translate
from aiogram.filters import Command
from core.settings import settings
from core.utils.fsm_utils import clear_if_slang_state
from core.states import SlangStates

# Обработчик команды /start
async def start_handler(message: Message, bot: Bot, state: FSMContext):
    await clear_if_slang_state(state)
    user_name = message.from_user.full_name or message.from_user.username or "пользователь"
    await message.answer(
        f"Привет, <b>{user_name}</b>! Я бот для перевода английского сленга. Выбери действие:",
        reply_markup=main_menu_keyboard
    )

# Обработчик кнопки 'О боте'
async def about_handler(message: Message, bot: Bot, state: FSMContext):
    await clear_if_slang_state(state)
    admin_id = settings.bots.admin_id
    admin_username = settings.bots.admin_username
    text = (
        "<b>О боте</b>\n\n"
        "Этот бот помогает переводить и объяснять современный английский сленг.\n"
        "\n<b>Возможности:</b>\n"
        "• Перевод и объяснение сленга с помощью нейросети (AI)\n"
        "• Перевод с использованием Urban Dictionary и Яндекс Переводчика\n"
        "• Режим арены для сравнения разных подходов\n"
        "• Получение случайных сленговых слов для расширения словарного запаса\n"
        "• Удобный выбор режима перевода\n"
        "\n<b>Контакты для связи с администратором:</b>\n"
        f'<a href="https://t.me/{admin_username}">@{admin_username}</a> (нажмите, чтобы написать)\n'
        "\nЕсли у вас есть вопросы, предложения или вы нашли ошибку — пишите!"
    )
    await message.answer(text, parse_mode="HTML")

# Обработчик кнопки 'Перевести сленг'
async def slang_button_handler(message: Message, bot: Bot, state: FSMContext):
    await clear_if_slang_state(state)
    await message.answer(
        "Пожалуйста, отправьте одно или несколько английских слов или фраз для перевода (через запятую, точку с запятой или с новой строки, не более 5 за раз).",
        reply_markup=main_menu_keyboard
    )
    # Получаем текущий режим (или по умолчанию ai)
    data = await state.get_data()
    mode = data.get('mode', 'ai')
    await message.answer("Текущий режим перевода:", reply_markup=mode_button(mode))
    await state.set_state(SlangStates.waiting_for_slang)

# Обработчик кнопки 'Случайный сленг'
async def random_slang_handler(message: Message, bot: Bot, state: FSMContext):
    await clear_if_slang_state(state)
    await message.answer(
        "Сколько случайных сленгов показать?",
        reply_markup=get_random_slang_inline_keyboard()
    )

# Callback-хендлер для генерации случайных сленгов
async def random_slang_callback_handler(callback: CallbackQuery, bot: Bot):
    try:
        await callback.answer()
        count = int(callback.data.replace("random_slang_", ""))
        if count > 5:
            await callback.message.answer("Можно запросить не более 5 случайных сленгов за раз.", reply_markup=main_menu_keyboard)
            return
        wait_msg = await bot.send_sticker(chat_id=callback.message.chat.id, sticker=STICKER_DICE)
        try:
            explanation = await get_random_slang_openrouter(count)
            text = f"<b>Случайные сленги:</b>\n{explanation}"
        except Exception as e:
            text = "Произошла ошибка при обращении к нейросети. Попробуйте позже."
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=wait_msg.message_id)
        text = clean_llm_response(text)
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=post_random_slang_keyboard, parse_mode="HTML")
    except Exception as e:
        await callback.message.answer("Произошла ошибка. Попробуйте ещё раз или обратитесь к администратору.", reply_markup=main_menu_keyboard)

# Обработчик ввода сленга
async def slang_translate_handler(message: Message, bot: Bot, state: FSMContext):
    # Не обрабатывать служебные кнопки как перевод
    if message.text in ["🏠 В меню"]:
        return
    # Получаем режим перевода (ai, urban, arena)
    data = await state.get_data()
    mode = data.get('mode', 'ai')
    queries = split_queries(message.text)
    if not queries:
        await message.answer("Не удалось распознать слова для перевода.", reply_markup=main_menu_keyboard)
        await state.clear()
        await state.update_data(mode=mode)
        return
    if len(queries) > 5:
        await message.answer("Можно переводить не более 5 слов/фраз за раз.", reply_markup=main_menu_keyboard)
        await state.clear()
        await state.update_data(mode=mode)
        return
    wait_msg = await bot.send_sticker(chat_id=message.chat.id, sticker=STICKER_HOURGLASS)
    results = []
    for q in queries:
        try:
            if mode == 'ai':
                explanation = await get_openrouter_explanation(q)
                results.append(format_ai_answer(q, explanation))
            elif mode == 'urban':
                definition, example, definition_tr, example_tr = await get_urban_definition_with_translate(q)
                if not definition_tr:
                    results.append(f"<b>{q}</b>: Не найдено в Urban Dictionary.")
                else:
                    results.append(format_urban_answer(q, definition_tr, example_tr))
            elif mode == 'arena':
                from asyncio import gather
                ai_task = get_openrouter_explanation(q)
                urban_task = get_urban_definition_with_translate(q)
                ai_result, urban_result = await gather(ai_task, urban_task)
                definition, example, definition_tr, example_tr = urban_result
                if not definition_tr:
                    arena_text = f"<b>{q}</b>\n\n🤖 <b>AI:</b>\n{ai_result}\n\n<b>Urban+Яндекс:</b> Не найдено в Urban Dictionary."
                else:
                    arena_text = format_arena_answer(q, ai_result, definition_tr, example_tr)
                results.append(arena_text)
        except Exception as e:
            results.append(format_api_error(q))
    await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
    text = "\n\n".join(results)
    text = clean_llm_response(text)
    await message.answer(text, parse_mode="HTML")
    await message.answer(
        "Если хотите перевести ещё — просто отправьте одно или несколько новых слов или фраз.\n\nВы также можете сменить режим.",
        reply_markup=post_answer_inline_keyboard()
    )
    # Не сбрасываем состояние, чтобы пользователь мог сразу ввести новое слово
    await state.update_data(mode=mode)

# Обработчик команды /help
async def help_handler(message: Message, bot: Bot):
    await message.answer(
        "Это бот для перевода и объяснения английского сленга.\n\n"
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/help — справка\n\n"
        "Вы можете переводить одно или несколько сленговых выражений, а также узнавать случайные современные сленги.",
        reply_markup=main_menu_keyboard
    )

# Обработчик кнопки '🎲 Ещё случайный'
async def random_more_handler(message: Message, bot: Bot):
    await random_slang_handler(message, bot)

# Обработчик кнопки 'В меню'
async def to_menu_handler(message: Message, bot: Bot, state: FSMContext):
    # Если пользователь в состоянии перевода, сбрасываем состояние и показываем главное меню
    await state.clear()
    await message.answer(
        "Вы вернулись в главное меню.",
        reply_markup=main_menu_keyboard
    )

router = Router()

@router.callback_query(lambda c: c.data == "change_mode")
async def change_mode_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=mode_menu_keyboard())
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("set_mode_"))
async def set_mode_callback(callback: CallbackQuery, state: FSMContext):
    mode = callback.data.replace("set_mode_", "")
    await state.update_data(mode=mode)
    await callback.message.edit_reply_markup(reply_markup=mode_button(mode))
    await callback.answer(f"Режим изменён: {mode}")

@router.callback_query(lambda c: c.data == "about_modes")
async def about_modes_callback(callback: CallbackQuery):
    text = (
        "<b>Режимы перевода:</b>\n\n"
        "🤖 <b>AI</b> — нейросеть объясняет сленг на русском языке.\n\n"
        "📚 <b>Urban+Яндекс</b> — определение берётся из Urban Dictionary и переводится на русский через Яндекс Переводчик.\n\n"
        "⚔️ <b>Арена</b> — бот показывает оба варианта: и нейросеть, и Urban+Яндекс, чтобы вы могли сравнить ответы."
    )
    await callback.answer()
    await callback.message.answer(text, parse_mode="HTML")

# Обработчик кнопки 'Назад' (inline)
@router.callback_query(lambda c: c.data == "back_to_translate")
async def back_to_translate_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Если хотите перевести ещё — просто отправьте одно или несколько новых слов или фраз.\n\nВы также можете сменить режим.",
        reply_markup=post_answer_inline_keyboard()
    )
    await callback.answer()

# Обработчик inline-кнопки 'Режимы'
@router.callback_query(lambda c: c.data == "modes_menu")
async def modes_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=modes_inline_keyboard())
    await callback.answer()
