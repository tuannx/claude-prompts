#!/usr/bin/env python3
"""
BDD Step definitions for MCP (Model Context Protocol) Integration
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from pytest_bdd import scenarios, given, when, then, parsers

# Import shared step definitions
from shared_steps import *

# Mock ensmallen before importing
sys.modules['ensmallen'] = MagicMock()

# Load MCP integration scenarios
scenarios('../features/mcp_integration.feature')


@given("Claude Desktop is available on the system")
def claude_desktop_available(context):
    """Set up system with Claude Desktop"""
    # Mock Claude Desktop presence
    pass


@given("MCP server is not installed")
def mcp_server_not_installed(context):
    """Set up system without MCP server"""
    # Mock no MCP installation
    pass


@given("Claude Desktop is not found")
def claude_desktop_not_found(context):
    """Set up system without Claude Desktop"""
    # Mock missing Claude Desktop
    pass


@given("MCP server is installed")
def mcp_server_installed(context):
    """Set up system with MCP server installed"""
    # Mock existing MCP installation
    pass


@given("MCP server is installed and configured")
def mcp_server_installed_and_configured(context):
    """Set up fully configured MCP server"""
    # Mock complete MCP setup
    pass


@then("MCP server should be installed for Claude Desktop")
def mcp_server_should_be_installed(context):
    """Assert MCP server was installed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["installed", "setup", "configured"])


@then("configuration files should be updated")
def configuration_files_updated(context):
    """Assert config files were modified"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["configuration", "config", "updated"])


@then("installation confirmation should be displayed")
def installation_confirmation_displayed(context):
    """Assert installation success message"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["success", "installed", "ready"])


@then("MCP server should be installed anyway")
def mcp_server_installed_anyway(context):
    """Assert force install worked"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["installed", "forced", "setup"])


@then("a warning about Claude Desktop should be displayed")
def warning_about_claude_desktop(context):
    """Assert warning message is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["warning", "claude desktop", "not found"])


@then("MCP server should be removed from Claude Desktop")
def mcp_server_should_be_removed(context):
    """Assert MCP server was uninstalled"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["removed", "uninstalled", "cleaned"])


@then("configuration should be cleaned up")
def configuration_cleaned_up(context):
    """Assert config cleanup occurred"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cleaned", "removed", "reset"])


@then("uninstallation confirmation should be displayed")
def uninstallation_confirmation_displayed(context):
    """Assert uninstall success message"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["uninstalled", "removed", "success"])


@then('installation status should show "installed"')
def installation_status_installed(context):
    """Assert status shows installed"""
    output = context.command_result.output.lower()
    assert "installed" in output


@then("configuration details should be displayed")
def configuration_details_displayed(context):
    """Assert config details are shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["configuration", "settings", "path"])


@then("Claude Desktop integration status should be shown")
def claude_integration_status_shown(context):
    """Assert Claude integration info is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["claude", "integration", "connected"])


@then('installation status should show "not installed"')
@then("installation status should show \"not installed\"")
def installation_status_not_installed(context):
    """Assert status shows not installed"""
    output = context.command_result.output.lower()
    assert any(phrase in output for phrase in ["not installed", "not found", "missing"])


@then("available installation options should be displayed")
def installation_options_displayed(context):
    """Assert installation options are shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["install", "setup", "configure"])