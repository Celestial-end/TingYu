#应用初始化
from flask import Flask
from dotenv import load_dotenv
import os

#加载环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)

    # 设置上传文件夹
    upload_folder = os.getenv('UPLOAD_FOLDER', 'storage/uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder

    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)

    # 基础配置
    default_max_size = 16 * 1024 * 1024  # 16MB
    try:
        max_size_env = os.getenv('MAX_CONTENT_LENGTH')
        if max_size_env is not None:
            app.config['MAX_CONTENT_LENGTH'] = int(max_size_env)
        else:
            app.config['MAX_CONTENT_LENGTH'] = default_max_size
    except ValueError:
        # 如果转换失败，回退到默认值
        app.config['MAX_CONTENT_LENGTH'] = default_max_size

    # 导入并注册上传路由蓝图
    from app.routes.upload_routes import bp as upload_bp
    app.register_blueprint(upload_bp)

    return app
