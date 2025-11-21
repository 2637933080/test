from locust import HttpUser, task, between
import random

class OrderSystemUser(HttpUser):
    # 用户在执行任务之间等待1到5秒
    wait_time = between(1, 5)
    
    # 商品列表用于测试
    items = ['item1', 'item2', 'item3']
    
    @task(1)
    def create_order(self):
        """创建订单的任务"""
        # 随机选择一个商品和数量
        item_id = random.choice(self.items)
        quantity = random.randint(1, 10)
        
        # 发送创建订单的POST请求
        headers = {'Content-Type': 'application/json'}
        payload = {
            "item_id": item_id,
            "quantity": quantity
        }
        
        with self.client.post("/orders/", 
                             json=payload, 
                             headers=headers, 
                             catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 400:
                # 如果是库存不足等预期错误，也视为成功完成请求
                response.success()
            else:
                response.failure(f"Got unexpected response code: {response.status_code}")
    
    @task(2)
    def check_inventory(self):
        """检查库存的任务，权重为2，执行频率更高"""
        item_id = random.choice(self.items)
        self.client.get(f"/inventory/{item_id}")
    
    def on_start(self):
        """每个用户开始时执行一次"""
        pass