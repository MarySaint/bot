from telegram import (Update, 
                      
                      )
from telegram.ext import (CallbackContext,
                          CallbackQueryHandler,
                          ConversationHandler,
                          ContextTypes, 
                          MessageHandler,
                          filters
                          )

from database import db



async def change_properties(update:Update,context:CallbackContext):
        query = update.callback_query
        context.user_data["dish_id"] = query.data.split("=")[-1]
        await context.bot.delete_message(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id
        )
        query.answer()
        await context.bot.send_message(chat_id = query.message.chat_id, text = "Напишите новые характеристики")
        return "PROPS"
        
async def get_props_dish(update:Update,context:ContextTypes.DEFAULT_TYPE):
    new_props = update.message.text
    if db.update_dish_by_id(dish_id=context.user_data["dish_id"],data=new_props, column="properties"):
            await update.message.reply_text("Блюдо обновлено")
    else:
            await update.message.reply_text("Ошибка")
        

def get():
    change_handler = CallbackQueryHandler(pattern=r"^change_dish_id", callback=change_properties)
    conv_handler = ConversationHandler(
        entry_points=[change_handler],
        states={
            "PROPS": [MessageHandler(filters.TEXT, get_props_dish)]
        },
        fallbacks=[change_handler]
    )
    return [conv_handler]