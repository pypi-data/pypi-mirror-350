import unittest
from hungovercoders_repo_tools import greetings

class TestExample(unittest.TestCase):
    def test_hello(self):
        # Capture the output of the hello function
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        greetings.hello()
        sys.stdout = sys.__stdout__
        self.assertIn("Hello from hungovercoders-repo-tools!", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()
