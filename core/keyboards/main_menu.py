from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍 Перевести сленг"),
            KeyboardButton(text="🎲 Случайный сленг")
        ],
        [
            KeyboardButton(text="ℹ️ О боте")
        ]
    ],
    resize_keyboard=True
)

def get_random_slang_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f"random_slang_{i}") for i in range(1, 6)]
        ]
    )

# Клавиатура после случайного сленга
post_random_slang_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎲 Сгенерировать ещё"),
            KeyboardButton(text="🏠 В меню")
        ]
    ],
    resize_keyboard=True
)

def mode_button(mode: str) -> InlineKeyboardMarkup:
    mode_names = {
        'ai': '🤖 AI',
        'urban': '📚 Urban+Яндекс',
        'arena': '⚔️ Арена'
    }
    text = f"Режим: {mode_names.get(mode, '🤖 AI')}"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data="change_mode"),
                InlineKeyboardButton(text="ℹ️ О режимах", callback_data="about_modes")
            ]
        ]
    )
    return kb

def mode_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤖 AI", callback_data="set_mode_ai")],
            [InlineKeyboardButton(text="📚 Urban+Яндекс", callback_data="set_mode_urban")],
            [InlineKeyboardButton(text="⚔️ Арена", callback_data="set_mode_arena")],
            [InlineKeyboardButton(text="ℹ️ О режимах", callback_data="about_modes")],
        ]
    )

def modes_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Сменить режим", callback_data="change_mode")],
            [InlineKeyboardButton(text="ℹ️ О режимах", callback_data="about_modes")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_translate")]
        ]
    )

def post_answer_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚙️ Режимы", callback_data="modes_menu")
            ]
        ]
    ) 