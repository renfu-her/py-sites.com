# Quick Orders - Installation Guide

## 🚀 Quick Installation

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Git (optional)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd quick-order
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/Scripts/activate
```

### Step 3: Install Dependencies

```bash
# Install simplified dependencies (Windows compatible)
pip install -r requirements-simple.txt
```

### Step 4: Create Database

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE `quick-orders`;
exit;
```

Or run the SQL file:
```bash
mysql -u root -p < create_database.sql
```

### Step 5: Configure Environment

```bash
# Copy environment configuration
cp env.example .env

# Edit .env file if needed
# DATABASE_URL=mysql+pymysql://root:password@localhost/quick-orders
```

### Step 6: Initialize Database

```bash
python setup_database.py
```

### Step 7: Start Application

```bash
python app.py
```

## 🎯 Access System

- **Frontend**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Default Admin**: admin@example.com / admin123

## 🔧 Windows Quick Install

For Windows users, you can use the automated installer:

```bash
# Run the installer script
install.bat
```

This will automatically:
1. Install Python dependencies
2. Create environment configuration
3. Initialize database with sample data
4. Provide access information

## 📱 System Features

### Customer Features
- Browse product catalog
- View product details with ingredients
- Add items to shopping cart
- User registration and login
- Order submission and tracking

### Admin Features
- Product management (CRUD)
- Ingredient configuration
- Order status management
- User management
- Store information management

## 🛠️ Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```
Error: Can't connect to MySQL server
```
**Solution**: Ensure MySQL service is running and credentials are correct

#### 2. Dependency Installation Failed
```
Error: Failed building wheel for [package]
```
**Solution**: Use `requirements-simple.txt` instead of `requirements.txt`

#### 3. Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port in `app.py` or kill the process using port 5000

#### 4. Permission Denied
```
Error: Permission denied
```
**Solution**: Run as administrator or check file permissions

### Environment Setup

#### MySQL Configuration
```sql
-- Create database
CREATE DATABASE `quick-orders` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional)
CREATE USER 'quickorders'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `quick-orders`.* TO 'quickorders'@'localhost';
FLUSH PRIVILEGES;
```

#### Python Environment
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Upgrade pip if needed
python -m pip install --upgrade pip
```

## 📋 Verification

After installation, verify the setup:

1. **Check Database Connection**
   ```bash
   python -c "from application import create_app; from database import db; app = create_app(); print('Database connected:', db.engine.url)"
   ```

2. **Test Application Startup**
   ```bash
   python app.py
   # Should show "Quick Orders System Starting..."
   ```

3. **Access Web Interface**
   - Open http://localhost:5000
   - Should see product catalog
   - Login to admin panel with default credentials

## 🎉 Next Steps

After successful installation:

1. **Add Products**: Login to admin panel and add your products
2. **Configure Ingredients**: Set up product ingredients and pricing
3. **Customize Store**: Update store information and settings
4. **Test Orders**: Place test orders to verify functionality

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Check system logs for error messages
4. Submit an issue with detailed error information

## 🔄 Updates

To update the system:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements-simple.txt --upgrade

# Run database migrations (if any)
python setup_database.py
```

Enjoy using Quick Orders! 🍽️
