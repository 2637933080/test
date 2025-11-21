from .inventory import InventoryService
from .payments import PaymentService

class OrderService:
    def __init__(self):
        self.orders = {}
        self.order_counter = 0
        self.inventory_service = InventoryService()
        self.payment_service = PaymentService()
    
    def create_order(self, item_id, quantity):
        """
        创建订单
        """
        # 检查库存
        if self.inventory_service.check_stock(item_id) < quantity:
            return {'status': 'failed', 'message': 'Insufficient stock'}
        
        # 扣减库存
        if not self.inventory_service.deduct_stock(item_id, quantity):
            return {'status': 'failed', 'message': 'Failed to deduct stock'}
        
        # 创建订单
        self.order_counter += 1
        order_id = f"order_{self.order_counter}"
        order = {
            'order_id': order_id,
            'item_id': item_id,
            'quantity': quantity,
            'status': 'created'
        }
        self.orders[order_id] = order
        
        return {'status': 'success', 'order_id': order_id, 'message': 'Order created successfully'}
    
    def get_order(self, order_id):
        """获取订单详情"""
        return self.orders.get(order_id, None)
    
    def pay_order(self, order_id, amount):
        """为订单付款"""
        order = self.orders.get(order_id)
        if not order:
            return {'status': 'failed', 'message': 'Order not found'}
        
        # 处理支付
        payment_result = self.payment_service.process_payment(order_id, amount)
        if payment_result['status'] == 'success':
            order['status'] = 'paid'
            
        return payment_result