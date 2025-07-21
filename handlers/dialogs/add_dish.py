from telegram.ext import(
                    ContextTypes,
                    ConversationHandler)
                    
                
from telegram import Update
from database import db
from database import models

async def cancel_add_dish(update:Update,context:ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text("Добавление отменено🔙")
     return ConversationHandler.END

async def default(update:Update,context:ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text("Следите за инструкциями...⚠️")

async def start_add_dish(update:Update,context:ContextTypes.DEFAULT_TYPE):
     if 'admin' in context.user_data:
         await update.message.reply_text("Введите название блюда")
         return "name"
     else:
         await update.message.reply_text("Для начала войдите в личный кабинет админа")
         return ConversationHandler.END
    

async def get_name(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
   
    await update.message.reply_text("Сделайте описание в формате:\n"
                                    "[Цена]\n"
                                    "[Теги: Веган/Мясоед/Безглютен/Диабетик]\n"
                                    "[Описание]")
    return "desc"

async def get_desc(update:Update,context:ContextTypes.DEFAULT_TYPE):
       if len(update.message.text.split('\n'))!=3:
            await update.message.reply_text("Описание сделано в неправильном формате❌")
            return "desc"
       else:
        context.user_data["desc"] = update.message.text
        await update.message.reply_text("Отправь фото")
        return "photo"


async def get_photo(update:Update,context:ContextTypes.DEFAULT_TYPE):
       print("фото пришло")
       print(update.message)
       photo = await update.message.photo[-1].get_file()
       binary_photo = await  photo.download_as_bytearray()
       context.user_data["photo"] = binary_photo
       result = save_dish(context.user_data)
       if result: 
            await update.message.reply_text("Блюдо добавлено ✅")
       else:
             await update.message.reply_text("Ошибка при добавлении ☹️")
       return ConversationHandler.END

def save_dish(data):
     name = data["name"]
     photo = data["photo"]
     price,tags,desc = data["desc"].split('\n')
     dish = models.Dish(name,int(price),tags,desc,photo)
     return db.add_dish(dish)