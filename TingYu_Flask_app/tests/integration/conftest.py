# 在文件顶部添加路径设置
import os
import pytest
import sys
from pathlib import Path

# 获取资源目录路径
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

# 使用示例
sample_jpg = RESOURCES_DIR / "sample.jpg"
invalid_txt = RESOURCES_DIR / "invalid.txt"
large_jpg = RESOURCES_DIR / "large.jpg"
# 获取项目根目录路径
project_root = Path(__file__).resolve().parents[2]  # 根据实际目录层级调整
sys.path.insert(0, str(project_root))

# 现在导入应用模块
from app import create_app
# tests/integration/conftest.py
@pytest.fixture(scope='module')
def test_client():
    # 设置测试环境变量
    os.environ['UPLOAD_FOLDER'] = '/tmp/test_uploads'
    # 设置整数字符串值
    os.environ['MAX_CONTENT_LENGTH'] = '16777216'  # 16MB的整数值
    
    # 创建测试应用
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client