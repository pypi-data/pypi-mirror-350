import unittest
from unittest.mock import Mock, patch
from whispa_app.translation import translate, translate_text, TranslationError, MODEL_MAP

class TestTranslation(unittest.TestCase):
    """Test cases for translation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_text = "Hello, this is a test."
        
    def test_empty_text_returns_empty(self):
        """Test that empty text returns empty string"""
        self.assertEqual(translate("", "English"), "")
        self.assertEqual(translate("   ", "English"), "")
        
    def test_invalid_language_raises_error(self):
        """Test that invalid target language raises ValueError"""
        with self.assertRaises(ValueError) as context:
            translate(self.sample_text, "InvalidLanguage")
        self.assertIn("Unsupported target language", str(context.exception))
        
    def test_supported_languages(self):
        """Test that all advertised languages are in MODEL_MAP"""
        expected_languages = {"English", "Spanish", "French", "German", "Chinese", "Japanese"}
        self.assertEqual(set(MODEL_MAP.keys()), expected_languages)
        
    @patch('whispa_app.translation.get_translation_model')
    def test_translation_error_handling(self, mock_get_model):
        """Test that translation errors are properly handled"""
        mock_get_model.side_effect = Exception("Model loading failed")
        
        with self.assertRaises(TranslationError) as context:
            translate(self.sample_text, "English")
        self.assertIn("Translation failed", str(context.exception))
        
    @patch('whispa_app.translation.translate')
    def test_translate_text_wrapper(self, mock_translate):
        """Test that translate_text properly wraps translate"""
        translate_text(self.sample_text, "English")
        mock_translate.assert_called_once_with(self.sample_text, "English")

if __name__ == '__main__':
    unittest.main() 