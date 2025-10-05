#!/usr/bin/env python3
"""
Database Test Script for Quick Orders Flask Application
"""

from application import create_app
from database import db
from models import Product, Store, User

def test_database():
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    
    # 创建应用上下文
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection
            print("Testing database connection...")
            
            # Get table count
            table_count = len(db.metadata.tables)
            print(f"Database tables: {table_count}")
            
            # Test queries
            products = Product.query.count()
            stores = Store.query.count()
            users = User.query.count()
            
            print(f"Products: {products}")
            print(f"Stores: {stores}")
            print(f"Users: {users}")
            
            # Get first few products
            print("\nFirst 3 products:")
            for product in Product.query.limit(3).all():
                print(f"  - {product.name} (ID: {product.id})")
            
            print("\n[OK] Database connection test successful!")
            
        except Exception as e:
            print(f"[FAILED] Database connection test failed: {e}")
            return False
    
    return True

if __name__ == '__main__':
    test_database()
