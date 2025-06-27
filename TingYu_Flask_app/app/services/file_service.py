import os
from ..utils import file_utils

class FileService:
    def __init__(self, app):
        self.app = app

    def save_uploaded_file(self, file):
        """保存上传的文件"""
        if not file_utils.allow_file(file.filename):
            raise ValueError("不支持的文件类型")
        
        # 验证文件内容（暂时禁用）
        # if not file_utils.validate_image_content(file.stream):
        #     raise ValueError("无效的图像文件内容")
        
        # 生成唯一文件名
        unique_filename = file_utils.generate_unique_filename(file.filename)
        save_path = os.path.join(self.app.config['UPLOAD_FOLDER'], unique_filename)

        #保存文件
        file.save(save_path)

        return {
            "filename": unique_filename,
            "path": save_path
        }