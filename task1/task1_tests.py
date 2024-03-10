import unittest
from task1 import get_response
from langchain_core.messages import AIMessage, HumanMessage

class TestResponse(unittest.TestCase):
    
    def test_context(self):
        chat_history = []
        question = "Do you know any strategic objects?"
        response = get_response(question, chat_history)
        self.assertTrue(
            response.find("Neapolis Smart EcoCity") != -1 or \
            response.find("City Eco Parking") or \
            response.find("Autonomous Public Transportation"),
            "The context is insufficient or not provided at all!"
        )

    def test_history(self):
        chat_history = []
        question = "Does Paphos has a mall?"
        ai_response = get_response(question, chat_history)
        print(ai_response)
        chat_history.extend([HumanMessage(content=question), ai_response])
        second_question = "Does it have an electronic store?"
        ai_second_response = get_response(second_question, chat_history)
        print(ai_second_response)
        self.assertTrue(
            ai_second_response.find("mall") != -1,
            "The chat does not support memory!"
        )
        
if __name__ == '__main__':
    unittest.main()