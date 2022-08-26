import unittest, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from controllers import bot_controller

class FakeDatabase:
    def query_get_username(self):
        return [
            { 'userid': 1, 'name': 'user1'},
            { 'userid': 2, 'name': 'user2'}
        ]
db = FakeDatabase()
ctrl = bot_controller.BotControllers(db)
ctrl.load_users()

class TestBotController(unittest.TestCase):

    def test_get_user(self):
        self.assertEqual(ctrl.get_username(1), 'user1')

if __name__ == '__main__':
    unittest.main()