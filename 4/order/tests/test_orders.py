import unittest
from app.services.orders import OrderService
from app.services.inventory import InventoryService

class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.order_service = OrderService()
    
    def test_create_order_success(self):
        # 测试成功创建订单
        result = self.order_service.create_order('item1', 5)
        self.assertEqual(result['status'], 'success')
        self.assertIn('order_', result['order_id'])
        
        # 验证订单是否正确创建
        order = self.order_service.get_order(result['order_id'])
        self.assertIsNotNone(order)
        self.assertEqual(order['item_id'], 'item1')
        self.assertEqual(order['quantity'], 5)
        self.assertEqual(order['status'], 'created')
    
    def test_create_order_insufficient_stock(self):
        # 测试库存不足时创建订单
        result = self.order_service.create_order('item1', 101)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], 'Insufficient stock')
    
    def test_pay_order_success(self):
        # 测试成功支付订单
        # 先创建一个订单
        create_result = self.order_service.create_order('item2', 5)
        self.assertEqual(create_result['status'], 'success')
        
        # 然后支付该订单
        order_id = create_result['order_id']
        pay_result = self.order_service.pay_order(order_id, 100.0)
        self.assertEqual(pay_result['status'], 'success')
        
        # 验证订单状态是否更新
        order = self.order_service.get_order(order_id)
        self.assertEqual(order['status'], 'paid')
    
    def test_pay_nonexistent_order(self):
        # 测试支付不存在的订单
        result = self.order_service.pay_order('nonexistent_order', 100.0)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], 'Order not found')

if __name__ == '__main__':
    unittest.main()