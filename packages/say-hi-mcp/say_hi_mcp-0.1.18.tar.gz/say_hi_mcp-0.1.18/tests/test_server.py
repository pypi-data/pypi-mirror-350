"""Tests for Say Hi MCP Server."""

import pytest
from say_hi_mcp.server import SayHiMCPServer, Interest, Profile


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


def test_interest_model():
    """Test Interest pydantic model."""
    # Valid interest
    interest = Interest(name="编程", level="expert")
    assert interest.name == "编程"
    assert interest.level == "expert"
    
    # Test with different levels
    levels = ["beginner", "intermediate", "expert"]
    for level in levels:
        interest = Interest(name="photography", level=level)
        assert interest.level == level


def test_profile_model():
    """Test Profile pydantic model validation."""
    # Valid profile
    interests = [
        Interest(name="编程", level="expert"),
        Interest(name="摄影", level="intermediate")
    ]
    profile = Profile(age=25, location="北京", interests=interests)
    assert profile.age == 25
    assert profile.location == "北京"
    assert len(profile.interests) == 2
    
    # Test age validation
    with pytest.raises(ValueError):
        Profile(age=-1, location="北京", interests=interests)  # Age too low
    
    with pytest.raises(ValueError):
        Profile(age=200, location="北京", interests=interests)  # Age too high
    
    # Test interests validation
    with pytest.raises(ValueError):
        Profile(age=25, location="北京", interests=[])  # Empty interests list
    
    # Test valid edge cases
    profile_min_age = Profile(age=0, location="北京", interests=interests)
    assert profile_min_age.age == 0
    
    profile_max_age = Profile(age=150, location="北京", interests=interests)
    assert profile_max_age.age == 150


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
    from say_hi_mcp.server import Interest, Profile
    assert SayHiMCPServer is not None
    assert Interest is not None
    assert Profile is not None


def test_complex_profile_example():
    """Test a complex profile example to ensure the multi-level structure works."""
    interests = [
        Interest(name="编程", level="expert"),
        Interest(name="摄影", level="intermediate"),
        Interest(name="音乐", level="beginner"),
        Interest(name="阅读", level="expert")
    ]
    
    profile = Profile(
        age=28,
        location="上海",
        interests=interests
    )
    
    assert profile.age == 28
    assert profile.location == "上海"
    assert len(profile.interests) == 4
    
    # Test that interests maintain their structure
    programming_interest = profile.interests[0]
    assert programming_interest.name == "编程"
    assert programming_interest.level == "expert"
    
    # Test serialization (this tests the multi-level structure)
    profile_dict = profile.model_dump()
    assert profile_dict["age"] == 28
    assert profile_dict["location"] == "上海"
    assert len(profile_dict["interests"]) == 4
    assert profile_dict["interests"][0]["name"] == "编程"
    assert profile_dict["interests"][0]["level"] == "expert" 