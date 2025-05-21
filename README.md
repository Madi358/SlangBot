# Telegram SlangBot

Бот для перевода и объяснения современного английского сленга с помощью нейросети и Urban Dictionary + Яндекс Переводчика.

## Возможности
- Перевод и объяснение сленга с помощью нейросети (AI)
- Перевод с использованием Urban Dictionary и Яндекс Переводчика
- Режим арены для сравнения разных подходов
- Получение случайных сленговых слов
- Удобный выбор режима перевода прямо в чате

## Быстрый старт

1. **Клонируйте репозиторий и перейдите в папку проекта:**
   ```bash
   git clone <repo_url>
   cd SlangBot
   ```

2. **Создайте и активируйте виртуальное окружение (опционально):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env` на основе примера ниже и заполните своими ключами:**
   ```
   TOKEN_API=your_telegram_bot_token
   ADMIN_ID=your_telegram_user_id
   OPENROUTER_API_KEY=your_openrouter_api_key
   YANDEX_API_KEY=your_yandex_translate_api_key
   YANDEX_FOLDER_ID=your_yandex_folder_id
   ```

5. **Запустите бота:**
   ```bash
   python main.py
   ```

## Пример .env
См. файл `.env.example` или используйте шаблон выше.

## Контакты
Если возникли вопросы или предложения — пишите админу (ID берётся из переменной окружения `ADMIN_ID`).

---

**Удачного использования!**
