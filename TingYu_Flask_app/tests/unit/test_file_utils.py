import pytest
from app.utils import file_utils
from pathlib import Path
from io import BytesIO

# 获取资源目录路径
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

# 使用示例
sample_jpg = RESOURCES_DIR / "sample.jpg"
invalid_txt = RESOURCES_DIR / "invalid.txt"
large_jpg = RESOURCES_DIR / "large.jpg"

def test_allow_file():
    #测试有效扩展名
    assert file_utils.allow_file("image.png") is True
    assert file_utils.allow_file("photo.jpg") is True

    #测试无效扩展名
    assert file_utils.allow_file("file.exe") is False
    assert file_utils.allow_file("document.pdf") is False

def test_generate_unique_filename():
    filename = "test_image.png"
    unique_filename = file_utils.generate_unique_filename(filename)
    
    #测试生成的文件名格式
    assert unique_filename.endswith(".png")
    assert 36 <= len(unique_filename) <= 37 # UUID + '.' + 扩展名

    #验证唯一性
    unique_filename2 = file_utils.generate_unique_filename(filename)
    assert unique_filename != unique_filename2

def test_validate_image_content():
    # 有效JPEG
    jpeg_stream = BytesIO(b'\xff\xd8\xff\xe0\x00\x10JFIF')
    assert file_utils.validate_image_content(jpeg_stream) is True
    
    # 有效PNG
    png_stream = BytesIO(b'\x89PNG\r\n\x1a\n')
    assert file_utils.validate_image_content(png_stream) is True
    
    # 无效内容
    invalid_stream = BytesIO(b'Invalid image content')
    assert file_utils.validate_image_content(invalid_stream) is False