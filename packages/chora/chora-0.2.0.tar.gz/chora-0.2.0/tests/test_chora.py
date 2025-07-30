#!/usr/bin/env python3
"""
Simple test script to verify chora server functionality.
"""

import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests


def create_test_structure(root_dir):
    """Create a test file structure for chora."""
    root = Path(root_dir)

    # Create GET /users endpoint
    users_get = root / "users" / "GET"
    users_get.mkdir(parents=True, exist_ok=True)

    (users_get / "DATA").write_text('{"users": ["alice", "bob"]}')
    (users_get / "STATUS").write_text("200")
    (users_get / "HEADERS").write_text("Content-Type: application/json")

    # Create GET /users/123 endpoint
    user_123_get = root / "users" / "123" / "GET"
    user_123_get.mkdir(parents=True, exist_ok=True)

    (user_123_get / "DATA").write_text('{"id": 123, "name": "alice"}')
    (user_123_get / "STATUS").write_text("200")
    (user_123_get / "HEADERS").write_text("Content-Type: application/json")

    # Create POST /users endpoint
    users_post = root / "users" / "POST"
    users_post.mkdir(parents=True, exist_ok=True)

    (users_post / "DATA").write_text('{"success": true, "id": 456}')
    (users_post / "STATUS").write_text("201")
    (users_post / "HEADERS").write_text("Content-Type: application/json")


def test_chora_server():
    """Test the chora server."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test structure
        create_test_structure(temp_dir)

        # Start chora server
        print(f"Starting chora server with root: {temp_dir}")
        process = subprocess.Popen(
            [sys.executable, "-m", "chora", "--root", temp_dir, "--port", "8080"]
        )

        try:
            # Wait a moment for server to start
            time.sleep(2)

            # Test GET /users
            response = requests.get("http://localhost:8080/users")
            print(f"GET /users: {response.status_code} - {response.text}")
            assert response.status_code == 200
            assert "alice" in response.text

            # Test GET /users/123
            response = requests.get("http://localhost:8080/users/123")
            print(f"GET /users/123: {response.status_code} - {response.text}")
            assert response.status_code == 200
            assert "alice" in response.text

            # Test POST /users
            response = requests.post(
                "http://localhost:8080/users", json={"name": "charlie"}
            )
            print(f"POST /users: {response.status_code} - {response.text}")
            assert response.status_code == 201
            assert "success" in response.text

            # Test 404
            response = requests.get("http://localhost:8080/nonexistent")
            print(f"GET /nonexistent: {response.status_code}")
            assert response.status_code == 404

            print("All tests passed!")

        finally:
            # Stop the server
            process.terminate()
            process.wait()


if __name__ == "__main__":
    test_chora_server()
