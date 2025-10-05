#!/usr/bin/env python3
"""
Database Setup Script
Create database tables and default data
"""

import os
import sys
from application import create_app
from database import db
from models import User, Product, ProductIngredient

def setup_database():
    """Setup database"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Create default admin user
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = User(
                name='Administrator',
                email='admin@example.com',
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("Created default admin user: admin@example.com / admin123")
        
        # Create sample products
        if Product.query.count() == 0:
            print("Creating sample products...")
            
            # Coffee product
            coffee = Product(
                name='Americano Coffee',
                price=25.00,
                cold_price=27.00,
                hot_price=25.00,
                description='Classic Americano coffee, rich and mellow'
            )
            db.session.add(coffee)
            
            # Coffee ingredients
            coffee_ingredients = [
                ProductIngredient(product=coffee, name='Sugar', price=0),
                ProductIngredient(product=coffee, name='Milk', price=3.00),
                ProductIngredient(product=coffee, name='Oat Milk', price=5.00),
                ProductIngredient(product=coffee, name='Coconut Milk', price=5.00),
                ProductIngredient(product=coffee, name='Vanilla Syrup', price=4.00),
                ProductIngredient(product=coffee, name='Caramel Syrup', price=4.00)
            ]
            
            for ingredient in coffee_ingredients:
                db.session.add(ingredient)
            
            # Tea product
            tea = Product(
                name='Oolong Tea',
                price=20.00,
                cold_price=22.00,
                hot_price=20.00,
                description='Fragrant oolong tea with long-lasting sweetness'
            )
            db.session.add(tea)
            
            # Tea ingredients
            tea_ingredients = [
                ProductIngredient(product=tea, name='Sugar', price=0),
                ProductIngredient(product=tea, name='Lemon', price=2.00),
                ProductIngredient(product=tea, name='Honey', price=3.00),
                ProductIngredient(product=tea, name='Tapioca Pearls', price=4.00)
            ]
            
            for ingredient in tea_ingredients:
                db.session.add(ingredient)
            
            # Dessert product
            dessert = Product(
                name='Cheesecake',
                price=35.00,
                special_price=30.00,
                description='Rich cheesecake that melts in your mouth'
            )
            db.session.add(dessert)
            
            print("Sample products created successfully!")
        
        # Commit all changes
        db.session.commit()
        print("Database setup completed!")
        
        print("\n=== System Information ===")
        print("Admin Account: admin@example.com")
        print("Admin Password: admin123")
        print("Access URL: http://localhost:5000")
        print("Admin Panel: http://localhost:5000/admin")
        print("==========================")

if __name__ == '__main__':
    setup_database()
