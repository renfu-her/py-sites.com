# Quick Orders System - Project Plan

## Project Overview

Based on MVC Shopping project architecture, develop a fast ordering system specifically designed for restaurant/beverage shop order management.

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy with Flask-Migrate
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Processing**: Pillow (PIL)
- **Authentication**: Flask-Login

## Database Configuration

- **Username**: root
- **Password**: (empty)
- **Database Name**: quick-orders

## Database Model Design

### 1. Users (User Table)
```sql
- id (Primary Key)
- name (Name) - VARCHAR(100), NOT NULL
- password (Password) - VARCHAR(255), NOT NULL
- email (Email) - VARCHAR(255), UNIQUE, NOT NULL
- phone (Phone) - VARCHAR(20)
- address (Address) - TEXT
- is_admin (Is Admin) - BOOLEAN, DEFAULT FALSE
- is_active (Is Active) - BOOLEAN, DEFAULT TRUE
- created_at (Created At) - DATETIME
- updated_at (Updated At) - DATETIME
```

### 2. Product (Product Table)
```sql
- id (Primary Key)
- name (Product Name) - VARCHAR(255), NOT NULL
- price (Base Price) - DECIMAL(10,2), NOT NULL
- special_price (Special Price) - DECIMAL(10,2), DEFAULT 0
- cold_price (Cold Drink Price) - DECIMAL(10,2), DEFAULT 0
- hot_price (Hot Drink Price) - DECIMAL(10,2), DEFAULT 0
- description (Description) - TEXT
- is_active (Is Active) - BOOLEAN, DEFAULT TRUE
- created_at (Created At) - DATETIME
- updated_at (Updated At) - DATETIME
```

### 3. ProductImage (产品图片表)
```sql
- id (主键)
- product_id (产品ID) - INT, FOREIGN KEY
- image (图片路径) - VARCHAR(500), NOT NULL
- sort (排序) - INT, DEFAULT 0
- is_active (是否激活) - BOOLEAN, DEFAULT TRUE
- created_at (创建时间) - DATETIME
```

### 4. ProductIngredient (产品配料表)
```sql
- id (主键)
- product_id (产品ID) - INT, FOREIGN KEY
- name (配料名称) - VARCHAR(255), NOT NULL
- price (配料价格) - DECIMAL(10,2), DEFAULT 0
- is_active (是否激活) - BOOLEAN, DEFAULT TRUE
- created_at (创建时间) - DATETIME
```

### 5. Store (店铺表)
```sql
- id (主键)
- product_id (产品ID) - INT, FOREIGN KEY
- name (店铺名称) - VARCHAR(255), NOT NULL
- description (店铺描述) - TEXT
- work_time (营业时间) - VARCHAR(100)
- address (店铺地址) - TEXT
- phone (店铺电话) - VARCHAR(20)
- is_active (是否激活) - BOOLEAN, DEFAULT TRUE
- created_at (创建时间) - DATETIME
- updated_at (更新时间) - DATETIME
```

### 6. Order (订单表)
```sql
- id (主键)
- user_id (用户ID) - INT, FOREIGN KEY, NULLABLE (支持游客订单)
- order_number (订单号) - VARCHAR(50), UNIQUE, NOT NULL
- customer_name (客户姓名) - VARCHAR(255), NOT NULL
- customer_phone (客户电话) - VARCHAR(20), NOT NULL
- customer_email (客户邮箱) - VARCHAR(255)
- total_amount (总金额) - DECIMAL(10,2), NOT NULL
- status (订单状态) - ENUM('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled')
- payment_method (支付方式) - VARCHAR(50)
- payment_status (支付状态) - VARCHAR(50), DEFAULT 'pending'
- notes (备注) - TEXT
- created_at (创建时间) - DATETIME
- updated_at (更新时间) - DATETIME
```

### 7. OrderItem (订单项目表)
```sql
- id (主键)
- order_id (订单ID) - INT, FOREIGN KEY
- product_id (产品ID) - INT, FOREIGN KEY
- product_name (产品名称) - VARCHAR(255), NOT NULL (快照)
- product_price (产品价格) - DECIMAL(10,2), NOT NULL (快照)
- quantity (数量) - INT, NOT NULL
- line_total (小计) - DECIMAL(10,2), NOT NULL
- temperature (温度选择) - ENUM('cold', 'hot', 'normal'), DEFAULT 'normal'
- ingredients (配料) - JSON (存储选择的配料)
- created_at (创建时间) - DATETIME
```

### 8. Cart (购物车表)
```sql
- id (主键)
- user_id (用户ID) - INT, FOREIGN KEY, NULLABLE (支持游客)
- session_id (会话ID) - VARCHAR(255), NULLABLE (游客购物车)
- created_at (创建时间) - DATETIME
- updated_at (更新时间) - DATETIME
```

