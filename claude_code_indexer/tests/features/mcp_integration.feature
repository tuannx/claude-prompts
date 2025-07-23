Feature: MCP (Model Context Protocol) Integration
  As a developer using claude-code-indexer
  I want to integrate with Claude Desktop via MCP
  So that I can use indexing features directly in Claude

  Background:
    Given Claude Desktop is available on the system

  Scenario: Install MCP server
    Given MCP server is not installed
    When I run "claude-code-indexer mcp install"
    Then the command should succeed
    And MCP server should be installed for Claude Desktop
    And configuration files should be updated
    And installation confirmation should be displayed

  Scenario: Force install MCP server
    Given Claude Desktop is not found
    When I run "claude-code-indexer mcp install --force"
    Then the command should succeed
    And MCP server should be installed anyway
    And a warning about Claude Desktop should be displayed

  Scenario: Uninstall MCP server
    Given MCP server is installed
    When I run "claude-code-indexer mcp uninstall"
    Then the command should succeed
    And MCP server should be removed from Claude Desktop
    And configuration should be cleaned up
    And uninstallation confirmation should be displayed

  Scenario: Check MCP status when installed
    Given MCP server is installed and configured
    When I run "claude-code-indexer mcp status"
    Then the command should succeed
    And installation status should show "installed"
    And configuration details should be displayed
    And Claude Desktop integration status should be shown

  Scenario: Check MCP status when not installed
    Given MCP server is not installed
    When I run "claude-code-indexer mcp status"
    Then the command should succeed
    And installation status should show "not installed"
    And available installation options should be displayed