import pytest
import requests

def test_service_functionality():
    response = requests.get('http://localhost:5000/health')
    assert response.status_code == 200

def test_database_recovery():
    # 模拟数据库连接中断
    import os
    os.system('docker stop <your_database_container_name>')
    
    response = requests.post('http://localhost:5000/payment', json={'amount': 100})
    assert response.status_code != 200  # 预期会失败

    # 恢复数据库连接
    os.system('docker start <your_database_container_name>')

    response = requests.post('http://localhost:5000/payment', json={'amount': 100})
    assert response.status_code == 200  # 预期会成功