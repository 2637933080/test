import requests
import time

# 等待一段时间确保服务器已启动
time.sleep(2)

try:
    # 正常登录
    response = requests.post('http://localhost:5000/login', data={'username': 'admin', 'password': 'password'})
    print("Normal login:", response.json())
except requests.exceptions.ConnectionError:
    print("无法连接到服务器，请确保 app.py 正在运行")

try:
    # SQL 注入
    response = requests.post('http://localhost:5000/login', data={'username': "' OR 1=1 --", 'password': 'anything'})
    print("SQL injection:", response.json())
except requests.exceptions.ConnectionError:
    print("无法连接到服务器，请确保 app.py 正在运行")