import unittest
from pygridgain import Client
from langchain_core.messages import HumanMessage, AIMessage
from langchain_gridgain.chat_message_histories import GridGainChatMessageHistory

class TestGridGainChatMessageHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up GridGain/Apache Ignite client
        # Modify these connection details as per your GridGain/Apache Ignite setup
        cls.client = Client()
        cls.client.connect('localhost', 10800)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def setUp(self):
        self.session_id = "test_session"
        self.history = GridGainChatMessageHistory(
            session_id=self.session_id,
            client=self.client
        )

    def tearDown(self):
        self.history.clear()

    def test_add_and_retrieve_messages(self):
        # Test adding and retrieving messages
        messages = [
            HumanMessage(content="Hello, AI!"),
            AIMessage(content="Hello, human! How can I assist you today?"),
            HumanMessage(content="What's the weather like?"),
            AIMessage(content="I'm sorry, but I don't have access to real-time weather information. You might want to check a weather app or website for the most up-to-date weather conditions in your area.")
        ]

        self.history.add_messages(messages)

        retrieved_messages = self.history.messages

        self.assertEqual(len(retrieved_messages), len(messages))
        for original, retrieved in zip(messages, retrieved_messages):
            self.assertEqual(original.content, retrieved.content)
            self.assertEqual(type(original), type(retrieved))

    def test_clear_messages(self):
        # Test clearing messages
        messages = [
            HumanMessage(content="This is a test message."),
            AIMessage(content="This is a test response.")
        ]

        self.history.add_messages(messages)
        self.assertEqual(len(self.history.messages), 2)

        self.history.clear()
        self.assertEqual(len(self.history.messages), 0)

    def test_multiple_sessions(self):
        # Test handling multiple sessions
        session1 = GridGainChatMessageHistory(session_id="session1", client=self.client)
        session2 = GridGainChatMessageHistory(session_id="session2", client=self.client)

        session1.add_messages([HumanMessage(content="Message for session 1")])
        session2.add_messages([HumanMessage(content="Message for session 2")])

        self.assertEqual(len(session1.messages), 1)
        self.assertEqual(len(session2.messages), 1)
        self.assertEqual(session1.messages[0].content, "Message for session 1")
        self.assertEqual(session2.messages[0].content, "Message for session 2")

        session1.clear()
        session2.clear()

if __name__ == '__main__':
    unittest.main()