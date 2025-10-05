# Quick Orders - Quick Start Guide

## 🚀 5-Minute Quick Start

### Step 1: Environment Setup

Ensure you have installed:
- Python 3.8+
- MySQL 8.0+

### Step 2: Create Database

```sql
-- Login to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE `quick-orders`;

-- Exit MySQL
exit;
```

Or run directly:
```bash
mysql -u root -p < create_database.sql
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Windows users (recommended)
install.bat

# Or manually install simplified dependencies
pip install -r requirements-simple.txt
```

### Step 5: Initialize System

```bash
python setup_database.py
```

### Step 6: Start Application

```bash
python run.py
```

## 🎯 Access System

- **Frontend**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Admin Account**: admin@example.com / admin123

## 📱 Feature Demo

### Customer Features
1. Browse product list
2. View product details
3. Add to cart
4. Register/Login
5. Submit orders

### Admin Features
1. Login to admin panel
2. Manage products
3. Process orders
4. Manage users

## 🔧 Common Issues

### Q: Database connection failed
A: Ensure MySQL service is running and credentials are correct

### Q: Dependency installation failed
A: Check Python version and use virtual environment

### Q: Port is occupied
A: Modify port number in run.py

## 📞 Technical Support

If you encounter problems, please check:
1. Python version >= 3.8
2. MySQL service is running normally
3. Database quick-orders has been created
4. All dependencies are properly installed

## 🎉 Start Using

After system startup, you can:
1. Add products in admin panel
2. Configure ingredients and pricing
3. Customers start ordering
4. Manage order status

Enjoy using! 🍽️
