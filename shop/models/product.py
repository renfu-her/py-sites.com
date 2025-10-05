from datetime import datetime
from decimal import Decimal
from database import db

class Product(db.Model):
    """產品模型"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    special_price = db.Column(db.Numeric(10, 2), default=0)
    cold_price = db.Column(db.Numeric(10, 2), default=0)
    hot_price = db.Column(db.Numeric(10, 2), default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    images = db.relationship('ProductImage', backref='product', lazy='select', cascade='all, delete-orphan')
    ingredients = db.relationship('ProductIngredient', backref='product', lazy='select', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    # stores relationship 在 Store 模型中定義
    
    def get_price(self, temperature='normal'):
        """根據溫度獲取價格"""
        if temperature == 'cold' and self.cold_price > 0:
            return float(self.cold_price)
        elif temperature == 'hot' and self.hot_price > 0:
            return float(self.hot_price)
        elif self.special_price > 0:
            return float(self.special_price)
        else:
            return float(self.price)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class ProductImage(db.Model):
    """產品圖片模型"""
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    sort = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductImage {self.image}>'

class ProductIngredient(db.Model):
    """產品配料模型"""
    __tablename__ = 'product_ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductIngredient {self.name}>'
