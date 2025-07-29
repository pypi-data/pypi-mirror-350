# In tests/test_generator.py
from uuid7.generator import UUIDv7 # Correct module and class name
import unittest

class TestUUIDv7Generator(unittest.TestCase):
    def test_generation(self):
        generator = UUIDv7() # Use the correct class name
        uid = generator.generate()
        self.assertIsInstance(uid, str)
        self.assertEqual(len(uid), 36) # Basic check for UUID format
        # Add more specific tests for UUIDv7 properties if desired

if __name__ == '__main__':
    unittest.main()