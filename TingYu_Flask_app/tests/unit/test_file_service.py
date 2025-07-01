import pytest
from unittest.mock import MagicMock
from app.services.file_service import FileService
from werkzeug.datastructures import FileStorage
from pathlib import Path

# 获取资源目录路径
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

# 使用示例
sample_jpg = RESOURCES_DIR / "sample.jpg"
invalid_txt = RESOURCES_DIR / "invalid.txt"
large_jpg = RESOURCES_DIR / "large.jpg"
@pytest.fixture
def mock_app():
    app = MagicMock()
    app.config = {
        'UPLOAD_FOLDER': '/tmp/uploads',
        'MAX_CONTENT_LENGTH': 16 * 1024 * 1024
    }
    return app

def test_save_uploaded_file_success(mock_app, tmp_path):
    # 设置临时上传目录
    mock_app.config['UPLOAD_FOLDER'] = str(tmp_path)
    
    # 创建模拟文件
    file = FileStorage(
        stream=open('tests/resources/sample.jpg', 'rb'),
        filename='sample.jpg',
        content_type='image/jpeg'
    )
    
    service = FileService(mock_app)
    result = service.save_uploaded_file(file)
    
    # 验证结果
    assert 'filename' in result
    assert 'path' in result
    assert result['path'] == str(tmp_path / result['filename'])
    
    # 验证文件是否实际保存
    assert (tmp_path / result['filename']).exists()

def test_save_uploaded_file_invalid_type(mock_app):
    file = MagicMock()
    file.filename = 'invalid.pdf'
    
    service = FileService(mock_app)
    
    with pytest.raises(ValueError, match="不支持的文件类型"):
        service.save_uploaded_file(file)

def test_save_uploaded_file_invalid_content(mock_app):
    # 创建无效内容文件
    file = FileStorage(
        stream=open('tests/resources/invalid.txt', 'rb'),
        filename='fake.jpg',
        content_type='image/jpeg'
    )
    
    service = FileService(mock_app)
    
    with pytest.raises(ValueError, match="无效的图像文件内容"):
        service.save_uploaded_file(file)