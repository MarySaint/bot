from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters
from ai import recommend_engine

async def personal_recommendation(update: Update, context: CallbackContext):
    data = await recommend_engine.run(update, context)
    if not data:
        await update.message.reply_text("Вы еще не заказывали ничего. Попробуйте что-то из меню ✅")
        return
    await update.message.reply_text(data)

def get():
    return [MessageHandler(filters.Text("Персональная рекомендация"), personal_recommendation)]
