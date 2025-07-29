import unittest
import tempfile
import os
from justai.tools.prompts import set_prompt_file, add_prompt_file, get_prompt

class TestPrompts(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.prompt_file = os.path.join(self.temp_dir, "test_prompts.toml")
        with open(self.prompt_file, "w") as f:
            f.write('test_prompt = "This is a test prompt {variable}"\n')

    def tearDown(self):
        os.remove(self.prompt_file)
        os.rmdir(self.temp_dir)

    def test_set_and_get_prompt(self):
        set_prompt_file(self.prompt_file)
        prompt = get_prompt("test_prompt", variable="value")
        self.assertEqual(prompt, "This is a test prompt value")

    def test_add_prompt_file(self):
        set_prompt_file(self.prompt_file)
        new_prompt_file = os.path.join(self.temp_dir, "new_prompts.toml")
        with open(new_prompt_file, "w") as f:
            f.write('new_prompt = "This is a new prompt {variable}"\n')
        add_prompt_file(new_prompt_file)
        prompt = get_prompt("new_prompt", variable="value")
        self.assertEqual(prompt, "This is a new prompt value")
        os.remove(new_prompt_file)

if __name__ == '__main__':
    unittest.main()