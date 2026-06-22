import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import logging

# ===== НАСТРОЙКИ =====
TOKEN = '8605528496:AAHAQQv_qK3ukUTCDjrAIwAnE--643k4ti0'  # СЮДА ВСТАВЬТЕ СВОЙ ТОКЕН

# Список постов (4 штуки)
POSTS = [
    "🔥 Пост 1: Супер-скидка 50%! Промокод BOT50",
    "🚀 Пост 2: Курс Python всего за 1 рубль!",
    "💡 Пост 3: Телеграм-канал с мемами — подпишись!",
    "🎁 Пост 4: Розыгрыш iPhone 15 — участвуй!"
]

CHAT_ID = None  # Сюда запишется ID вашего чата
logging.basicConfig(level=logging.INFO)

# ===== ФУНКЦИЯ ОТПРАВКИ ПОСТА =====
async def send_post(bot, index):
    if CHAT_ID is None:
        return
    text = f"📢 Пост {index+1} из {len(POSTS)}:\n\n{POSTS[index]}"
    keyboard = [[InlineKeyboardButton("➡️ Следующий пост", callback_data=f"next_{index}")]]
    await bot.send_message(CHAT_ID, text, reply_markup=InlineKeyboardMarkup(keyboard))

# ===== БЕСКОНЕЧНЫЙ ЦИКЛ ОТПРАВКИ КАЖДЫЕ 30 МИНУТ =====
async def scheduler(bot):
    index = 0
    while True:
        await send_post(bot, index)
        index = (index + 1) % len(POSTS)
        await asyncio.sleep(1800)  # 1800 секунд = 30 минут

# ===== КОМАНДА /start =====
async def start(update, context):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("✅ Бот запущен! Посты пойдут каждые 30 минут.")
    if not hasattr(context.application, "scheduler_task"):
        context.application.scheduler_task = asyncio.create_task(scheduler(context.bot))

# ===== КОМАНДА /stop =====
async def stop(update, context):
    if hasattr(context.application, "scheduler_task"):
        context.application.scheduler_task.cancel()
        del context.application.scheduler_task
        await update.message.reply_text("⏹ Остановлено.")
    else:
        await update.message.reply_text("⏹ Бот уже остановлен.")

# ===== ОБРАБОТКА КНОПКИ "СЛЕДУЮЩИЙ" =====
async def button(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("next_"):
        index = int(data.split("_")[1])
        next_index = (index + 1) % len(POSTS)
        await send_post(context.bot, next_index)
        await query.edit_message_text(f"✅ Пост {next_index+1} отправлен по кнопке.")

# ===== ЗАПУСК =====
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CallbackQueryHandler(button))
    print("✅ Бот запущен! Идите в Telegram и напишите /start")
    app.run_polling()

if __name__ == "__main__":
    main()