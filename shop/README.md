# Quick Orders - Fast Food Ordering System

A Flask-based fast food ordering system designed specifically for restaurants and beverage shops, supporting multi-price systems, ingredient selection, and order management.

## Features

### 🍽️ Product Management
- **Multi-Price System**: Support for base price, special price, and different prices for hot/cold beverages
- **Ingredient System**: Products can have ingredients with independent pricing
- **Temperature Selection**: Support for cold, hot, and room temperature options
- **Image Management**: Product image upload and display

### 🛒 Shopping Cart Features
- **Guest Cart**: Support for non-logged-in users to use shopping cart
- **Real-time Calculation**: Real-time price calculation (base price + ingredient price)
- **Quantity Management**: Support for modifying quantities and removing items

### 📋 Order System
- **Complete Workflow**: Full workflow from cart to order completion
- **Status Tracking**: Order status management (pending → confirmed → preparing → ready → completed)
- **User System**: Support for user registration, login, and order history

### 👨‍💼 Admin Panel
- **Product Management**: CRUD operations for products
- **Order Management**: Order status updates and detail viewing
- **User Management**: User information management
- **Store Management**: Store information management

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy with Flask-Migrate
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **Image Processing**: Pillow (PIL)

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/Scripts/activate

# Install Python dependencies
pip install -r requirements-simple.txt

# Create MySQL database
mysql -u root -p
CREATE DATABASE `quick-orders`;
```

### 2. Configure Environment

```bash
# Copy environment configuration file
cp env.example .env

# Edit configuration file if needed
# DATABASE_URL=mysql+pymysql://root:password@localhost/quick-orders
```

### 3. Initialize Database

```bash
# Setup database tables and data
python setup_database.py
```

### 4. Start Application

```bash
# Start development server
python app.py
```

### 5. Access System

- **Frontend**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Default Admin**: admin@example.com / admin123

## Database Models

### Core Table Structure

- **users**: User table (customers and administrators)
- **products**: Product table (supports multi-price)
- **product_images**: Product image table
- **product_ingredients**: Product ingredient table
- **stores**: Store information table
- **orders**: Order table
- **order_items**: Order item table
- **carts**: Shopping cart table
- **cart_items**: Shopping cart item table

### Special Features

1. **Multi-Price Support**: Each product supports base price, special price, cold drink price, hot drink price
2. **Ingredient System**: JSON field stores ingredient selection with dynamic price calculation
3. **Guest Cart**: Uses session_id to support non-logged-in user shopping
4. **Order Snapshot**: Order items save product information snapshots to avoid historical orders being affected by product changes

## API Endpoints

### Frontend API

- `GET /api/products` - Get product list
- `GET /api/products/<id>` - Get product details
- `POST /api/cart/add` - Add to cart
- `POST /api/cart/update` - Update cart
- `POST /api/cart/remove` - Remove from cart
- `GET /api/cart` - Get cart contents
- `POST /api/orders` - Create order

### Admin API

- Product management CRUD operations
- Order status management
- User management
- Store management

## Project Structure

```
quick-orders/
├── app.py                 # Main application file
├── config.py             # Configuration file
├── database.py           # Database connection
├── requirements.txt      # Python dependencies
├── setup_database.py     # Database setup script
├── app.py               # Main application entry point
├── models/              # Data models
├── routes/              # Route handlers
├── templates/           # HTML templates
├── static/              # Static assets
├── utils/               # Utility functions
└── migrations/          # Database migrations
```

## Usage Instructions

### Customer Workflow

1. **Browse Products**: View all available products on the homepage
2. **View Details**: Click on products to view detailed information and ingredient options
3. **Add to Cart**: Select temperature and ingredients, then add to cart
4. **Manage Cart**: Modify quantities and remove unwanted items
5. **Checkout**: Login and fill in order information to submit
6. **Track Orders**: View order status in "My Orders"

### Administrator Workflow

1. **Login to Admin Panel**: Use administrator account to login
2. **Product Management**: Add, edit, and delete products
3. **Ingredient Management**: Configure ingredient options for products
4. **Order Management**: View and process orders
5. **Store Management**: Manage store information

## Development Guide

### Adding New Products

1. Create products in admin panel
2. Set base price and special price
3. Add product images
4. Configure ingredient options

### Custom Pricing

- **Base Price**: Default product price
- **Special Price**: Promotional price (higher priority than base price)
- **Cold Drink Price**: Special price for cold drinks
- **Hot Drink Price**: Special price for hot drinks

### Ingredient System

- Each ingredient can have independent pricing
- Supports required and optional ingredients
- Prices automatically accumulate to order total

## Deployment Recommendations

### Production Environment

1. **Database**: Use dedicated MySQL server
2. **Static Files**: Use CDN or Nginx for static file handling
3. **Application Server**: Use Gunicorn + Nginx
4. **Image Storage**: Consider using cloud storage services

### Security Configuration

1. **Environment Variables**: Use strong passwords and keys
2. **Database**: Set appropriate user permissions
3. **HTTPS**: Use HTTPS in production environment
4. **File Upload**: Limit file types and sizes

## Frequently Asked Questions

### Q: How to add new product types?
A: Create new products in the admin panel's product management, set corresponding prices and ingredients.

### Q: How to modify order status?
A: In the admin panel's order management, select the order and update its status.

### Q: What image formats are supported?
A: Supports PNG, JPG, JPEG, GIF, WebP formats, automatically converts to WebP format.

### Q: How to backup data?
A: Use MySQL's mysqldump command to backup the database.

## License

MIT License - See LICENSE file for details

## Support

For questions or suggestions, please submit an Issue or contact the development team.