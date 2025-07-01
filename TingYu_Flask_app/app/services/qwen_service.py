#负责通义千问api调用封装
import requests
from dashscope import MultiModalConversation
from app.config import Config_Cloud
import os
import pyaudio
import dashscope
from dashscope.audio.tts_v2 import *
from .wave2lip_lipmaker_service import video_generate
from app.utils import file_utils

qwen_api_key = Config_Cloud.SYNC_API_KEY

prompt_1 = """
    你是一个听障儿童的说话学习助手，请根据图片中的主要内容，生成一个简短的句子，用于帮助听障儿童学习。  
    要求句子结构严谨,语法严谨,用字标准,句子长度少于超过12个字(不包括标点符号)。
    生成示例1:
        1. 图片内容："一个小男孩在操场上玩耍"
        2. 生成句子："小男孩在操场玩耍"
    生成示例2:
        1.图片内容:"桌子上有一个苹果"
        2.生成句子:"这是一个苹果，被放在桌上。"
    生成示例3:
        1.图片内容:"一只小猫在吃小炒肉"
        2.生成句子:"小猫正在吃小炒肉。"
    生成示例4:
        1.图片内容:"一只小猫在追老鼠"
        2.生成句子:"小猫正在追老鼠。"
    生成示例5:
        1.图片内容:"小狗在守大门"
        2.生成句子:"小狗在大门前守着。"
"""

prompt_2 = """
    你是听障儿童的说话学习助手，根据语音内容，给出积极的反馈，以鼓励听障儿童说话。
    生成示例:
        你好呀小朋友。
        你的努力很棒哦，你说的也很标准，再努力一下就可以说的更好了！
        我也在努力学习更多知识来帮助你，我会一直在你身边的。
        你可以多和我交流，多和我互动，我们可以聊一聊。
        加油！相信你自己！

"""

def analyse_image(image_path) -> str:
    """调用Qwen-VL模型分析上传的图像内容并返回描述"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图像文件不存在: {image_path}")
    
    response = MultiModalConversation.call(
        api_key = qwen_api_key,
        model = "qwen-vl-plus",
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "content": prompt_1
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {"image": image_path},
                    {"text": "请告诉我图中这个是什么东西，并用一个简短的句子描述。"}
                ]
            }
        ],
        result_format = "text", 
        top_p = 0.2,
    )

    return response.output.choices[0].message.content[0]['text']

def daily_talk()-> str:
    """调用Qwen-VL模型和Qwen-7B模型进行日常话题生成"""
    prompt = prompt_1
    response = MultiModalConversation.call(
        model = "qwen-max",
        messages=[
            {
                "role": "system",
                "content": [
                    {"text": prompt_2}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"text": "我听不到声音，我想学习说话"}
                ]
            }
        ]
    )
    return response.output.choices[0].message.content[0]['text']




def audio_generate(text_path,out_path):
    """把输入的文字转换为音频"""
    model = "cosyvoice-v1"
    voice = "longfeifei_v2"
    text_to_word = SpeechSynthesizer(model=model, voice=voice)
    audio = text_to_word.generate_audio(text_path)
    with open(out_path, "wb") as f:
        f.write(audio)
    print("音频生成成功")
    return audio

def voice_generate(video_path,text_path,out_path):
    """把音频转换为唇语视频"""
    audio = audio_generate(text_path,out_path)
    audio_path = file_utils.generate_unique_filename(audio)
    out_path = video_generate(video_path,audio_path)
    return out_path

def model_comment(audio_path):
    model =  "qwen-audio-turbo",
    api_key = qwen_api_key,
    message = [
        {
            "role": "user",
            "content":[
                {"audio":audio_path},
                {"text": prompt_2}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(
        model = model,
        api_key = api_key,
        messages = message,
        result_format = "message"
    )
    return response.result.message.content.text