import requests
import json

BASE_URL = "http://localhost:8000"

class IntegrationClient:
    def __init__(self):
        self.base_url = BASE_URL
    
    def create_order(self, item_id, quantity):
        """创建订单"""
        url = f"{self.base_url}/orders/"
        payload = {
            "item_id": item_id,
            "quantity": quantity
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def get_order(self, order_id):
        """获取订单信息"""
        url = f"{self.base_url}/orders/{order_id}"
        response = requests.get(url)
        return response.json()
    
    def pay_order(self, order_id, amount):
        """支付订单"""
        url = f"{self.base_url}/orders/{order_id}/pay"
        payload = {
            "order_id": order_id,
            "amount": amount
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def check_inventory(self, item_id):
        """检查库存"""
        url = f"{self.base_url}/inventory/{item_id}"
        response = requests.get(url)
        return response.json()

if __name__ == "__main__":
    # 示例用法
    client = IntegrationClient()
    
    # 创建订单
    print("Creating order...")
    result = client.create_order("item1", 2)
    print(f"Create order result: {result}")
    
    if result.get("status") == "success":
        order_id = result["order_id"]
        
        # 获取订单信息
        print(f"\nGetting order {order_id}...")
        order = client.get_order(order_id)
        print(f"Order details: {order}")
        
        # 支付订单
        print(f"\nPaying order {order_id}...")
        payment_result = client.pay_order(order_id, 200.0)
        print(f"Payment result: {payment_result}")
        
        # 再次获取订单信息，确认状态
        print(f"\nGetting updated order {order_id}...")
        updated_order = client.get_order(order_id)
        print(f"Updated order details: {updated_order}")
    
    # 检查库存
    print("\nChecking inventory...")
    inventory = client.check_inventory("item1")
    print(f"Inventory info: {inventory}")