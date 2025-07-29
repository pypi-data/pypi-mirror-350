#!/bin/env python3
import signal
import unittest
import subprocess
import time
import requests
import os
from tempfile import gettempdir
from serve_dir.server import parse_byte_range


class TestServeDirCommand(unittest.TestCase):
    PORT = 8058  # Default port
    TEST_DIR = os.path.join(gettempdir(), "test_serve_dir")

    @classmethod
    def setUpClass(cls):
        # Create a test directory with some files
        os.makedirs(cls.TEST_DIR, exist_ok=True)
        with open(os.path.join(cls.TEST_DIR, "test.txt"), "w") as f:
            f.write("Hello World")
        with open(os.path.join(cls.TEST_DIR, "test.html"), "w") as f:
            f.write("<h1>Test Index</h1>")

    @classmethod
    def tearDownClass(cls):
        # Clean up test directory
        for f in os.listdir(cls.TEST_DIR):
            os.remove(os.path.join(cls.TEST_DIR, f))
        os.rmdir(cls.TEST_DIR)

    def run_server_command(self, args, timeout=5):
        """Run the server command in a subprocess and return the process"""
        cmd = ["python", "-m", "serve_dir"] + args
        print(f"\nExecuting: {' '.join(cmd)}")

        # Start the server in a subprocess
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=self.TEST_DIR)
        # Wait a bit for server to start
        time.sleep(2)

        # Return the process so caller can manage it
        return process

    # @unittest.skip
    def test_default_serve(self):
        """Test serving with default arguments"""
        process = self.run_server_command([], timeout=5)
        try:
            # Verify server is running
            response = requests.get(f"http://localhost:{self.PORT}")
            self.assertEqual(response.status_code, 200)
            print(response.text)

            # Check if directory listing is working
            self.assertIn("test.html", response.text)

            # Check if we can access a file
            response = requests.get(f"http://localhost:{self.PORT}/test.txt")
            self.assertEqual(response.text, "Hello World")
        finally:
            process.send_signal(signal.SIGINT)
            process.wait()

    # @unittest.skip
    def test_custom_port(self):
        """Test serving with custom port"""
        custom_port = 9999
        process = self.run_server_command(["-p", str(custom_port)], timeout=5)
        try:
            # Verify server is running on custom port
            response = requests.get(f"http://0.0.0.0:{custom_port}")
            self.assertIn("test.html", response.text)
            self.assertEqual(response.status_code, 200)
        finally:
            process.send_signal(signal.SIGINT)
            process.wait()

    # @unittest.skip
    def test_root_directory(self):
        """Test serving from a specific directory"""
        process = self.run_server_command([self.TEST_DIR], timeout=5)
        try:
            # Verify we see our test files
            response = requests.get(f"http://localhost:{self.PORT}")
            self.assertIn("test.txt", response.text)
            self.assertIn("test.html", response.text)
        finally:
            process.send_signal(signal.SIGINT)
            process.wait()

    # @unittest.skip
    def test_byte_range_support(self):
        """Test byte range support"""
        process = self.run_server_command(["--byte-range"], timeout=5)
        try:
            # Test range request
            headers = {"Range": "bytes=0-4"}
            response = requests.get(f"http://localhost:{self.PORT}/test.txt", headers=headers)
            self.assertEqual(response.status_code, 206)  # Partial content
            self.assertEqual(response.text, "Hello"[0:5])
            headers = {"Range": "bytes=100000-400000"}
            response = requests.get(f"http://localhost:{self.PORT}/test.txt", headers=headers)
            self.assertEqual(response.status_code, 416)  # Range Not Satisfiable

        finally:
            process.send_signal(signal.SIGINT)
            process.wait()

    # @unittest.skip
    def test_cgi_support(self):
        """Test CGI support (skipped by default as it requires CGI setup)"""
        # This test would require actual CGI scripts to test properly
        process = self.run_server_command(["--cgi"], timeout=5)
        try:
            # Just verify server starts (actual CGI testing would need more setup)
            response = requests.get(f"http://localhost:{self.PORT}")
            self.assertEqual(response.status_code, 200)
        finally:
            process.send_signal(signal.SIGINT)
            process.wait()

    def test_extra(self):
        a, b = parse_byte_range("bytes=123-456")
        self.assertEqual((a, b), (123, 456))


if __name__ == "__main__":
    unittest.main()
