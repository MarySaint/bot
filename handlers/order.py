from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, filters, CallbackQueryHandler
from database import db, models
import sqlite3
from datetime import datetime
from utils.logger import log_action


async def view_cart(update: Update, context: CallbackContext):
    user_data = context.user_data
    if 'card' not in user_data or not user_data['card']:
        await update.message.reply_text("Ваша корзина пуста ✅")
        log_action(user=update.effective_user.username, action="Просмотр пустой корзины")
        return
    cart = user_data['card']
    summary = {}
    total_price = 0
    for dish_id in cart:
        summary[dish_id] = summary.get(dish_id, 0) + 1
    text = "✅ *Ваша корзина:*\n"
    for dish_id, count in summary.items():
        dish_data = db.get_dish_by_id(dish_id)
        if isinstance(dish_data, tuple):
            dish = models.Dish()
            dish.from_tuple(dish_data)
        elif isinstance(dish_data, dict):
            dish = models.Dish()
            dish.name = dish_data['name']
            dish.price = dish_data['price']
        else:
            dish = dish_data
        price = dish.price * count
        total_price += price
        text += f"- {dish.name} x {count} = {price}₽\n"
    text += f"\n*Итого:* {total_price}₽"
    keyboard = [[InlineKeyboardButton("Оформить заказ ✅", callback_data="checkout")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    log_action(user=update.effective_user.username, action="Просмотр корзины")


async def checkout(update: Update, context: CallbackContext):
    query = update.callback_query
    cart = context.user_data.get("card", [])
    if not cart:
        await query.answer("Корзина пуста")
        log_action(user=update.effective_user.username, action="Попытка оформить пустую корзину")
        return
    summary = {}
    total_price = 0
    for dish_id in cart:
        summary[dish_id] = summary.get(dish_id, 0) + 1
    # Корректно вычисляем total_price
    for dish_id, count in summary.items():
        dish_data = db.get_dish_by_id(dish_id)
        if isinstance(dish_data, tuple):
            dish = models.Dish()
            dish.from_tuple(dish_data)
        elif isinstance(dish_data, dict):
            dish = models.Dish()
            dish.name = dish_data['name']
            dish.price = dish_data['price']
        else:
            dish = dish_data
        total_price += dish.price * count
    total_count = sum(summary.values())
    user_name = update.effective_user.full_name if update.effective_user else "unknown"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "в работе"
    # Сохраняем заказ
    conn = sqlite3.connect("bot/database/app.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (count, total_price, date, user_name, status) VALUES (?, ?, ?, ?, ?)",
        (total_count, total_price, date, user_name, status)
    )
    order_id = cursor.lastrowid
    for dish_id, count in summary.items():
        cursor.execute(
            "INSERT INTO orders_dishes (Id_order, Id_dish, count) VALUES (?, ?, ?)",
            (order_id, dish_id, count)
        )
    conn.commit()
    conn.close()
    # Очищаем корзину
    context.user_data["card"] = []
    await query.answer()
    await query.edit_message_text("Ваш заказ оформлен и находится в работе! 🟢")
    log_action(user=update.effective_user.username, action="Оформление заказа клиентом. ID заказа = {order_id} ",level="WARNING")

async def view_orders(update: Update, context: CallbackContext):
    user = update.message.from_user
    conn = sqlite3.connect("bot/database/app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_name = ?", (user.full_name,))
    orders = cursor.fetchall()
    conn.close()
    if not orders:
        await update.message.reply_text("Сделайте заказ ✅")
        log_action(user=user.username, action="Просмотр заказов (нет заказов)")
        return
    text = "✅ *Ваши заказы:*\n"
    for order in orders:
        text += f"\n✅ Заказ №{order[0]} — {order[1]} блюд, {order[2]}₽, статус: {order[5]}\n"
    await update.message.reply_text(text, parse_mode='Markdown')
    log_action(user=user.username, action="Просмотр заказов")

def get():
    return [
        MessageHandler(filters.Text("Корзина"), view_cart),
        CallbackQueryHandler(checkout, pattern=r"^checkout"),
        MessageHandler(filters.Text("Заказы"), view_orders),
    ]
        