### 9. CartItem (购物车项目表)
```sql
- id (主键)
- cart_id (购物车ID) - INT, FOREIGN KEY
- product_id (产品ID) - INT, FOREIGN KEY
- quantity (数量) - INT, NOT NULL
- temperature (温度选择) - ENUM('cold', 'hot', 'normal'), DEFAULT 'normal'
- ingredients (配料) - JSON (存储选择的配料)
- created_at (创建时间) - DATETIME
```

## 项目结构

```
quick-orders/
├── app.py                 # 主应用文件
├── config.py             # 配置文件
├── requirements.txt      # Python 依赖
├── setup_database.py     # 数据库设置脚本
├── models/               # 数据库模型
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   ├── product_image.py
│   ├── product_ingredient.py
│   ├── store.py
│   ├── order.py
│   ├── order_item.py
│   ├── cart.py
│   └── cart_item.py
├── routes/               # URL 路由
│   ├── __init__.py
│   ├── frontend.py
│   ├── admin.py
│   └── api.py
├── templates/            # HTML 模板
│   ├── base.html
│   ├── frontend/
│   │   ├── index.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── login.html
│   │   └── register.html
│   └── admin/
│       ├── dashboard.html
│       ├── products.html
│       ├── orders.html
│       └── stores.html
├── static/               # 静态资源
│   ├── css/
│   ├── js/
│   └── images/
├── utils/                # 工具函数
│   ├── __init__.py
│   ├── image_utils.py
│   └── helpers.py
└── migrations/           # 数据库迁移
    ├── env.py
    ├── script.py.mako
    └── alembic.ini
```

## 功能规划

### 前端功能
1. **产品展示**
   - 产品列表页面
   - 产品详情页面（支持冷热饮选择、配料选择）
   - 产品图片轮播

2. **购物车功能**
   - 添加到购物车
   - 购物车管理（修改数量、删除项目）
   - 价格计算（基础价格 + 配料价格 + 冷热饮差价）

3. **用户系统**
   - 用户注册/登录
   - 用户资料管理
   - 订单历史

4. **订单流程**
   - 购物车结算
   - 订单确认
   - 订单状态跟踪

### 后端功能 (Admin)
1. **产品管理**
   - 产品 CRUD 操作
   - 产品图片管理
   - 配料管理
   - 价格管理（基础价格、特殊价格、冷热饮价格）

2. **订单管理**
   - 订单列表
   - 订单状态更新
   - 订单详情查看

3. **店铺管理**
   - 店铺信息管理
   - 营业时间设置

4. **用户管理**
   - 用户列表
   - 用户状态管理

## API 端点规划

### 前端 API
- `GET /api/products` - 获取产品列表
- `GET /api/products/<id>` - 获取产品详情
- `POST /api/cart/add` - 添加到购物车
- `POST /api/cart/update` - 更新购物车
- `POST /api/cart/remove` - 从购物车移除
- `GET /api/cart` - 获取购物车内容
- `POST /api/orders` - 创建订单
- `GET /api/orders/<id>` - 获取订单详情

### 管理 API
- `GET /admin/products` - 产品管理页面
- `POST /admin/products` - 创建产品
- `PUT /admin/products/<id>` - 更新产品
- `DELETE /admin/products/<id>` - 删除产品
- `GET /admin/orders` - 订单管理页面
- `PUT /admin/orders/<id>/status` - 更新订单状态

## 开发阶段

### 阶段 1: 基础架构搭建
1. 创建项目结构
2. 配置数据库连接
3. 创建基础模型
4. 设置 Flask 应用

### 阶段 2: 核心功能开发
1. 用户认证系统
2. 产品管理功能
3. 购物车功能
4. 订单系统

### 阶段 3: 前端界面开发
1. 产品展示页面
2. 购物车页面
3. 订单页面
4. 管理后台

### 阶段 4: 测试与优化
1. 功能测试
2. 性能优化
3. 用户体验优化

## 特色功能

1. **多价格体系**: 支持基础价格、特殊价格、冷热饮不同价格
2. **配料系统**: 产品可添加配料，每个配料有独立价格
3. **温度选择**: 支持冷饮、热饮、常温选择
4. **游客购物车**: 支持未登录用户使用购物车
5. **订单状态跟踪**: 完整的订单状态管理流程
6. **店铺信息**: 支持多店铺信息管理

## 部署配置

### 环境变量
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:@localhost/quick-orders
FLASK_ENV=development
```

### 数据库初始化
1. 创建 MySQL 数据库 `quick-orders`
2. 运行数据库迁移
3. 创建默认管理员账户

## 开发时间估算

- **阶段 1**: 2-3 天
- **阶段 2**: 5-7 天
- **阶段 3**: 4-5 天
- **阶段 4**: 2-3 天

**总计**: 13-18 天

## 技术难点与解决方案

1. **多价格计算**: 在 OrderItem 中存储价格快照，避免价格变更影响历史订单
2. **配料系统**: 使用 JSON 字段存储选择的配料信息
3. **游客购物车**: 使用 session_id 管理游客购物车
4. **订单状态管理**: 实现状态机模式管理订单状态流转

这个规划书为 Quick Orders 系统提供了完整的开发指导，接下来将按照这个规划书逐步实现系统功能。
