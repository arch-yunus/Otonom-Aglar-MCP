import os
import pytest
import sys
import importlib.util

# Load the secure executor module dynamically since it starts with a number
target_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', '04_advanced_agentic_systems', 'secure_executor.py'))
spec = importlib.util.spec_from_file_location("secure_executor", target_file)
secure_executor = importlib.util.module_from_spec(spec)
sys.modules["secure_executor"] = secure_executor
spec.loader.exec_module(secure_executor)

def test_safe_path_valid():
    """Test that valid paths within the sandbox are allowed."""
    assert secure_executor.is_safe_path("test.txt") == True
    assert secure_executor.is_safe_path("folder/file.json") == True
    
def test_safe_path_traversal():
    """Test that path traversal attempts are blocked."""
    assert secure_executor.is_safe_path("../secret.txt") == False
    assert secure_executor.is_safe_path("../../etc/passwd") == False
    assert secure_executor.is_safe_path("folder/../../system.ini") == False

def test_secure_write_blocked(monkeypatch):
    """Test that write function actually blocks and returns an error for invalid paths."""
    result = secure_executor.secure_write_file("../malicious.sh", "echo 'hacked'")
    assert "GÜVENLİK İHLALİ" in result
    assert "Path Traversal" in result

def test_sandbox_dir_is_used():
    """Verify the default sandbox dir points to a safe tmp environment."""
    assert "mcp_sandbox" in secure_executor.SANDBOX_DIR
