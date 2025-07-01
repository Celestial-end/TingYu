import unittest
from unittest.mock import patch, MagicMock

from app.services.qwen_service import analyse_image, daily_talk


class TestQwenService(unittest.TestCase):
    
    @patch('app.services.qwen_service.MultiModalConversation.call')
    @patch('app.services.qwen_service.os.path.exists')
    def test_analyse_image(self, mock_exists, mock_call):
        # Arrange
        image_path = 'path/to/image.jpg'
        expected_response = 'This is a test response.'
        
        mock_exists.return_value = True
        
        mock_content = MagicMock()
        mock_content.__getitem__.return_value = expected_response
        
        mock_message = MagicMock()
        mock_message.content = [mock_content]
        
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        
        mock_output = MagicMock()
        mock_output.choices = [mock_choice]
        
        mock_response = MagicMock()
        mock_response.output = mock_output
        mock_call.return_value = mock_response

        # Act
        result = analyse_image(image_path)

        # Assert
        self.assertEqual(result, expected_response)
        mock_call.assert_called_once()

    @patch('app.services.qwen_service.MultiModalConversation.call')
    def test_daily_talk(self, mock_call):
        # Arrange
        expected_response = 'This is a test response for daily talk.'
        
        mock_response = MagicMock()
        mock_response.output.choices[0].message.content = [{'text': expected_response}]
        mock_call.return_value = mock_response

        # Act
        result = daily_talk()

        # Assert
        self.assertEqual(result, expected_response)
        mock_call.assert_called_once()


if __name__ == '__main__':
    unittest.main()