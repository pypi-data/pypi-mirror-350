import unittest
from justai.model.message import Message, is_image_url

class TestMessage(unittest.TestCase):
    def test_message_creation(self):
        message = Message("user", "Test content")
        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "Test content")

    def test_message_to_dict(self):
        message = Message("user", "Test content")
        message_dict = message.to_dict()
        self.assertEqual(message_dict["role"], "user")
        self.assertEqual(message_dict["content"], "Test content")

    def test_is_image_url(self):
        valid_url = "https://example.com/image.jpg"
        invalid_url = "https://example.com/not_an_image.txt"
        self.assertTrue(is_image_url(valid_url))
        self.assertFalse(is_image_url(invalid_url))

if __name__ == '__main__':
    import os
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    unittest.main()