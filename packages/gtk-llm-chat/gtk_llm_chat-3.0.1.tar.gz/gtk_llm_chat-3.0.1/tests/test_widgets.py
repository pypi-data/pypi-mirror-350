import unittest
from gtk_llm_chat.widgets import Message

class TestWidgets(unittest.TestCase):
    def test_message_content(self):
        msg = Message("Test", "user")
        self.assertEqual(msg.content, "Test")

    def test_file_reference(self):
        self.assertIn("test_widgets.py", __file__)

if __name__ == "__main__":
    unittest.main()
