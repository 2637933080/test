import unittest
from app.services.inventory import InventoryService

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        self.inventory_service = InventoryService()
    
    def test_check_stock(self):
        # 测试检查库存功能
        stock = self.inventory_service.check_stock('item1')
        self.assertEqual(stock, 100)
        
        # 测试不存在的商品
        stock = self.inventory_service.check_stock('nonexistent_item')
        self.assertEqual(stock, 0)
    
    def test_deduct_stock_success(self):
        # 测试成功扣减库存
        result = self.inventory_service.deduct_stock('item1', 10)
        self.assertTrue(result)
        self.assertEqual(self.inventory_service.check_stock('item1'), 90)
    
    def test_deduct_stock_insufficient(self):
        # 测试库存不足时的扣减
        result = self.inventory_service.deduct_stock('item1', 110)
        self.assertFalse(result)
        self.assertEqual(self.inventory_service.check_stock('item1'), 100)
    
    def test_add_stock_existing_item(self):
        # 测试为已有商品增加库存
        self.inventory_service.add_stock('item1', 10)
        self.assertEqual(self.inventory_service.check_stock('item1'), 110)
    
    def test_add_stock_new_item(self):
        # 测试为新商品增加库存
        self.inventory_service.add_stock('item_new', 25)
        self.assertEqual(self.inventory_service.check_stock('item_new'), 25)

if __name__ == '__main__':
    unittest.main()