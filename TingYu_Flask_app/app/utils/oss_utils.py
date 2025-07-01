import oss2
from config import Config_Cloud
import uuid
import os

def upload_file(file_path, folder="videos"):
    """上传文件到oss"""
    auth = oss2.Auth(Config_Cloud.OSS_ACCESS_KEY_ID, Config_Cloud.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, Config_Cloud.OSS_ENDPOINT, Config_Cloud.OSS_BUCKET_NAME)

    #生成唯一文件名
    ext = os.path.splitext(file_path)[1]
    object_name = f"{folder}/{uuid.uuid4().hex}{ext}"

    #上传文件
    bucket.put_object_from_file(object_name, file_path)

    return f"{Config_Cloud.OSS_ENDPOINT}/{Config_Cloud.OSS_BUCKET_NAME}/{object_name}"

def generate_presigned_url(file_path, expires_in=3600, folder="videos"):
    """生成预签名URL"""
    auth = oss2.Auth(Config_Cloud.OSS_ACCESS_KEY_ID, Config_Cloud.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, Config_Cloud.OSS_ENDPOINT, Config_Cloud.OSS_BUCKET_NAME)

    #生成唯一文件名
    ext = os.path.splitext(file_path)[1]
    object_name = f"{folder}/{uuid.uuid4().hex}{ext}"

    return bucket.sign_url("GET", object_name, expires_in)
