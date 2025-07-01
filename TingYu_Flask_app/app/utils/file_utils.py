import os
import uuid
from werkzeug.utils import secure_filename

def allow_file(filename):
    """检查文件扩展名是否合法"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','mp4','wav','avi','wmv','mp3'}
    return '.' in filename and filename and \
              filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """生成唯一文件名"""
    filename = secure_filename(filename)
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

def validate_image_content(file_stream):
    """验证文件内容是否为有效图像"""
    header = file_stream.read(512) #读取图片文件头
    file_stream.seek(0) #重置指针

    #检查常见的图片类型的文件头
    if header.startswith(b'\xff\xd8\xff'): #JPEG的文件头
        return True
    elif header.startswith(b'\x89PNG\r\n\x1a\n'): #PNG的文件头
        return True
    elif header.startswith(b'GIF8'): #GIF的文件头
        return True
    else:
        return False
    
def validate_video_content(file_stream):
    """检验文件内容是否为有效视频"""
    header = file_stream.read(10)#读取视频文件头
    file_stream.seek(0)

    if header.startswith(b'\x00\x00\x00\x18'): #MP4的文件头
        return True
    elif header.startswith(b'\x00\x00\x01'): #AVI的文件头
        return True
    elif header.startswith(b'\x00\x00\x00\x20'): #WMV的文件头
        return True
    elif header.startswith(b'RIFF') and header[8:12] == b'AVI ': #AVI的文件头
        return True
    else:
        return False
    
def validate_audio_content(file_stream):
    header = file_stream.read(12)
    file_stream.seek(0)
    if header.startswith(b'RIFF') and header[8:12] == b'WAVE': #WAV的文件头
        return True
    elif header.startswith(b'fmt ') and header[12:16] == b'WAVE': #WAV的文件头
        return True
    elif header.startswith(b'ID3'): #MP3的文件头
        return True
    else:
        return False