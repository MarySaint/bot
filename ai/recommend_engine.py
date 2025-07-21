import sqlite3

def get_user_orders(user_name):
    conn = sqlite3.connect("bot/database/app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_name = ?", (user_name,))
    orders = cursor.fetchall()
    conn.close()
    return orders

async def run(update, context):
    user = update.effective_user
    user_name = user.full_name if user else None
    if not user_name:
        return None
    orders = get_user_orders(user_name)
    if not orders:
        return None
    # Здесь должен быть анализ заказов и генерация рекомендации через ИИ
    # Пока просто возвращаем заглушку
    return "На основе ваших прошлых заказов мы рекомендуем попробовать новое блюдо! 🍽️"
