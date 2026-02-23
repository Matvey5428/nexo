import sqlite3

# Подключаемся к базе (создаст файл, если его нет)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Таблица пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id BIGINT UNIQUE,
    username TEXT,
    balance_usdt REAL DEFAULT 0,
    balance_rub REAL DEFAULT 0,
    verified INTEGER DEFAULT 0
)
''')

# Таблица транзакций
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    amount REAL,
    currency TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()
print("База данных создана и таблицы готовы!")