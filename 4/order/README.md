# 订单系统

这是一个简单的订单系统，包含以下模块：
- 订单模块
- 库存模块
- 支付模块

## 目录结构

```
.
├── app
│   ├── services
│   │   ├── __init__.py
│   │   ├── inventory.py          # 库存管理模块
│   │   ├── orders.py             # 订单管理模块
│   │   └── payments.py           # 支付管理模块
│   ├── __init__.py
│   └── main.py                  # FastAPI应用入口
├── integration
│   ├── integration_client.py     # 集成测试客户端
│   └── requests.http             # VS Code REST Client插件使用的HTTP请求示例
├── tests
│   ├── __init__.py
│   ├── test_inventory.py         # 库存模块单元测试
│   ├── test_orders.py            # 订单模块单元测试
│   └── test_payments.py          # 支付模块单元测试
├── locustfile.py                 # Locust性能测试脚本
├── test_locust.py                # 更复杂的Locust性能测试脚本
└── README.md
```

## 安装依赖

```bash
pip install fastapi uvicorn requests locust
```

如果遇到urllib3版本兼容性问题，可以指定版本：
```bash
pip install "urllib3<2.0" requests locust
```

## 运行单元测试

```bash
# 运行所有测试
python -m unittest discover tests

# 或者单独运行某个测试
python -m unittest tests.test_inventory
python -m unittest tests.test_orders
python -m unittest tests.test_payments
```

## 启动服务

```bash
uvicorn app.main:app --reload
```

服务将在 `http://localhost:8000` 上运行。

## API接口

- `POST /orders/` - 创建订单
- `GET /orders/{order_id}` - 获取订单信息
- `POST /orders/{order_id}/pay` - 支付订单
- `GET /inventory/{item_id}` - 检查商品库存

## 集成测试

### 使用Python客户端

```bash
python integration/integration_client.py
```

### 使用VS Code REST Client插件

在VS Code中安装REST Client插件后，可以直接打开 [requests.http](integration/requests.http) 文件并点击每个请求旁的"Send Request"按钮来测试API。

## 性能测试

使用Locust进行性能测试：

```bash
# 使用默认的locustfile.py
locust

# 或者指定特定的测试文件
locust -f test_locust.py
```

运行上述命令后，在浏览器中打开 `http://localhost:8000`，配置并发用户数和加速率，然后开始测试。

例如，要模拟100个用户以每秒10个用户的速率启动：
1. 在Web界面的"Number of users"字段输入100
2. 在"Spawn rate"字段输入10
3. 点击"Start swarming"按钮开始测试

## 系统设计说明

### 库存模块 (Inventory Service)
- 管理商品库存数量
- 提供检查库存、扣减库存、增加库存功能

### 支付模块 (Payment Service)
- 处理订单支付
- 记录支付状态

### 订单模块 (Order Service)
- 协调库存和支付服务完成下单流程
- 管理订单生命周期

## 测试数据

系统预置了以下商品库存：
- item1: 100个
- item2: 50个
- item3: 75个