import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from core.settings import settings
from core.handlers.basic import start_handler, help_handler, about_handler, slang_button_handler, slang_translate_handler, random_slang_handler, random_slang_callback_handler, to_menu_handler, random_more_handler, SlangStates, router as basic_router
from aiogram.types import BotCommand


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text=f'<b>Бот запущен!</b>')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='<b>Бот остановлен!</b>')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
dp = Dispatcher()
dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)
# регистрируем команды
dp.message.register(start_handler, Command("start"))
dp.message.register(help_handler, Command("help"))
dp.message.register(about_handler, lambda message: message.text == "ℹ️ О боте")
dp.message.register(slang_button_handler, lambda message: message.text == "🔍 Перевести сленг")
dp.message.register(random_slang_handler, lambda message: message.text == "🎲 Случайный сленг")
dp.message.register(random_more_handler, lambda message: message.text == "🎲 Сгенерировать ещё")
dp.message.register(to_menu_handler, lambda message, state=None: message.text == "🏠 В меню", flags={"with_state": True})
dp.callback_query.register(random_slang_callback_handler, lambda c: c.data.startswith("random_slang_"))
dp.message.register(slang_translate_handler, SlangStates.waiting_for_slang)
dp.include_router(basic_router)


async def main():
    # Устанавливаем меню команд Telegram
    await bot.set_my_commands([
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="help", description="Справка по боту")
    ])
    # Настройка диспетчера и запуск обработчиков
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    # Запуск основной асинхронной функции
    import asyncio
    asyncio.run(main())
