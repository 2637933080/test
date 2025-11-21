import unittest
from app.services.payments import PaymentService

class TestPaymentService(unittest.TestCase):
    def setUp(self):
        self.payment_service = PaymentService()
    
    def test_process_payment_success(self):
        # 测试支付成功情况
        result = self.payment_service.process_payment('order_1', 100.0)
        self.assertEqual(result['status'], 'success')
        self.assertIn('txn_', result['transaction_id'])
    
    def test_process_payment_failed(self):
        # 测试支付失败情况（金额无效）
        result = self.payment_service.process_payment('order_2', -50.0)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], 'Invalid amount')
    
    def test_get_payment_status(self):
        # 测试获取支付状态
        self.payment_service.process_payment('order_3', 150.0)
        status = self.payment_service.get_payment_status('order_3')
        self.assertEqual(status, 'success')
        
        # 测试获取未支付订单的状态
        status = self.payment_service.get_payment_status('nonexistent_order')
        self.assertEqual(status, 'not_found')

if __name__ == '__main__':
    unittest.main()