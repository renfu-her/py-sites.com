from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user, login_user, logout_user
from database import db
from models import User, Product, Cart, CartItem, Order, OrderItem, Store

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    """首頁"""
    from sqlalchemy.orm import joinedload

    stores = Store.query.options(
        joinedload(Store.products).joinedload(Product.images),
        joinedload(Store.images)
    ).filter_by(is_active=True).order_by(Store.name).all()

    return render_template('frontend/index.html', stores=stores)


@frontend_bp.route('/store/<int:store_id>')
def store_detail(store_id):
    """門市詳情"""
    from sqlalchemy.orm import joinedload

    store = Store.query.options(
        joinedload(Store.images),
        joinedload(Store.products).joinedload(Product.images)
    ).filter_by(id=store_id, is_active=True).first_or_404()

    return render_template('frontend/store_detail.html', store=store)

@frontend_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """產品詳情頁"""
    from sqlalchemy.orm import joinedload
    product = Product.query.options(
        joinedload(Product.images),
        joinedload(Product.ingredients)
    ).filter_by(id=product_id, is_active=True).first_or_404()
    return render_template('frontend/product_detail.html', product=product)

@frontend_bp.route('/cart')
def cart():
    """購物車頁面"""
    cart = get_or_create_cart()
    return render_template('frontend/cart.html', cart=cart)

@frontend_bp.route('/checkout')
@login_required
def checkout():
    """結算頁面"""
    cart = get_or_create_cart()
    if cart.cart_items.count() == 0:
        flash('購物車為空', 'warning')
        return redirect(url_for('frontend.cart'))
    return render_template('frontend/checkout.html', cart=cart)

@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用戶登錄"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('frontend.index'))
        else:
            flash('郵箱或密碼錯誤', 'error')
    
    return render_template('frontend/login.html')

@frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用戶註冊"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        # 檢查郵箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('郵箱已存在', 'error')
            return render_template('frontend/register.html')
        
        # 創建新用戶
        user = User(name=name, email=email, phone=phone)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('註冊成功，請登錄', 'success')
        return redirect(url_for('frontend.login'))
    
    return render_template('frontend/register.html')

@frontend_bp.route('/logout')
@login_required
def logout():
    """用戶登出"""
    logout_user()
    flash('已成功登出', 'info')
    return redirect(url_for('frontend.index'))

@frontend_bp.route('/orders')
@login_required
def orders():
    """訂單列表"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('frontend/orders.html', orders=orders)

@frontend_bp.route('/create-order', methods=['POST'])
def create_order():
    """創建訂單"""
    try:
        cart = get_or_create_cart()
        if cart.cart_items.count() == 0:
            return jsonify({'status': 'error', 'message': '購物車為空'}), 400
        
        # 獲取表單數據
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        customer_email = request.form.get('customer_email')
        payment_method = request.form.get('payment_method')
        notes = request.form.get('notes')
        delivery_address = request.form.get('delivery_address')
        
        if not customer_name or not customer_phone:
            return jsonify({'status': 'error', 'message': '請填寫姓名和手機號'}), 400
        
        # 如果用戶已登入，更新用戶資料
        if current_user.is_authenticated:
            if customer_phone:
                current_user.phone = customer_phone
            if delivery_address:
                current_user.address = delivery_address
        
        # 創建訂單
        order = Order(
            user_id=current_user.id if current_user.is_authenticated else None,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            payment_method=payment_method,
            notes=notes,
            total_amount=cart.total_amount
        )
        
        db.session.add(order)
        db.session.flush()  # 獲取訂單ID
        
        # 創建訂單項
        for cart_item in cart.cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                product_name=cart_item.product.name,
                product_price=cart_item.unit_price,
                quantity=cart_item.quantity,
                temperature=cart_item.temperature,
                line_total=cart_item.line_total
            )
            db.session.add(order_item)
        
        # 清空購物車
        cart.cart_items.delete()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '訂單創建成功',
            'redirect_url': url_for('frontend.orders')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': '訂單創建失敗: ' + str(e)}), 500

def get_or_create_cart():
    """獲取或創建購物車"""
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
    else:
        # 遊客購物車
        session_id = session.get('session_id')
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        cart = Cart.query.filter_by(session_id=session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            db.session.add(cart)
            db.session.commit()
    
    return cart
