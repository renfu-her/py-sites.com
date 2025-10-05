from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database import db
from models import User, Product, ProductImage, ProductIngredient, Order, Store, StoreImage

backend_bp = Blueprint('backend', __name__)

@backend_bp.before_request
def require_admin():
    #   ?? ??  ?  ??
    if request.endpoint in ['backend.login', 'backend.logout']:
        return None
    
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('backend.login'))

@backend_bp.route('/')
def dashboard():
    
    #   ?   
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    # ?   ???
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('backend/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders)

@backend_bp.route('/products')
def products():
    
    from sqlalchemy.orm import joinedload
    products = Product.query.options(
        joinedload(Product.images),
        joinedload(Product.ingredients)
    ).all()
    return render_template('backend/products.html', products=products)

@backend_bp.route('/products/create', methods=['GET', 'POST'])
def create_product():
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        special_price = request.form.get('special_price') or 0
        cold_price = request.form.get('cold_price') or 0
        hot_price = request.form.get('hot_price') or 0
        description = request.form.get('description')
        is_active = bool(request.form.get('is_active'))
        
        product = Product(
            name=name,
            price=float(price) if price else 0,
            special_price=float(special_price) if special_price else 0,
            cold_price=float(cold_price) if cold_price else 0,
            hot_price=float(hot_price) if hot_price else 0,
            description=description,
            is_active=is_active
        )
        
        db.session.add(product)
        db.session.commit()
        
        # 處理圖片上傳
        from utils.image_utils import save_product_image
        images = request.files.getlist('images')
        if images:
            for idx, image_file in enumerate(images):
                if image_file and image_file.filename:
                    image_path = save_product_image(image_file, product.id)
                    if image_path:
                        product_image = ProductImage(
                            product_id=product.id,
                            image=image_path,
                            sort=idx,
                            is_active=True
                        )
                        db.session.add(product_image)
            db.session.commit()
        
        flash('商品創建成功', 'success')
        return redirect(url_for('backend.products'))
    
    return render_template('backend/create_product.html')

@backend_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        price = request.form.get('price')
        special_price = request.form.get('special_price') or 0
        cold_price = request.form.get('cold_price') or 0
        hot_price = request.form.get('hot_price') or 0
        
        product.price = float(price) if price else 0
        product.special_price = float(special_price) if special_price else 0
        product.cold_price = float(cold_price) if cold_price else 0
        product.hot_price = float(hot_price) if hot_price else 0
        product.description = request.form.get('description')
        product.is_active = bool(request.form.get('is_active'))
        
        # 處理新上傳的圖片
        from utils.image_utils import save_product_image
        images = request.files.getlist('images')
        if images:
            # 獲取當前最大排序號
            max_sort = db.session.query(db.func.max(ProductImage.sort)).filter_by(product_id=product.id).scalar() or 0
            
            for idx, image_file in enumerate(images):
                if image_file and image_file.filename:
                    image_path = save_product_image(image_file, product.id)
                    if image_path:
                        product_image = ProductImage(
                            product_id=product.id,
                            image=image_path,
                            sort=max_sort + idx + 1,
                            is_active=True
                        )
                        db.session.add(product_image)
        
        db.session.commit()
        
        flash('商品更新成功', 'success')
        return redirect(url_for('backend.products'))
    
    return render_template('backend/edit_product.html', product=product)

@backend_bp.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    
    flash('Operation completed', 'success')
    return redirect(url_for('backend.products'))

@backend_bp.route('/orders')
def orders():
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('backend/orders.html', orders=orders)

@backend_bp.route('/orders/<int:order_id>')
def order_detail(order_id):
    
    order = Order.query.get_or_404(order_id)
    return render_template('backend/order_detail.html', order=order)

@backend_bp.route('/orders/<int:order_id>/status', methods=['POST'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Operation completed', 'success')
    else:
        flash('Operation failed', 'error')
    
    return redirect(url_for('backend.order_detail', order_id=order_id))

@backend_bp.route('/users')
def users():
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('backend/users.html', users=users)


@backend_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        is_admin = bool(request.form.get('is_admin'))
        is_active = bool(request.form.get('is_active'))

        if not name or not email or not password:
            flash('Operation failed', 'error')
            return render_template('backend/create_user.html', form_data=request.form)

        if User.query.filter_by(email=email).first():
            flash('Operation failed', 'error')
            return render_template('backend/create_user.html', form_data=request.form)

        user = User(
            name=name,
            email=email,
            phone=phone,
            is_admin=is_admin,
            is_active=is_active
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Operation completed', 'success')
        return redirect(url_for('backend.users'))

    return render_template('backend/create_user.html', form_data=None)


@backend_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Operation failed', 'error')
        return redirect(url_for('backend.users'))

    if user.is_admin:
        flash('Operation failed', 'error')
        return redirect(url_for('backend.users'))

    db.session.delete(user)
    db.session.commit()

    flash('Operation completed', 'success')
    return redirect(url_for('backend.users'))


@backend_bp.route('/stores')
def stores():
    
    from sqlalchemy.orm import joinedload

    stores = Store.query.options(joinedload(Store.products)).all()
    return render_template('backend/stores.html', stores=stores)

@backend_bp.route('/stores/create', methods=['GET', 'POST'])
def create_store():
    
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    selected_product_ids = []

    if request.method == 'POST':
        # 獲取多個選中的產品 ID
        selected_product_ids = request.form.getlist('product_ids')
        
        if not selected_product_ids:
            flash('請至少選擇一個商品', 'error')
            return render_template('backend/create_store.html', products=products, selected_product_ids=selected_product_ids)

        store = Store(
            name=request.form.get('name'),
            description=request.form.get('description'),
            work_time=request.form.get('work_time'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            is_active=bool(request.form.get('is_active'))
        )

        db.session.add(store)
        db.session.flush()  # 獲取 store.id
        
        # 關聯選中的商品
        for product_id in selected_product_ids:
            product = Product.query.get(int(product_id))
            if product:
                store.products.append(product)
        
        # 處理店鋪圖片上傳
        from utils.image_utils import save_store_image
        images = request.files.getlist('images')
        if images:
            for idx, image_file in enumerate(images):
                if image_file and image_file.filename:
                    image_path = save_store_image(image_file, store.id)
                    if image_path:
                        store_image = StoreImage(
                            store_id=store.id,
                            image=image_path,
                            sort=idx,
                            is_active=True
                        )
                        db.session.add(store_image)
        
        db.session.commit()

        flash('店鋪創建成功', 'success')
        return redirect(url_for('backend.stores'))

    return render_template('backend/create_store.html', products=products, selected_product_ids=selected_product_ids)


@backend_bp.route('/stores/<int:store_id>/edit', methods=['GET', 'POST'])
def edit_store(store_id):
    
    store = Store.query.get_or_404(store_id)
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()

    # 獲取當前店鋪已關聯的商品 ID 列表
    selected_product_ids = [str(p.id) for p in store.products]

    if request.method == 'POST':
        # 獲取新選擇的商品 ID 列表
        new_product_ids = request.form.getlist('product_ids')
        
        if not new_product_ids:
            flash('請至少選擇一個商品', 'error')
            return render_template('backend/edit_store.html', store=store, products=products, selected_product_ids=selected_product_ids)

        # 更新店鋪基本信息
        store.name = request.form.get('name')
        store.description = request.form.get('description')
        store.work_time = request.form.get('work_time')
        store.address = request.form.get('address')
        store.phone = request.form.get('phone')
        store.is_active = bool(request.form.get('is_active'))

        # 更新商品關聯
        store.products = []  # 清空現有關聯
        for product_id in new_product_ids:
            product = Product.query.get(int(product_id))
            if product:
                store.products.append(product)

        # 處理新上傳的店鋪圖片
        from utils.image_utils import save_store_image
        images = request.files.getlist('images')
        if images:
            # 獲取當前最大排序號
            max_sort = db.session.query(db.func.max(StoreImage.sort)).filter_by(store_id=store.id).scalar() or 0
            
            for idx, image_file in enumerate(images):
                if image_file and image_file.filename:
                    image_path = save_store_image(image_file, store.id)
                    if image_path:
                        store_image = StoreImage(
                            store_id=store.id,
                            image=image_path,
                            sort=max_sort + idx + 1,
                            is_active=True
                        )
                        db.session.add(store_image)

        db.session.commit()

        flash('店鋪更新成功', 'success')
        return redirect(url_for('backend.stores'))

    return render_template('backend/edit_store.html', store=store, products=products, selected_product_ids=selected_product_ids)


@backend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        #    ?  ?  ?  ?  
        if email == 'admin@admin.com':
            # ?  ?     ?  ?  
            admin_user = User.query.filter_by(email='admin@admin.com').first()
            if not admin_user:
                # ?    ?  ??  ??
                admin_user = User(
                    name='Administrator',
                    email='admin@admin.com',
                    is_admin=True,
                    is_active=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
            
            if admin_user.check_password(password) and admin_user.is_admin:
                from flask_login import login_user
                login_user(admin_user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('backend.dashboard'))
            else:
                flash('Operation failed', 'error')
        else:
            flash('Operation failed', 'error')
    
    return render_template('backend/login.html')

@backend_bp.route('/logout')
def logout():
    from flask_login import logout_user
    logout_user()
    flash('Information', 'info')
    return redirect(url_for('backend.login'))






