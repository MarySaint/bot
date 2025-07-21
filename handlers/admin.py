import sqlite3
from telegram.ext import(
                    CommandHandler,
                    ContextTypes,
                    ConversationHandler,
                    MessageHandler,
                    filters)
                    

from telegram import Update,ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
from utils.logger import log_action
from utils import validation
from database import db
from database import models
from handlers.dialogs.add_dish import *

async def admin(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите номер телефона 📞 в формате 80001234567 ")
    return "phone"

async def get_phone(update:Update,context:ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    if validation.validate_phone_number(phone):
        user =  db.get_user_by_phone(phone)
        if user:
            context.user_data["admin"] = user
            keyboard = [
                ["Добавить➕"],
                ["Показать блюда👁‍🗨"],
                ["Заказы"]
            ]
            await update.message.reply_text("Добро пожаловать в личный кабинет 👋",
                                            reply_markup=ReplyKeyboardMarkup(keyboard))
            #логирование
            log_action(user=update.effective_user.username, action="Вход в личный кабинет админа",level="INFO")
            return ConversationHandler.END
        else:
             await update.message.reply_text("Пользователь не найден ❌")
             #логирование
             log_action(user=update.effective_user.username, action="Вход в личный кабинет админа",level="ERROR")
    else:
        await update.message.reply_text("Введенный номер некорректен 🔴")
         #логирование
        log_action(user=update.effective_user.username, action="Вход в личный кабинет админа",level="ERROR")

async def admin_view_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("bot/database/app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    if not orders:
        await update.message.reply_text("Нет заказов")
        return
    text = "✅ *Все заказы:*\n"
    for order in orders:
        text += f"\n✅ Заказ №{order[0]} — {order[4]} — {order[1]} блюд, {order[2]}₽, статус: {order[5]}\n"
    await update.message.reply_text(text, parse_mode='Markdown')


def get():
    login_handler = ConversationHandler(
        entry_points=[CommandHandler("admin",admin)],
        states={
            "phone": [MessageHandler(filters.TEXT,get_phone)]
        },
        fallbacks=[]
    )
    add_dish_handler = ConversationHandler(
         entry_points=[MessageHandler(filters.Text("Добавить➕"),start_add_dish)],
         states={
              "name": [MessageHandler(filters.TEXT&~filters.COMMAND,get_name),
                       CommandHandler("cancel",cancel_add_dish)],
              "desc": [MessageHandler(filters.TEXT&~filters.COMMAND,get_desc),
                       CommandHandler("cancel",cancel_add_dish)],
              "photo":[
                   MessageHandler(filters.PHOTO,get_photo),
                   CommandHandler("cancel",cancel_add_dish)]
         },
         fallbacks=[CommandHandler("cancel",cancel_add_dish)]
    )
   
    admin_orders_handler = MessageHandler(filters.Text("Заказы"), admin_view_orders)
    return [login_handler,add_dish_handler,admin_orders_handler]








          
     
 
     
    
    