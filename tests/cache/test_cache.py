import unittest, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from cache import cache

class TestCache(unittest.TestCase):

    users_cache = cache.Cache()
    users_cache.set(1, 'user1')
    users_cache.set(2, 'user2')

    def test_get_user(self):
        self.assertEqual(self.users_cache.get(1), 'user1')

    def test_get_size(self):
        self.assertEqual(self.users_cache.get_size(), 2)
       
    def test_get_size_after_insert(self):
        self.users_cache.set(3, 'user3')
        self.assertEqual(self.users_cache.get_size(), 3)

if __name__ == '__main__':
    unittest.main()