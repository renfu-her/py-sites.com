from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from database import db
from models import Product, ProductImage, Cart, CartItem, Order, OrderItem, User

api_bp = Blueprint('api', __name__)

@api_bp.route('/products')
def get_products():
    """獲取產品列表"""
    from sqlalchemy.orm import joinedload
    products = Product.query.options(
        joinedload(Product.images)
    ).filter_by(is_active=True).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': float(p.price),
        'special_price': float(p.special_price),
        'cold_price': float(p.cold_price),
        'hot_price': float(p.hot_price),
        'description': p.description,
        'images': [img.image for img in p.images if img.is_active]
    } for p in products])

@api_bp.route('/products/<int:product_id>')
def get_product(product_id):
    """獲取產品詳情"""
    from sqlalchemy.orm import joinedload
    product = Product.query.options(
        joinedload(Product.images),
        joinedload(Product.ingredients)
    ).filter_by(id=product_id, is_active=True).first_or_404()
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        'special_price': float(product.special_price),
        'cold_price': float(product.cold_price),
        'hot_price': float(product.hot_price),
        'description': product.description,
        'images': [img.image for img in product.images if img.is_active],
        'ingredients': [{
            'id': ing.id,
            'name': ing.name,
            'price': float(ing.price)
        } for ing in product.ingredients if ing.is_active]
    })

@api_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """添加到購物車"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    temperature = data.get('temperature', 'normal')
    ingredients = data.get('ingredients', [])
    
    product = Product.query.get_or_404(product_id)
    cart = get_or_create_cart()
    
        # 檢查是否已存在相同配置的商品
    existing_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id,
        temperature=temperature
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
        existing_item.set_ingredients(ingredients)
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            temperature=temperature
        )
        cart_item.set_ingredients(ingredients)
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': '已添加到購物車'})

@api_bp.route('/cart/update', methods=['POST'])
def update_cart_item():
    """更新購物車項目"""
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity')
    
    cart_item = CartItem.query.get_or_404(item_id)
    cart_item.quantity = quantity
    
    if quantity <= 0:
        db.session.delete(cart_item)
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': '購物車已更新'})

@api_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    """從購物車移除"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    cart_item = CartItem.query.get_or_404(item_id)
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': '已從購物車移除'})

@api_bp.route('/cart')
def get_cart():
    """獲取購物車內容"""
    cart = get_or_create_cart()
    items = []
    
    for item in cart.cart_items:
        items.append({
            'id': item.id,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': item.product.get_price(item.temperature)
            },
            'quantity': item.quantity,
            'temperature': item.temperature,
            'ingredients': item.ingredients or [],
            'total_price': item.get_total_price()
        })
    
    return jsonify({
        'items': items,
        'total_items': cart.get_total_items(),
        'total_amount': cart.get_total_amount()
    })

@api_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    """創建訂單"""
    data = request.get_json()
    cart = get_or_create_cart()
    
    if cart.cart_items.count() == 0:
        return jsonify({'error': '購物車為空'}), 400
    
    # 創建訂單
    order = Order(
        user_id=current_user.id,
        customer_name=data.get('customer_name'),
        customer_phone=data.get('customer_phone'),
        customer_email=data.get('customer_email'),
        payment_method=data.get('payment_method', 'cash'),
        notes=data.get('notes', '')
    )
    
    db.session.add(order)
    db.session.flush()  # 獲取訂單ID
    
    # 創建訂單項目
    total_amount = 0
    for cart_item in cart.cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            product_price=cart_item.product.get_price(cart_item.temperature),
            quantity=cart_item.quantity,
            temperature=cart_item.temperature,
            ingredients=cart_item.ingredients
        )
        order_item.calculate_line_total()
        total_amount += float(order_item.line_total)
        
        db.session.add(order_item)
    
    order.total_amount = total_amount
    db.session.commit()
    
    # 清空購物車
    cart.clear()
    
    return jsonify({'success': True, 'order_id': order.id, 'order_number': order.order_number})

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

# 管理員 API
@api_bp.route('/admin/products/images/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_product_image(image_id):
    """刪除商品圖片"""
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': '無權限'}), 403
    
    from models import ProductImage
    from utils.image_utils import delete_product_image as delete_img
    
    image = ProductImage.query.get_or_404(image_id)
    image_path = image.image
    
    db.session.delete(image)
    db.session.commit()
    
    # 刪除實體文件
    delete_img(image_path)
    
    return jsonify({'status': 'success', 'message': '圖片已刪除'})

@api_bp.route('/admin/stores/images/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_store_image(image_id):
    """刪除店鋪圖片"""
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': '無權限'}), 403
    
    from models import StoreImage
    from utils.image_utils import delete_store_image as delete_img
    
    image = StoreImage.query.get_or_404(image_id)
    image_path = image.image
    
    db.session.delete(image)
    db.session.commit()
    
    # 刪除實體文件
    delete_img(image_path)
    
    return jsonify({'status': 'success', 'message': 'Banner 圖片已刪除'})

@api_bp.route('/admin/products/<int:product_id>/toggle-status', methods=['POST'])
@login_required
def toggle_product_status(product_id):
    """切換商品狀態"""
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': '無權限'}), 403
    
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    
    return jsonify({'status': 'success', 'is_active': product.is_active})

@api_bp.route('/admin/stores/<int:store_id>/toggle-status', methods=['POST'])
@login_required
def toggle_store_status(store_id):
    """切換店鋪狀態"""
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': '無權限'}), 403
    
    from models import Store
    store = Store.query.get_or_404(store_id)
    store.is_active = not store.is_active
    db.session.commit()
    
    return jsonify({'status': 'success', 'is_active': store.is_active})

@api_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """切換用戶狀態"""
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': '無權限'}), 403
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({'status': 'success', 'is_active': user.is_active})

@api_bp.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@login_required
def update_order_status(order_id):
    """更新訂單狀態"""
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': '無權限'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()
    
    return jsonify({'status': 'success', 'order_status': order.status})