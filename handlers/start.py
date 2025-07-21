from telegram.ext import CommandHandler,ContextTypes
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
   keybord = [
      ["Показать блюда"],
      ["Корзина"],
      ["Заказы"]
   ]
   await update.message.reply_text(
    """
👋 Добро пожаловать в ресторан FitFood! 
 Я помогу вам выбрать идеальное блюдо, рассчитать калории и оформить заказ 🍽️
    """,
    reply_markup=ReplyKeyboardMarkup(keybord, resize_keyboard=True)
)

def get():
    return [CommandHandler("start",start)]


    


