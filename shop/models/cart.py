from datetime import datetime
from database import db
import json

class Cart(db.Model):
    """購物車模型"""
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 支持遊客
    session_id = db.Column(db.String(255), nullable=True)  # 遊客會話ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    cart_items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_total_items(self):
        """獲取購物車總項目數"""
        return sum(item.quantity for item in self.cart_items)
    
    def get_total_amount(self):
        """獲取購物車總金額"""
        total = 0
        for item in self.cart_items:
            # 基礎價格
            base_price = item.product.get_price(item.temperature)
            total += base_price * item.quantity
            
            # 添加配料價格
            if item.ingredients:
                for ingredient in item.ingredients:
                    if isinstance(ingredient, dict):
                        # 如果ingredient是字典，直接獲取price
                        ingredient_price = float(ingredient.get('price', 0))
                    else:
                        # 如果ingredient是ID，從product的ingredients中查找
                        ingredient_id = ingredient
                        ingredient_obj = None
                        for prod_ingredient in item.product.ingredients:
                            if prod_ingredient.id == ingredient_id:
                                ingredient_obj = prod_ingredient
                                break
                        ingredient_price = float(ingredient_obj.price) if ingredient_obj else 0
                    
                    total += ingredient_price * item.quantity
        return total
    
    @property
    def total_items(self):
        """購物車總項目數（屬性形式）"""
        return self.get_total_items()
    
    @property
    def total_amount(self):
        """購物車總金額（屬性形式）"""
        return self.get_total_amount()
    
    def clear(self):
        """清空購物車"""
        for item in self.cart_items:
            db.session.delete(item)
        db.session.commit()
    
    def __repr__(self):
        return f'<Cart {self.id}>'

class CartItem(db.Model):
    """購物車項目模型"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Enum('cold', 'hot', 'normal'), default='normal')
    ingredients = db.Column(db.JSON)  # 存儲選擇的配料信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_total_price(self):
        """獲取項目總價格"""
        # 基礎價格
        base_price = self.product.get_price(self.temperature)
        total = base_price * self.quantity
        
        # 添加配料價格
        if self.ingredients:
            for ingredient in self.ingredients:
                if isinstance(ingredient, dict):
                    # 如果ingredient是字典，直接獲取price
                    ingredient_price = float(ingredient.get('price', 0))
                else:
                    # 如果ingredient是ID，從product的ingredients中查找
                    ingredient_id = ingredient
                    ingredient_obj = None
                    for prod_ingredient in self.product.ingredients:
                        if prod_ingredient.id == ingredient_id:
                            ingredient_obj = prod_ingredient
                            break
                    ingredient_price = float(ingredient_obj.price) if ingredient_obj else 0
                
                total += ingredient_price * self.quantity
        
        return total
    
    @property
    def line_total(self):
        """項目總價格（屬性形式）"""
        return self.get_total_price()
    
    @property
    def unit_price(self):
        """單價（含配料）"""
        base_price = self.product.get_price(self.temperature)
        ingredient_price = 0
        if self.ingredients:
            for ingredient in self.ingredients:
                if isinstance(ingredient, dict):
                    # 如果ingredient是字典，直接獲取price
                    ingredient_price += float(ingredient.get('price', 0))
                else:
                    # 如果ingredient是ID，從product的ingredients中查找
                    ingredient_id = ingredient
                    ingredient_obj = None
                    for prod_ingredient in self.product.ingredients:
                        if prod_ingredient.id == ingredient_id:
                            ingredient_obj = prod_ingredient
                            break
                    if ingredient_obj:
                        ingredient_price += float(ingredient_obj.price)
        return base_price + ingredient_price
    
    def set_ingredients(self, ingredients_list):
        """設置配料"""
        self.ingredients = ingredients_list
    
    def __repr__(self):
        return f'<CartItem {self.product.name} x{self.quantity}>'
