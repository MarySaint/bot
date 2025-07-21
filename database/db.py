import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
from database import models

# Получаем абсолютный путь к файлу базы данных относительно текущего файла

conn =  sqlite3.connect("bot/database/app.db")

cursor = conn.cursor()

def get_user_by_phone(phone):
    cursor.execute("select * from users where phone = ?",(phone,))
    return cursor.fetchone()
def add_dish(d: models.Dish):
    try:
        cursor.execute("INSERT INTO dishes(name,price,photo,tags,description,properties,ans_neurlink) values(?,?,?,?,?,?,?)",d.to_tuple())
        conn.commit()
        return True 
    except Exception as e: 
        print(e)
        return False
    
def get_dishes():
    cursor.execute("SELECT * FROM dishes")
    dishes = [] 
    for r in cursor.fetchall():
        dish = models.Dish()
        dish.from_tuple(r)
        dishes.append(dish)
    return dishes

def get_dish_by_id(dish_id):
    cursor.execute("select * from dishes where id = ?",(dish_id,))
    return cursor.fetchone()


def update_dish_by_id(dish_id,data, column):
    try:
        cursor.execute(f"Update dishes set {column} = ? where id = ?",(data,dish_id))
        conn.commit()
        return True 
    except Exception as e:
        print(e)
        return False
def get_ans_neurlink(dish_id):
      cursor.execute("select ans_neurlink from dishes where id = ?",(dish_id,))
      ans_neurlink = cursor.fetchone()[0]
      return ans_neurlink
    