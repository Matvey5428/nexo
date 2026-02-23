from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_PATH = 'database.db'

def get_user_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT balance_usdt, balance_rub, trading_volume, verified FROM users WHERE telegram_id=?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "usdt": row[0],
            "rub": row[1],
            "trading_volume": row[2],
            "verified": row[3]
        }
    return {"usdt": 0, "rub": 0, "trading_volume": 0, "verified": 0}

@app.route('/user/<int:user_id>')
def user_info(user_id):
    data = get_user_data(user_id)
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)