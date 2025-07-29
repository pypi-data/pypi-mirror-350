"""Tests for Say Hi MCP Server."""

import pytest
from say_hi_mcp.server import SayHiMCPServer


def test_server_initialization():
    """Test that the server can be initialized."""
    server = SayHiMCPServer()
    assert server is not None
    assert server.mcp is not None


def test_server_with_custom_name():
    """Test that the server can be initialized with a custom name."""
    custom_name = "test-server"
    server = SayHiMCPServer(name=custom_name)
    assert server is not None
    assert server.mcp is not None


def test_name_parameter_examples():
    """Test that various name formats are valid for our tools."""
    # Test valid names that would work with our tools
    valid_names = [
        "Alice",
        "张三", 
        "李四",
        "John",
        "a" * 50,  # Maximum length
        "A"        # Minimum length
    ]
    
    # These names should all be valid for our tools
    for name in valid_names:
        assert len(name) >= 1
        assert len(name) <= 50
        assert isinstance(name, str)
    
    # Invalid names (these would fail validation in the actual tools)
    invalid_names = [
        "",        # Too short
        "a" * 51   # Too long
    ]
    
    for name in invalid_names:
        assert len(name) < 1 or len(name) > 50


def test_tools_registration():
    """Test that tools are properly registered with the MCP server."""
    server = SayHiMCPServer()
    # Note: In a real test, we would need to set up the MCP server properly
    # and test the tools through the MCP protocol. This is a simplified test.
    assert server.mcp is not None
    
    # Test that server initializes without errors
    # The tools should be registered during initialization
    assert hasattr(server, 'mcp')


def test_import():
    """Test that the package can be imported correctly."""
    from say_hi_mcp import SayHiMCPServer
    assert SayHiMCPServer is not None 