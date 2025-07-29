import unittest
from justai.tools.cache import CachDB, cached_llm_response
from unittest.mock import patch, MagicMock

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = CachDB()

    def tearDown(self):
        self.cache.clear()
        self.cache.close()

    def test_write_and_read(self):
        self.cache.write("test_key", ("test_value", 10, 5))
        result = self.cache.read("test_key")
        self.assertEqual(result, ("test_value", 10, 5))

    @patch('justai.tools.cache.CachDB')
    def test_cached_llm_response(self, mock_cache):
        mock_model = MagicMock()
        mock_model.chat.return_value = ("Test response", 10, 5)
        mock_cache_instance = mock_cache.return_value
        mock_cache_instance.read.return_value = None

        result = cached_llm_response(mock_model, [], [], False)
        self.assertEqual(result, ("Test response", 10, 5))
        mock_cache_instance.write.assert_called_once()

if __name__ == '__main__':
    unittest.main()