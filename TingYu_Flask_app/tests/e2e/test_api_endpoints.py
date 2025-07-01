#端到端测试
import pytest
import requests
import os
import time
import uuid

# 基础URL - 根据实际部署调整
BASE_URL = "http://localhost:5000"
from pathlib import Path

# 获取资源目录路径
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

# 使用示例
sample_jpg = RESOURCES_DIR / "sample.jpg"
invalid_txt = RESOURCES_DIR / "invalid.txt"
large_jpg = RESOURCES_DIR / "large.jpg"

@pytest.fixture(scope="module")
def test_image():
    return open('tests/resources/sample.jpg', 'rb')

def test_full_upload_workflow(test_image):
    # 1. 测试上传API
    files = {'image': ('test_image.jpg', test_image, 'image/jpeg')}
    response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    assert response.status_code == 200
    upload_data = response.json()
    assert upload_data['status'] == 'success'
    assert 'filename' in upload_data
    
    # 2. 验证文件是否可访问
    # (实际部署中可能需要配置静态文件路由)
    # 这里我们直接检查文件系统
    file_path = upload_data['path']
    assert os.path.exists(file_path)
    
    # 3. 验证文件内容
    file_size = os.path.getsize(file_path)
    assert file_size > 0
    
    # 4. 清理测试文件
    os.remove(file_path)
    assert not os.path.exists(file_path)

def test_concurrent_uploads():
    # 测试并发处理能力
    urls = [f"{BASE_URL}/api/upload" for _ in range(5)]
    files = [{'image': (f'test_{i}.jpg', open('tests/resources/sample.jpg', 'rb'), 'image/jpeg')} 
             for i in range(5)]
    
    responses = [requests.post(url, files=file) for url, file in zip(urls, files)]
    
    for response in responses:
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
    
    # 清理文件
    for response in responses:
        file_path = response.json()['path']
        os.remove(file_path)