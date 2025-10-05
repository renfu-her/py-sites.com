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

### 3. ProductImage (Product Image Table)
```sql
- id (Primary Key)
- product_id (Product ID) - INT, FOREIGN KEY
- image (Image Path) - VARCHAR(500), NOT NULL
- sort (Sort Order) - INT, DEFAULT 0
- is_active (Is Active) - BOOLEAN, DEFAULT TRUE
- created_at (Created At) - DATETIME
```

### 4. ProductIngredient (Product Ingredient Table)
```sql
- id (Primary Key)
- product_id (Product ID) - INT, FOREIGN KEY
- name (Ingredient Name) - VARCHAR(255), NOT NULL
- price (Ingredient Price) - DECIMAL(10,2), DEFAULT 0
- is_active (Is Active) - BOOLEAN, DEFAULT TRUE
- created_at (Created At) - DATETIME
```

### 5. Store (Store Table)
```sql
- id (Primary Key)
- product_id (Product ID) - INT, FOREIGN KEY
- name (Store Name) - VARCHAR(255), NOT NULL
- description (Store Description) - TEXT
- work_time (Working Hours) - VARCHAR(100)
- address (Store Address) - TEXT
- phone (Store Phone) - VARCHAR(20)
- is_active (Is Active) - BOOLEAN, DEFAULT TRUE
- created_at (Created At) - DATETIME
- updated_at (Updated At) - DATETIME
```

### 6. Order (Order Table)
```sql
- id (Primary Key)
- user_id (User ID) - INT, FOREIGN KEY, NULLABLE (supports guest orders)
- order_number (Order Number) - VARCHAR(50), UNIQUE, NOT NULL
- customer_name (Customer Name) - VARCHAR(255), NOT NULL
- customer_phone (Customer Phone) - VARCHAR(20), NOT NULL
- customer_email (Customer Email) - VARCHAR(255)
- total_amount (Total Amount) - DECIMAL(10,2), NOT NULL
- status (Order Status) - ENUM('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled')
- payment_method (Payment Method) - VARCHAR(50)
- payment_status (Payment Status) - VARCHAR(50), DEFAULT 'pending'
- notes (Notes) - TEXT
- created_at (Created At) - DATETIME
- updated_at (Updated At) - DATETIME
```

### 7. OrderItem (Order Item Table)
```sql
- id (Primary Key)
- order_id (Order ID) - INT, FOREIGN KEY
- product_id (Product ID) - INT, FOREIGN KEY
- product_name (Product Name) - VARCHAR(255), NOT NULL (snapshot)
- product_price (Product Price) - DECIMAL(10,2), NOT NULL (snapshot)
- quantity (Quantity) - INT, NOT NULL
- line_total (Line Total) - DECIMAL(10,2), NOT NULL
- temperature (Temperature Choice) - ENUM('cold', 'hot', 'normal'), DEFAULT 'normal'
- ingredients (Ingredients) - JSON (stores selected ingredients)
- created_at (Created At) - DATETIME
```

### 8. Cart (Shopping Cart Table)
```sql
- id (Primary Key)
- user_id (User ID) - INT, FOREIGN KEY, NULLABLE (supports guests)
- session_id (Session ID) - VARCHAR(255), NULLABLE (guest cart)
- created_at (Created At) - DATETIME
- updated_at (Updated At) - DATETIME
```

### 9. CartItem (Cart Item Table)
```sql
- id (Primary Key)
- cart_id (Cart ID) - INT, FOREIGN KEY
- product_id (Product ID) - INT, FOREIGN KEY
- quantity (Quantity) - INT, NOT NULL
- temperature (Temperature Choice) - ENUM('cold', 'hot', 'normal'), DEFAULT 'normal'
- ingredients (Ingredients) - JSON (stores selected ingredients)
- created_at (Created At) - DATETIME
```

## Project Structure

