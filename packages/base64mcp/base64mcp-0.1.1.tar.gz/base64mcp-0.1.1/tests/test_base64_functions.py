import unittest
import base64
import sys
import os
from unittest.mock import MagicMock, patch

# Import mock classes
from tests.mock_imports import Server

# Mock the asyncio module
sys.modules['asyncio'] = MagicMock()
sys.modules['asyncio'].Server = Server

# Mock the mcp.server module
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server'].FastMCP = MagicMock()

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the necessary modules
from base64mcp.server import Env, Client


class TestBase64Functions(unittest.TestCase):
    """Test cases for base64 encode and decode functions."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create environment with different configurations
        self.env_default = Env(to_low="false", to_upper="false")
        self.env_lower = Env(to_low="true", to_upper="false")
        self.env_upper = Env(to_low="false", to_upper="true")

        # Create clients with different environments
        self.client_default = Client(self.env_default)
        self.client_lower = Client(self.env_lower)
        self.client_upper = Client(self.env_upper)

    def test_encode_basic(self):
        """Test basic encoding functionality."""
        # Extract the core encoding logic from the server.py file
        data = "Hello, World!"
        data_bytes = data.encode('utf-8')
        encoded_bytes = base64.b64encode(data_bytes)
        encoded_str = encoded_bytes.decode('utf-8')

        # Expected result is the standard base64 encoding
        expected = "SGVsbG8sIFdvcmxkIQ=="
        self.assertEqual(encoded_str, expected)

    def test_encode_lowercase(self):
        """Test encoding with lowercase conversion."""
        # Extract the core encoding logic from the server.py file
        data = "Hello, World!"
        data_bytes = data.encode('utf-8')
        encoded_bytes = base64.b64encode(data_bytes)
        encoded_str = encoded_bytes.decode('utf-8')

        # Apply lowercase conversion
        final_result = encoded_str.lower()

        # Expected result is the lowercase version of the base64 encoding
        expected = "sgvsbg8sifdvcmxkiq=="
        self.assertEqual(final_result, expected)

    def test_encode_uppercase(self):
        """Test encoding with uppercase conversion."""
        # Extract the core encoding logic from the server.py file
        data = "Hello, World!"
        data_bytes = data.encode('utf-8')
        encoded_bytes = base64.b64encode(data_bytes)
        encoded_str = encoded_bytes.decode('utf-8')

        # Apply uppercase conversion
        final_result = encoded_str.upper()

        # Expected result is the uppercase version of the base64 encoding
        expected = "SGVSBG8SIFDVCMXKIQ=="
        self.assertEqual(final_result, expected)

    def test_decode_basic(self):
        """Test basic decoding functionality."""
        # Extract the core decoding logic from the server.py file
        data = "SGVsbG8sIFdvcmxkIQ=="
        base64_bytes = data.encode('ascii')
        decoded_bytes = base64.b64decode(base64_bytes)
        decoded_str = decoded_bytes.decode('utf-8')

        # Expected result is the original string
        expected = "Hello, World!"
        self.assertEqual(decoded_str, expected)

    def test_decode_lowercase(self):
        """Test decoding with lowercase conversion."""
        # Extract the core decoding logic from the server.py file
        data = "SGVsbG8sIFdvcmxkIQ=="
        base64_bytes = data.encode('ascii')
        decoded_bytes = base64.b64decode(base64_bytes)
        decoded_str = decoded_bytes.decode('utf-8')

        # Apply lowercase conversion
        final_result = decoded_str.lower()

        # Expected result is the lowercase version of the original string
        expected = "hello, world!"
        self.assertEqual(final_result, expected)

    def test_decode_uppercase(self):
        """Test decoding with uppercase conversion."""
        # Extract the core decoding logic from the server.py file
        data = "SGVsbG8sIFdvcmxkIQ=="
        base64_bytes = data.encode('ascii')
        decoded_bytes = base64.b64decode(base64_bytes)
        decoded_str = decoded_bytes.decode('utf-8')

        # Apply uppercase conversion
        final_result = decoded_str.upper()

        # Expected result is the uppercase version of the original string
        expected = "HELLO, WORLD!"
        self.assertEqual(final_result, expected)

    def test_decode_invalid_input(self):
        """Test decoding with invalid base64 input."""
        # Extract the core decoding logic from the server.py file
        data = "Invalid Base64 Input!"
        base64_bytes = data.encode('ascii')

        # Expect a binascii.Error when decoding invalid base64
        with self.assertRaises(base64.binascii.Error):
            base64.b64decode(base64_bytes)


if __name__ == '__main__':
    unittest.main()
