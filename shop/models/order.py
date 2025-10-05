from datetime import datetime
from decimal import Decimal
from database import db
import json
import uuid

class Order(db.Model):
    """訂單模型"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 支持遊客訂單
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(255))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled'), 
                      default='pending')
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        if not self.order_number:
            self.order_number = self.generate_order_number()
    
    def generate_order_number(self):
        """生成訂單號"""
        return f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    def calculate_total(self):
        """計算訂單總金額"""
        total = Decimal('0')
        for item in self.order_items:
            total += Decimal(str(item.line_total))
        self.total_amount = total
        return total
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    """訂單項目模型"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)  # 產品名稱快照
    product_price = db.Column(db.Numeric(10, 2), nullable=False)  # 產品價格快照
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)
    temperature = db.Column(db.Enum('cold', 'hot', 'normal'), default='normal')
    ingredients = db.Column(db.JSON)  # 存儲選擇的配料信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_line_total(self):
        """計算小計"""
        # 基礎價格
        base_total = Decimal(str(self.product_price)) * self.quantity
        
        # 添加配料價格
        if self.ingredients:
            for ingredient in self.ingredients:
                ingredient_price = Decimal(str(ingredient.get('price', 0)))
                base_total += ingredient_price * self.quantity
        
        self.line_total = base_total
        return base_total
    
    def set_ingredients(self, ingredients_list):
        """設置配料"""
        self.ingredients = ingredients_list
        self.calculate_line_total()
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'