```
quick-orders/
├── app.py                 # Main application file
├── config.py             # Configuration file
├── database.py           # Database connection
├── requirements.txt      # Python dependencies
├── setup_database.py     # Database setup script
├── run.py               # Startup script
├── models/              # Data models
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
├── routes/              # URL routes
│   ├── __init__.py
│   ├── frontend.py
│   ├── admin.py
│   └── api.py
├── templates/           # HTML templates
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
├── static/              # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── image_utils.py
│   └── helpers.py
└── migrations/          # Database migrations
    ├── env.py
    ├── script.py.mako
    └── alembic.ini
```

## Feature Planning

### Frontend Features
1. **Product Display**
   - Product list page
   - Product detail page (supports hot/cold selection, ingredient selection)
   - Product image carousel

2. **Shopping Cart Features**
   - Add to cart
   - Cart management (modify quantities, remove items)
   - Price calculation (base price + ingredient price + hot/cold price difference)

3. **User System**
   - User registration/login
   - User profile management
   - Order history

4. **Order Process**
   - Cart checkout
   - Order confirmation
   - Order status tracking

### Backend Features (Admin)
1. **Product Management**
   - Product CRUD operations
   - Product image management
   - Ingredient management
   - Price management (base price, special price, hot/cold price)

2. **Order Management**
   - Order list
   - Order status updates
   - Order detail viewing

3. **Store Management**
   - Store information management
   - Working hours setup

4. **User Management**
   - User list
   - User status management

## API Endpoint Planning

### Frontend API
- `GET /api/products` - Get product list
- `GET /api/products/<id>` - Get product details
- `POST /api/cart/add` - Add to cart
- `POST /api/cart/update` - Update cart
- `POST /api/cart/remove` - Remove from cart
- `GET /api/cart` - Get cart contents
- `POST /api/orders` - Create order
- `GET /api/orders/<id>` - Get order details

### Admin API
- `GET /admin/products` - Product management page
- `POST /admin/products` - Create product
- `PUT /admin/products/<id>` - Update product
- `DELETE /admin/products/<id>` - Delete product
- `GET /admin/orders` - Order management page
- `PUT /admin/orders/<id>/status` - Update order status

## Development Phases

### Phase 1: Basic Architecture Setup
1. Create project structure
2. Configure database connection
3. Create basic models
4. Setup Flask application

### Phase 2: Core Feature Development
1. User authentication system
2. Product management features
3. Shopping cart features
4. Order system

### Phase 3: Frontend Interface Development
1. Product display pages
2. Shopping cart page
3. Order page
4. Admin panel

### Phase 4: Testing and Optimization
1. Feature testing
2. Performance optimization
3. User experience optimization

## Special Features

1. **Multi-Price System**: Support for base price, special price, different prices for hot/cold drinks
2. **Ingredient System**: Products can have ingredients with independent pricing
3. **Temperature Selection**: Support for cold, hot, room temperature selection
4. **Guest Cart**: Support for non-logged-in users to use shopping cart
5. **Order Status Tracking**: Complete order status management workflow
6. **Store Information**: Support for multi-store information management

## Deployment Configuration

### Environment Variables
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:@localhost/quick-orders
FLASK_ENV=development
```

### Database Initialization
1. Create MySQL database `quick-orders`
2. Run database migrations
3. Create default administrator account

## Development Time Estimation

- **Phase 1**: 2-3 days
- **Phase 2**: 5-7 days
- **Phase 3**: 4-5 days
- **Phase 4**: 2-3 days

**Total**: 13-18 days

## Technical Challenges and Solutions

1. **Multi-Price Calculation**: Store price snapshots in OrderItem to avoid price changes affecting historical orders
2. **Ingredient System**: Use JSON field to store selected ingredient information
3. **Guest Cart**: Use session_id to manage guest shopping cart
4. **Order Status Management**: Implement state machine pattern to manage order status transitions

This project plan provides complete development guidance for the Quick Orders system, and will be implemented step by step according to this plan.
