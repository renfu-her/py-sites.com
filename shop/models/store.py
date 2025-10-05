from datetime import datetime
from database import db

# Store 和 Product 的多對多關聯表
store_products = db.Table('store_products',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class Store(db.Model):
    """店鋪模型"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    work_time = db.Column(db.String(100))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    images = db.relationship('StoreImage', backref='store', lazy='select', order_by='StoreImage.sort', cascade='all, delete-orphan')
    products = db.relationship('Product', secondary=store_products, backref=db.backref('stores', lazy='dynamic'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Store {self.name}>'


class StoreImage(db.Model):
    """店鋪圖片"""
    __tablename__ = 'store_images'

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, index=True)
    image = db.Column(db.String(500), nullable=False)
    sort = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StoreImage {self.image}>'
