import flask
from flask import Flask, request, jsonify
import sqlite3
from threading import Thread

app = Flask(__name__)

# 创建数据库
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute("INSERT INTO users VALUES ('admin', 'password')")
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # 不安全的 SQL 查询
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})

def run_app():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    # 在单独的线程中运行 Flask 应用
    thread = Thread(target=run_app)
    thread.start()
    # 主线程可以继续执行其他任务
    print("Flask app is running in the background")