import unittest
import os
import json
from unittest.mock import patch, MagicMock
from langchain_google_genai import GoogleGenerativeAI
from cneura_ai import GeminiLLM  


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_google_genai")

class TestGeminiLLM(unittest.TestCase):

    def setUp(self):
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            raise ValueError("Gemini API key is required for testing")
        self.model = GeminiLLM(api_key=API_KEY)

    def test_initialization_with_api_key(self):
        self.assertEqual(self.model.api_key, os.getenv("GEMINI_API_KEY"))
        self.assertIsInstance(self.model.model, GoogleGenerativeAI)

    @patch('langchain_google_genai.GoogleGenerativeAI.invoke')
    def test_query_with_real_api(self, mock_invoke):
        mock_invoke.return_value = '{"field1": "value1", "field2": 123}' 
        response = self.model.query("Test prompt")
        
        if isinstance(response["data"], str):
            response["data"] = json.loads(response["data"])


        self.assertTrue(response["success"])
        self.assertEqual(response["data"], {"field1": "value1", "field2": 123})

    @patch('langchain_google_genai.GoogleGenerativeAI.invoke')
    def test_query_with_no_response(self, mock_invoke):
        mock_invoke.return_value = None
        response = self.model.query("Test prompt")
        self.assertFalse(response.get("success", False))
        self.assertEqual(response.get("error"), "No response from LLM")

if __name__ == '__main__':
    unittest.main()
