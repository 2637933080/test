from locust import HttpUser, task, between
import random

class OrderSystemUser(HttpUser):
    # 用户在执行任务之间等待1到3秒
    wait_time = between(1, 3)
    
    # 商品列表用于测试
    items = ['item1', 'item2', 'item3']
    
    def on_start(self):
        """每个用户开始时先创建一个订单，以便后续测试支付等功能"""
        self.created_orders = []  # 存储创建的订单ID
        
    @task(3)
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
                # 如果订单创建成功，保存订单ID用于后续测试
                try:
                    response_data = response.json()
                    if response_data.get('status') == 'success':
                        self.created_orders.append(response_data.get('order_id'))
                except:
                    pass
                response.success()
            elif response.status_code == 400:
                # 如果是库存不足等预期错误，也视为成功完成请求
                response.success()
            else:
                response.failure(f"Got unexpected response code: {response.status_code}")
    
    @task(1)
    def get_order(self):
        """获取订单信息的任务"""
        if self.created_orders:
            order_id = random.choice(self.created_orders)
            self.client.get(f"/orders/{order_id}")
        else:
            # 如果没有创建过订单，则随机生成一个ID测试
            order_id = f"order_{random.randint(1, 1000)}"
            self.client.get(f"/orders/{order_id}", 
                           catch_response=True)
    
    @task(2)
    def check_inventory(self):
        """检查库存的任务"""
        item_id = random.choice(self.items)
        self.client.get(f"/inventory/{item_id}")
    
    @task(1)
    def pay_for_order(self):
        """为订单付款的任务"""
        if self.created_orders:
            order_id = random.choice(self.created_orders)
            headers = {'Content-Type': 'application/json'}
            payload = {
                "order_id": order_id,
                "amount": round(random.uniform(10.0, 500.0), 2)
            }
            
            self.client.post(f"/orders/{order_id}/pay",
                            json=payload,
                            headers=headers,
                            catch_response=True)