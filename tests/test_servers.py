import pytest
import os
import sys
import importlib.util

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Resolve paths
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
hello_mcp = import_from_path("hello_mcp", os.path.join(base_path, "01_core_mechanics", "hello_mcp.py"))
file_system = import_from_path("file_system_server", os.path.join(base_path, "02_local_servers", "file_system_server.py"))
sqlite_server = import_from_path("sqlite_server", os.path.join(base_path, "02_local_servers", "sqlite_server.py"))

def test_hello_mcp_tools():
    assert hello_mcp.to_upper("hello") == "HELLO"
    assert "world" in hello_mcp.echo("world")

def test_file_system_tools():
    # Current directory should at least have src
    files = file_system.list_directory(".")
    assert "src" in files or "README.md" in files

def test_sqlite_describe_non_existent():
    # describe_table should handle non-existent tables or errors gracefully through tool_error_handler
    result = sqlite_server.describe_table("non_existent.db", "some_table")
    assert isinstance(result, str)
    assert "HATA" in result or "error" in result.lower()

# Note: Integration tests with actual LLM calls are skipped in unit tests
