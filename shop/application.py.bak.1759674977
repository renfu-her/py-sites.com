from flask import Flask
from flask_login import LoginManager
from config import config
from database import init_db
from models import User

def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    config_name = config_name or 'default'
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    init_db(app)
    
    # 初始化登录管理器
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 注册蓝图
    from routes.frontend import frontend_bp
    from routes.backend import backend_bp
    from routes.api import api_bp
    
    app.register_blueprint(frontend_bp)
    app.register_blueprint(backend_bp, url_prefix='/backend')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 自定義 Jinja2 過濾器
    @app.template_filter('none_to_empty')
    def none_to_empty(value):
        """將 None 轉換為空字串"""
        return value if value is not None else ''
    
    # 設置 Jinja2 環境選項
    app.jinja_env.finalize = lambda x: '' if x is None else x
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'error': '页面未找到'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': '服务器内部错误'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
