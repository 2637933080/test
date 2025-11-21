# Checkout 微服务测试项目

## 项目概述

这是一个简单的基于 Flask 的微服务，用于处理结账功能。该服务接收商品列表及其价格和数量，并计算总金额。

## 系统要求

- Python 3.11
- Flask
- pytest
- requests

## 安装步骤

1. 克隆或下载此项目
2. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```

## 运行服务

可以通过以下方式直接运行服务：
```
python app/checkout_service.py
```

服务将在 `http://localhost:5000` 上启动。

## API 接口

### POST /checkout

计算购物车中商品的总价。

#### 请求示例
```json
{
  "items": [
    {
      "price": 20,
      "quantity": 3
    }
  ]
}
```

#### 响应示例
```json
{
  "total": 60,
  "status": "ok"
}
```

如果购物车为空，则返回错误：
```json
{
  "error": "empty cart"
}
```

## 运行测试

使用 pytest 运行测试：
```
pytest
```

生成 HTML 测试报告：
```
pytest --html=report.html --self-contained-html
```

## CI/CD

该项目配置了 GitHub Actions，在每次推送时自动运行测试。