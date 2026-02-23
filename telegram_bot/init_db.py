import sqlite3
import os

# Берём абсолютный путь к текущей папке скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Создаём соединение с базой
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Создаём таблицу users, если не существует
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT DEFAULT '',
    balance_rub REAL DEFAULT 0,
    balance_usdt REAL DEFAULT 0,
    trading_volume REAL DEFAULT 0,
    verified INTEGER DEFAULT 0,
    blocked INTEGER DEFAULT 0
)
""")

# Добавляем тестового пользователя
cur.execute("""
INSERT OR IGNORE INTO users (telegram_id, username)
VALUES (?, ?)
""", (703924219, 'test_user'))

conn.commit()
conn.close()
print("База и таблица созданы успешно!")