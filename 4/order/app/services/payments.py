class PaymentService:
    def __init__(self):
        self.payment_status = {}
    
    def process_payment(self, order_id, amount):
        """
        处理支付
        简化处理：假设所有支付都会成功
        """
        # 模拟支付处理
        if amount > 0:
            self.payment_status[order_id] = 'success'
            return {'status': 'success', 'transaction_id': f'txn_{order_id}'}
        else:
            self.payment_status[order_id] = 'failed'
            return {'status': 'failed', 'message': 'Invalid amount'}
    
    def get_payment_status(self, order_id):
        """获取支付状态"""
        return self.payment_status.get(order_id, 'not_found')