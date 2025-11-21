class InventoryService:
    def __init__(self):
        # 初始化库存，简单起见使用字典存储商品ID和库存数量
        self.inventory = {
            'item1': 100,
            'item2': 50,
            'item3': 75
        }
    
    def check_stock(self, item_id):
        """检查商品库存"""
        return self.inventory.get(item_id, 0)
    
    def deduct_stock(self, item_id, quantity):
        """扣减库存"""
        if self.check_stock(item_id) >= quantity:
            self.inventory[item_id] -= quantity
            return True
        return False
    
    def add_stock(self, item_id, quantity):
        """增加库存"""
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity
        return True