# server.py
from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os

# -----------------------------------------
# Настройка Flask
# -----------------------------------------
app = Flask(__name__, static_folder="static")
import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# -----------------------------------------
# Функция получения данных пользователя
# -----------------------------------------
def get_user_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # создаем таблицу users, если не существует
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            balance_rub REAL DEFAULT 0,
            balance_usdt REAL DEFAULT 0,
            trading_volume REAL DEFAULT 0,
            verified INTEGER DEFAULT 0,
            blocked INTEGER DEFAULT 0
        )
    """)

    # получаем данные пользователя
    cursor.execute("""
        SELECT username, balance_usdt, balance_rub, trading_volume, verified, blocked
        FROM users
        WHERE telegram_id=?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "username": row[0],
            "usdt": row[1],
            "rub": row[2],
            "trading_volume": row[3],
            "verified": row[4],
            "blocked": bool(row[5])
        }
    return {
        "username": "",
        "usdt": 0,
        "rub": 0,
        "trading_volume": 0,
        "verified": 0,
        "blocked": False
    }

# -----------------------------------------
# API получения данных пользователя
# -----------------------------------------
@app.route('/user/<int:user_id>')
def user_info(user_id):
    data = get_user_data(user_id)
    return jsonify(data)

# -----------------------------------------
# Отдача HTML страниц (фронтенд)
# -----------------------------------------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/exchange')
def exchange():
    return send_from_directory(app.static_folder, 'exchange.html')

@app.route('/withdraw')
def withdraw():
    return send_from_directory(app.static_folder, 'withdraw.html')

# -----------------------------------------
# Запуск сервера
# -----------------------------------------
if __name__ == "__main__":
    # Render будет давать свой порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)