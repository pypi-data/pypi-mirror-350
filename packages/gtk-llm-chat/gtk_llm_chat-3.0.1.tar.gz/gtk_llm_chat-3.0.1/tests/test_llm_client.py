import unittest
import time
from unittest.mock import MagicMock
from gi.repository import GLib

from gtk_llm_chat.llm_client import LLMClient, DEBUG

class TestLLMClient(unittest.TestCase):
    def setUp(self):
        self.client = LLMClient()
        self.client.model = MagicMock()
        self.client.model.model_id = "test-model"
        self.client.conversation = MagicMock()
        self.client.conversation.id = "test-conversation"
        self.client.conversation.prompt = MagicMock(return_value=["chunk1", "chunk2"])
        self.client.conversation.responses = []
        self.client._is_generating_flag = False
        self.client._stream_thread = None
        self.client._init_error = None

    def test_send_message_emits_response(self):
        responses = []
        self.client.connect('response', lambda obj, chunk: responses.append(chunk))
        self.client.send_message("test prompt")
        while self.client._stream_thread and self.client._stream_thread.is_alive():
            time.sleep(0.1)
        self.assertEqual(responses, ["chunk1", "chunk2"])

    def test_send_message_emits_finished_success(self):
        finished_result = []
        self.client.connect('finished', lambda obj, success: finished_result.append(success))
        self.client.send_message("test prompt")
        while self.client._stream_thread and self.client._stream_thread.is_alive():
            time.sleep(0.1)
        self.assertTrue(finished_result[0])

    def test_send_message_emits_error_when_already_generating(self):
        errors = []
        self.client.connect('error', lambda obj, error: errors.append(error))
        self.client._is_generating_flag = True
        self.client.send_message("test prompt")
        self.assertEqual(errors, ["Ya se está generando una respuesta."])

    def test_send_message_emits_error_when_model_not_loaded(self):
        errors = []
        self.client.connect('error', lambda obj, error: errors.append(error))
        self.client.model = None
        self.client.send_message("test prompt")
        self.assertEqual(errors, ["Error al inicializar el modelo: Modelo no disponible"])

    def test_send_message_emits_error_during_streaming(self):
        errors = []
        self.client.connect('error', lambda obj, error: errors.append(error))
        self.client.conversation.prompt = MagicMock(side_effect=Exception("Test error"))
        self.client.send_message("test prompt")
        while self.client._stream_thread and self.client._stream_thread.is_alive():
            time.sleep(0.1)
        self.assertEqual(errors, ["Error durante el streaming: Test error"])

    def test_cancel_stops_stream(self):
        self.client.conversation.prompt = MagicMock(return_value=iter(["chunk1", "chunk2"]))
        self.client.send_message("test prompt")
        self.client.cancel()
        while self.client._stream_thread and self.client._stream_thread.is_alive():
            time.sleep(0.1)
        self.assertFalse(self.client._is_generating_flag)

    def test_load_history(self):
        history_entries = [
            {'prompt': 'user1', 'response': 'assistant1'},
            {'prompt': 'user2', 'response': 'assistant2'}
        ]
        self.client.load_history(history_entries)
        self.assertEqual(len(self.client.conversation.responses), 4)

    def test_load_history_no_model(self):
        self.client.model = None
        self.client.load_history([{'prompt': 'user1', 'response': 'assistant1'}])
        self.assertEqual(len(self.client.conversation.responses), 0)

    def test_load_history_no_conversation(self):
        self.client.conversation = None
        self.client.load_history([{'prompt': 'user1', 'response': 'assistant1'}])
        self.assertEqual(len(self.client.conversation.responses), 0)

    def test_get_model_id(self):
        self.assertEqual(self.client.get_model_id(), "test-model")

    def test_get_conversation_id(self):
        self.assertEqual(self.client.get_conversation_id(), "test-conversation")

    def test_get_model_id_none(self):
        self.client.model = None
        self.assertIsNone(self.client.get_model_id())

    def test_get_conversation_id_none(self):
        self.client.conversation = None
        self.assertIsNone(self.client.get_conversation_id())

if __name__ == '__main__':
    DEBUG = True
    unittest.main()
