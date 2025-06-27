#负责通义千问api调用封装
import requests
from dashscope import MultiModalConversation
import os

DashScope_API_kEY = os.getenv('DASHSCOPE_API_KEY')

def analyse_image(image_path) -> str:
    """调用Qwen-VL模型分析上传的图像内容并返回描述"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图像文件不存在: {image_path}")
    
    response = MultiModalConversation.call(
        model = "qwen-vl-plus",
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "content": "你是一个图像分析专家，能够描述图中的物体是什么并给出相关词语"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {"image": image_path},
                    {"text": "请告诉我图中这个是什么东西，并给出相关的词语"}
                ]
            }
        ]
    )

    return response.output.choices[0].message.content[0]['text']

