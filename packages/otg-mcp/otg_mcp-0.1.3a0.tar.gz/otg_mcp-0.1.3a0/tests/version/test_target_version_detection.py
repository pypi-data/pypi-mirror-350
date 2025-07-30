"""
Tests for automatic target API version detection and schema selection.

These tests verify that the client correctly uses the actual API version 
reported by a target device when available, falling back to the latest
available schema version when needed.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from otg_mcp.client import OtgClient
from otg_mcp.models import CapabilitiesVersionResponse


@pytest.fixture
def client():
    """Create a client instance for testing."""
    from otg_mcp.config import Config
    mock_config = Config()
    return OtgClient(config=mock_config)


@pytest.mark.asyncio
async def test_target_version_detection_uses_actual_version(client):
    """Test that client uses the actual target version when it has a matching schema."""
    # Setup mocks
    # Mock get_available_targets to return a target with a detected version
    client.get_available_targets = AsyncMock(return_value={
        "test-target": {
            "apiVersion": "1.30.0",  # Previously detected version (from device)
            "available": True,
            "ports": {}
        }
    })
    
    # Mock get_target_version to return a different version
    client.get_target_version = AsyncMock(return_value=CapabilitiesVersionResponse(
        api_spec_version="1.*",     # API spec version
        sdk_version="1.28.2",       # SDK version (now used for schema matching)
        app_version="1.0.0"
    ))
    
    # Mock schema_registry to indicate it has a schema for the actual version
    mock_registry = MagicMock()
    mock_registry.schema_exists.return_value = True  # Schema exists for 1_28_2
    
    # Replace the client's schema_registry with our mock
    client.schema_registry = mock_registry

    # Call _get_target_config with our test setup
    target_config = await client._get_target_config("test-target")
    
    # Verify that the API version was updated to the actual version
    assert target_config is not None
    assert target_config["apiVersion"] == "1.28.2"  # Should use actual version
    
    # Verify the schema registry was called correctly to check schema existence
    mock_registry.schema_exists.assert_called_with("1_28_2")


@pytest.mark.asyncio
async def test_target_version_detection_fallback_to_latest_version(client):
    """Test that client falls back to latest schema version when actual version has no schema."""
    # Setup mocks
    # Mock get_available_targets to return a target with a basic config
    client.get_available_targets = AsyncMock(return_value={
        "test-target": {
            "apiVersion": "unknown",  # Initial placeholder
            "available": True,
            "ports": {}
        }
    })
    
    # Mock get_target_version to return a version we don't have a schema for
    client.get_target_version = AsyncMock(return_value=CapabilitiesVersionResponse(
        api_spec_version="1.*",     # API spec version
        sdk_version="1.28.2",       # SDK version (now used for schema matching)
        app_version="1.0.0"
    ))
    
    # Mock schema_registry to indicate it does NOT have a schema for the actual version
    # but does have a latest version available
    mock_registry = MagicMock()
    mock_registry.schema_exists.return_value = False  # No schema for 1_28_2
    mock_registry.find_closest_schema_version.return_value = "1_30_0"  # Find closest schema version
    
    # Replace the client's schema_registry with our mock
    client.schema_registry = mock_registry

    # Call _get_target_config with our test setup
    target_config = await client._get_target_config("test-target")
    
    # Verify that the API version was updated to the closest matching schema version
    assert target_config is not None
    assert target_config["apiVersion"] == "1.30.0"  # Should use closest matching version (1_30_0 → 1.30.0)
    
    # Verify the schema registry was called correctly to check schema existence
    mock_registry.schema_exists.assert_called_with("1_28_2")
    mock_registry.find_closest_schema_version.assert_called_with("1_28_2")


@pytest.mark.asyncio
async def test_target_version_detection_handles_exceptions(client):
    """Test that client handles exceptions when getting target version."""
    # Setup mocks
    # Mock get_available_targets to return a target with minimal config
    client.get_available_targets = AsyncMock(return_value={
        "test-target": {
            "available": True,
            "ports": {}
        }
    })
    
    # Mock get_target_version to raise an exception
    client.get_target_version = AsyncMock(side_effect=Exception("Connection failed"))
    
    # Mock schema_registry to provide a latest version
    mock_registry = MagicMock()
    mock_registry.get_latest_schema_version.return_value = "1_30_0"

    # Replace the client's schema_registry with our mock
    client.schema_registry = mock_registry

    # Call _get_target_config - should not raise the exception and use the latest version
    target_config = await client._get_target_config("test-target")
    
    # Verify that the API version was set to the latest available version
    assert target_config is not None
    assert target_config["apiVersion"] == "1.30.0"  # Should use latest version (1_30_0 → 1.30.0)
    mock_registry.get_latest_schema_version.assert_called_once()
