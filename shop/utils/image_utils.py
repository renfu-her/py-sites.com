import os
import uuid
from datetime import datetime
from PIL import Image
from flask import current_app

def allowed_file(filename):
    """檢查文件擴展名是否允許"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_and_convert_to_webp(file_path, max_size=(800, 800), quality=85):
    """調整圖片大小並轉換為WebP格式"""
    try:
        # 打開圖片
        with Image.open(file_path) as img:
            # 轉換為RGB模式（如果需要）
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 調整大小
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 生成新的文件名（WebP格式）
            base_name = os.path.splitext(file_path)[0]
            webp_path = f"{base_name}.webp"
            
            # 保存為WebP格式
            img.save(webp_path, 'WebP', quality=quality, optimize=True)
            
            # 刪除原文件
            if file_path != webp_path:
                os.remove(file_path)
            
            return webp_path
    except Exception as e:
        print(f"圖片處理錯誤: {e}")
        return None

def save_product_image(file, product_id):
    """保存商品圖片到 static/uploads/product/{product_id}/ 目錄"""
    if not file or not allowed_file(file.filename):
        return None
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    original_ext = file.filename.rsplit('.', 1)[1].lower()
    temp_filename = f"{timestamp}_{unique_id}.{original_ext}"
    
    # 創建上傳目錄 static/uploads/product/{product_id}/
    upload_folder = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        'product',
        str(product_id)
    )
    os.makedirs(upload_folder, exist_ok=True)
    
    # 完整的文件路徑
    temp_file_path = os.path.join(upload_folder, temp_filename)
    
    # 保存文件
    file.save(temp_file_path)
    
    # 轉換為 WebP 格式
    webp_path = resize_and_convert_to_webp(temp_file_path)
    
    if webp_path:
        # 返回相對路徑 product/{product_id}/filename.webp (使用 / 而非 os.path.join 以確保 URL 路徑正確)
        webp_filename = os.path.basename(webp_path)
        return f"product/{product_id}/{webp_filename}"
    
    return None

def save_store_image(file, store_id):
    """保存店鋪圖片到 static/uploads/store/{store_id}/ 目錄"""
    if not file or not allowed_file(file.filename):
        return None
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    original_ext = file.filename.rsplit('.', 1)[1].lower()
    temp_filename = f"{timestamp}_{unique_id}.{original_ext}"
    
    # 創建上傳目錄 static/uploads/store/{store_id}/
    upload_folder = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        'store',
        str(store_id)
    )
    os.makedirs(upload_folder, exist_ok=True)
    
    # 完整的文件路徑
    temp_file_path = os.path.join(upload_folder, temp_filename)
    
    # 保存文件
    file.save(temp_file_path)
    
    # 轉換為 WebP 格式
    webp_path = resize_and_convert_to_webp(temp_file_path, max_size=(1200, 600))  # banner 尺寸更大
    
    if webp_path:
        # 返回相對路徑 store/{store_id}/filename.webp
        webp_filename = os.path.basename(webp_path)
        return f"store/{store_id}/{webp_filename}"
    
    return None

def delete_product_image(image_path):
    """刪除商品圖片"""
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        print(f"刪除圖片錯誤: {e}")
    return False

def delete_store_image(image_path):
    """刪除店鋪圖片"""
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        print(f"刪除圖片錯誤: {e}")
    return False

def secure_filename(filename):
    """安全的文件名處理"""
    import re
    # 移除危險字符
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    return filename
