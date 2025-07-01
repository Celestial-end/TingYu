import pytest
import os
from werkzeug.datastructures import FileStorage
from pathlib import Path

# 获取资源目录路径
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

# 使用示例
sample_jpg = RESOURCES_DIR / "sample.jpg"
invalid_txt = RESOURCES_DIR / "invalid.txt"
large_jpg = RESOURCES_DIR / "large.jpg"
def test_upload_valid_image(test_client, tmp_path):
    # 设置临时上传目录
    os.environ['UPLOAD_FOLDER'] = str(tmp_path)
    
    # 准备测试文件
    file_path = 'tests/resources/sample.jpg'
    with open(file_path, 'rb') as f:
        file = FileStorage(
            stream=f,
            filename='sample.jpg',
            content_type='image/jpeg'
        )
    
    # 发送请求
    response = test_client.post(
        '/api/upload',
        data={'image': file},
        content_type='multipart/form-data'
    )
    
    # 验证响应
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'filename' in json_data
    assert 'path' in json_data
    
    # 验证文件是否保存
    saved_path = json_data['path']
    assert os.path.exists(saved_path)

def test_upload_no_file(test_client):
    response = test_client.post('/api/upload')
    assert response.status_code == 400
    assert '未找到图片文件' in response.get_json()['error']

def test_upload_invalid_file_type(test_client):
    # 准备无效文件
    file = FileStorage(
        stream=open('tests/resources/invalid.pdf', 'rb'),
        filename='invalid.pdf',
        content_type='application/pdf'
    )
    
    response = test_client.post(
        '/api/upload',
        data={'image': file},
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 400
    assert '不支持的文件类型' in response.get_json()['error']

def test_upload_large_file(test_client, monkeypatch):
    # 设置小文件限制 (1KB)
    monkeypatch.setenv('MAX_FILE_SIZE', '1024')
    
    # 创建大文件 (2KB)
    large_file = FileStorage(
        stream=open('tests/resources/large.jpg', 'rb'),
        filename='large.jpg',
        content_type='image/jpeg'
    )
    
    response = test_client.post(
        '/api/upload',
        data={'image': large_file},
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 413  # Payload Too Large