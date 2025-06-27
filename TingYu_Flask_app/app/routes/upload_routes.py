#图像上传相关路由
from flask import Blueprint, request, jsonify, current_app
from ..services.file_service import FileService

#创建蓝图
bp = Blueprint('upload', __name__, url_prefix = '/api')

@bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to TingYu Flask App!"}), 200

@bp.route('/upload', methods=['POST','GET'])
def upload_image():
    """处理图像上传"""
    #1.检查是否有文件
    if 'file' not in request.files:
        return jsonify({"error": "没有上传文件"}), 400
    
    file = request.files['file']

    #2.检查文件名
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400
    
    try:
        file_service = FileService(current_app)
        result = file_service.save_uploaded_file(file)
        return jsonify(result)
    except Exception as e:
        import traceback
        current_app.logger.error('文件上传失败: %s', e)
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": "文件上传失败: " + str(e)}), 500
