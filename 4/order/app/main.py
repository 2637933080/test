from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.services.orders import OrderService
from app.services.inventory import InventoryService
from app.services.payments import PaymentService

app = FastAPI(title="Order System", description="A simple order system with order, inventory and payment modules")

# 初始化服务
order_service = OrderService()

class OrderRequest(BaseModel):
    item_id: str
    quantity: int

class PaymentRequest(BaseModel):
    order_id: str
    amount: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order System API"}

@app.post("/orders/")
def create_order(order_request: OrderRequest):
    """创建订单"""
    result = order_service.create_order(order_request.item_id, order_request.quantity)
    if result['status'] == 'success':
        return result
    else:
        raise HTTPException(status_code=400, detail=result['message'])

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """获取订单信息"""
    order = order_service.get_order(order_id)
    if order:
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders/{order_id}/pay")
def pay_order(order_id: str, payment_request: PaymentRequest):
    """支付订单"""
    if payment_request.order_id != order_id:
        raise HTTPException(status_code=400, detail="Order ID mismatch")
        
    result = order_service.pay_order(order_id, payment_request.amount)
    if result['status'] == 'success':
        return result
    else:
        raise HTTPException(status_code=400, detail=result.get('message', 'Payment failed'))

@app.get("/inventory/{item_id}")
def check_inventory(item_id: str):
    """检查商品库存"""
    inventory_service = InventoryService()
    stock = inventory_service.check_stock(item_id)
    return {"item_id": item_id, "stock": stock}