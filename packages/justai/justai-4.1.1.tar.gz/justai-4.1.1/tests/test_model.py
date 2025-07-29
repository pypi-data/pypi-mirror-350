import os
import unittest
from unittest.mock import patch
from justai.model.model import Model


class TestAgent(unittest.TestCase):
    def setUp(self):
        # Lijst van netwerken om te testen
        self.networks = ["gpt-4o", "gpt-4o-mini", "claude-3-opus-20240229", "claude-3-5-sonnet-20240620", 
                         "gemini-1.5-pro", "gemini-1.5-pro"]
        self.models = [Model(network) for network in self.networks]

    def test_chat(self):
        for i, model in enumerate(self.models):
            with self.subTest(network=self.networks[i]):
                with patch('justai.tools.cache.cached_llm_response') as mock_response:
                    mock_response.return_value = ("Test response", 10, 5)
                    response = model.chat("Test prompt")
                    self.assertEqual(isinstance(response, str), True)
                    self.assertGreater(len(response), 0)

    def test_append_messages(self):
        for i, model in enumerate(self.models):
            with self.subTest(network=self.networks[i]):
                model.append_messages("Test message")
                self.assertEqual(len(model.messages), 1)
                self.assertEqual(model.messages[0].content, "Test message")

    def test_reset(self):
        for i, model in enumerate(self.models):
            with self.subTest(network=self.networks[i]):
                model.append_messages("Test message")
                model.reset()
                self.assertEqual(len(model.messages), 0)

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    unittest.main()