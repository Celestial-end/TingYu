import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.qwen_service import analyse_image, daily_talk, voice_generate

class TestQwenService(unittest.TestCase):
    """测试Qwen服务模块"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建测试文件
        self.test_image_path = "test_images/test1.jpg"
        with open(self.test_image_path, 'w') as f:
            f.write('mock image content')
            
        self.test_text_path = "test_texts/test1.txt"
        with open(self.test_text_path, 'w') as f:
            f.write('测试文本内容')
            
        self.test_out_path = "test_output/test_audio.wav"
    
    def tearDown(self):
        """清理测试环境"""
        # 删除测试文件
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
            
        if os.path.exists(self.test_text_path):
            os.remove(self.test_text_path)
            
        if os.path.exists(self.test_out_path):
            os.remove(self.test_out_path)
    
    @patch('app.services.qwen_service.MultiModalConversation.call')
    def test_analyse_image(self, mock_call):
        """测试图像分析功能"""
        # 模拟返回值
        mock_response = MagicMock()
        mock_response.output.choices[0].message.content = [{'text': '测试图像描述'}]
        mock_call.return_value = mock_response
        
        result = analyse_image(self.test_image_path)
        self.assertEqual(result, '测试图像描述')
        
    @patch('app.services.qwen_service.MultiModalConversation.call')
    def test_daily_talk(self, mock_call):
        """测试日常对话生成"""
        # 模拟返回值
        mock_response = MagicMock()
        mock_response.output.choices[0].message.content = [{'text': '测试回复'}]
        mock_call.return_value = mock_response
        
        result = daily_talk()
        self.assertEqual(result, '测试回复')
        
    @patch('app.services.qwen_service.SpeechSynthesizer')
    def test_voice_generate(self, mock_speech_synthesizer):
        """测试语音生成功能"""
        # 准备测试数据
        mock_audio_data = b'test_audio_data'
        
        # 设置模拟对象
        mock_instance = mock_speech_synthesizer.return_value
        mock_instance.generate_audio.return_value = mock_audio_data
        
        # 执行测试
        voice_generate(None, self.test_text_path, self.test_out_path)
        
        # 验证结果
        mock_speech_synthesizer.assert_called_once_with(model="cosyvoice-v1", voice="longfeifei_v2")
        mock_instance.generate_audio.assert_called_once_with(self.test_text_path)
        
        with open(self.test_out_path, 'rb') as f:
            data = f.read()
            self.assertEqual(data, mock_audio_data)

if __name__ == '__main__':
    unittest.main()