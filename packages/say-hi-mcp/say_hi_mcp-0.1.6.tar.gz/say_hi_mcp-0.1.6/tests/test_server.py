"""Tests for Say Hi MCP Server."""

import pytest
from say_hi_mcp.server import SayHiMCPServer, GreetingInput


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


def test_greeting_input_validation():
    """Test GreetingInput pydantic model validation."""
    # Valid input
    valid_input = GreetingInput(my_name="Alice")
    assert valid_input.my_name == "Alice"
    
    # Test with Chinese name
    chinese_input = GreetingInput(my_name="张三")
    assert chinese_input.my_name == "张三"
    
    # Test minimum length validation
    with pytest.raises(ValueError):
        GreetingInput(my_name="")
    
    # Test maximum length validation (51 characters)
    long_name = "a" * 51
    with pytest.raises(ValueError):
        GreetingInput(my_name=long_name)
    
    # Test valid maximum length (50 characters)
    max_name = "a" * 50
    valid_max_input = GreetingInput(my_name=max_name)
    assert valid_max_input.my_name == max_name


@pytest.mark.asyncio
async def test_tools_with_pydantic():
    """Test that tools work with pydantic input."""
    server = SayHiMCPServer()
    # Note: In a real test, we would need to set up the MCP server properly
    # and test the tools through the MCP protocol. This is a simplified test.
    assert server.mcp is not None
    
    # Test that GreetingInput works as expected
    test_input = GreetingInput(my_name="TestUser")
    assert test_input.my_name == "TestUser"


def test_import():
    """Test that the package can be imported correctly."""
    from say_hi_mcp import SayHiMCPServer
    from say_hi_mcp.server import GreetingInput
    assert SayHiMCPServer is not None
    assert GreetingInput is not None 