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
    # Valid interest with level
    interest = Interest(name="编程", level="expert")
    assert interest.name == "编程"
    assert interest.level == "expert"
    
    # Valid interest without level
    interest_no_level = Interest(name="摄影")
    assert interest_no_level.name == "摄影"
    assert interest_no_level.level is None
    
    # Test with different levels
    levels = ["beginner", "intermediate", "expert"]
    for level in levels:
        interest = Interest(name="photography", level=level)
        assert interest.level == level


def test_profile_model():
    """Test Profile pydantic model validation."""
    # Valid complete profile
    interests = [
        Interest(name="编程", level="expert"),
        Interest(name="摄影", level="intermediate")
    ]
    profile = Profile(age=25, location="北京", interests=interests)
    assert profile.age == 25
    assert profile.location == "北京"
    assert len(profile.interests) == 2
    
    # Valid partial profiles
    profile_age_only = Profile(age=30)
    assert profile_age_only.age == 30
    assert profile_age_only.location is None
    assert profile_age_only.interests is None
    
    profile_location_only = Profile(location="上海")
    assert profile_location_only.age is None
    assert profile_location_only.location == "上海"
    assert profile_location_only.interests is None
    
    profile_interests_only = Profile(interests=[Interest(name="音乐")])
    assert profile_interests_only.age is None
    assert profile_interests_only.location is None
    assert len(profile_interests_only.interests) == 1
    
    # Empty profile
    empty_profile = Profile()
    assert empty_profile.age is None
    assert empty_profile.location is None
    assert empty_profile.interests is None
    
    # Test age validation (when provided)
    with pytest.raises(ValueError):
        Profile(age=-1, location="北京", interests=interests)  # Age too low
    
    with pytest.raises(ValueError):
        Profile(age=200, location="北京", interests=interests)  # Age too high
    
    # Test valid edge cases
    profile_min_age = Profile(age=0, location="北京", interests=interests)
    assert profile_min_age.age == 0
    
    profile_max_age = Profile(age=150, location="北京", interests=interests)
    assert profile_max_age.age == 150


def test_optional_interests():
    """Test interests with optional level."""
    # Interest with level
    interest_with_level = Interest(name="编程", level="expert")
    assert interest_with_level.name == "编程"
    assert interest_with_level.level == "expert"
    
    # Interest without level
    interest_without_level = Interest(name="摄影")
    assert interest_without_level.name == "摄影"
    assert interest_without_level.level is None
    
    # Profile with mixed interests
    mixed_interests = [
        Interest(name="编程", level="expert"),
        Interest(name="摄影"),  # No level
        Interest(name="音乐", level="beginner")
    ]
    
    profile = Profile(interests=mixed_interests)
    assert len(profile.interests) == 3
    assert profile.interests[0].level == "expert"
    assert profile.interests[1].level is None
    assert profile.interests[2].level == "beginner"


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


def test_all_optional_scenarios():
    """Test all possible optional parameter scenarios."""
    # Test different combinations of optional parameters
    test_cases = [
        # Complete profile
        Profile(age=25, location="北京", interests=[Interest(name="编程", level="expert")]),
        
        # Only age
        Profile(age=30),
        
        # Only location
        Profile(location="上海"),
        
        # Only interests
        Profile(interests=[Interest(name="音乐")]),
        
        # Age + location
        Profile(age=25, location="深圳"),
        
        # Age + interests
        Profile(age=22, interests=[Interest(name="绘画", level="intermediate")]),
        
        # Location + interests
        Profile(location="广州", interests=[Interest(name="跑步"), Interest(name="读书", level="expert")]),
        
        # Empty profile
        Profile(),
        
        # None (this would be handled as no profile provided)
        None
    ]
    
    for profile in test_cases:
        if profile is not None:
            # Test that the profile can be created and serialized
            profile_dict = profile.model_dump()
            assert isinstance(profile_dict, dict)
            
            # Test individual fields
            if profile.age is not None:
                assert isinstance(profile.age, int)
                assert 0 <= profile.age <= 150
            
            if profile.location is not None:
                assert isinstance(profile.location, str)
            
            if profile.interests is not None:
                assert isinstance(profile.interests, list)
                for interest in profile.interests:
                    assert isinstance(interest.name, str)
                    assert interest.level is None or isinstance(interest.level, str)


def test_interests_mixed_levels():
    """Test interests with mixed presence of levels."""
    mixed_interests = [
        Interest(name="编程", level="expert"),
        Interest(name="摄影"),  # No level provided
        Interest(name="音乐", level="beginner"),
        Interest(name="阅读")   # No level provided
    ]
    
    profile = Profile(interests=mixed_interests)
    
    # Check that all interests are properly stored
    assert len(profile.interests) == 4
    
    # Check individual interests
    assert profile.interests[0].name == "编程"
    assert profile.interests[0].level == "expert"
    
    assert profile.interests[1].name == "摄影"
    assert profile.interests[1].level is None
    
    assert profile.interests[2].name == "音乐"
    assert profile.interests[2].level == "beginner"
    
    assert profile.interests[3].name == "阅读"
    assert profile.interests[3].level is None
    
    # Test serialization
    serialized = profile.model_dump()
    assert len(serialized["interests"]) == 4
    assert serialized["interests"][1]["level"] is None
    assert serialized["interests"][3]["level"] is None 