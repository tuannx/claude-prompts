Feature: Stats Command Parameters
  As a developer using claude-code-indexer  
  I want to use various stats parameters
  So that I can get detailed statistics about my indexed codebase

  Background:
    Given I have an indexed project with cached data

  Scenario: Basic stats without parameters
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And statistics should include total nodes count
    And statistics should include total edges count
    And language breakdown should be displayed
    And node type distribution should be shown

  Scenario: Stats with custom database path
    Given I have a custom database at "/tmp/stats.db"
    When I run "claude-code-indexer stats --db /tmp/stats.db"
    Then the command should succeed
    And the custom database should be analyzed
    And statistics should come from the specified database
    And database path should be confirmed in output

  Scenario: Stats with cache information enabled
    When I run "claude-code-indexer stats --cache"
    Then the command should succeed
    And cache hit rate should be displayed
    And cache size information should be shown
    And cache entry count should be displayed
    And cache performance metrics should be included

  Scenario: Stats with project specification
    Given I have multiple indexed projects
    When I run "claude-code-indexer stats --project /path/to/project1"
    Then the command should succeed
    And only the specified project stats should be displayed
    And project-specific metrics should be shown
    And project path should be confirmed

  Scenario: Stats with all parameters combined
    Given I have a custom database at "/tmp/comprehensive.db"
    And I have multiple indexed projects
    When I run "claude-code-indexer stats --db /tmp/comprehensive.db --cache --project /test/project"
    Then the command should succeed
    And the custom database should be analyzed
    And cache statistics should be included
    And only the test project should be analyzed
    And comprehensive statistics should be displayed

  Scenario: Stats with cache but no cached data
    Given I have a project with no cache data
    When I run "claude-code-indexer stats --cache"
    Then the command should succeed
    And empty cache statistics should be displayed
    And cache miss information should be shown

  Scenario: Stats with non-existent database path
    When I run "claude-code-indexer stats --db /non/existent/path.db"
    Then the command should fail
    And an error message about database not found should be displayed

  Scenario: Stats with non-existent project
    When I run "claude-code-indexer stats --project /non/existent/project"
    Then the command should fail
    And an error message about project not found should be displayed

  Scenario: Stats showing detailed node type breakdown
    Given I have an indexed project with diverse node types
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And function count should be displayed
    And class count should be displayed
    And method count should be displayed
    And file count should be displayed
    And import count should be displayed

  Scenario: Stats showing relationship type breakdown
    Given I have an indexed project with relationships
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And calls relationship count should be displayed
    And contains relationship count should be displayed
    And imports relationship count should be displayed
    And inheritance relationship count should be displayed

  Scenario: Stats showing language-specific metrics
    Given I have an indexed project with Python and JavaScript files
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And Python file count should be displayed
    And JavaScript file count should be displayed
    And language-specific node counts should be shown
    And per-language statistics should be provided

  Scenario: Stats with timing information
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And last indexed time should be displayed
    And indexing duration should be shown
    And performance metrics should be included

  Scenario: Stats with storage information
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And database size should be displayed
    And storage efficiency metrics should be shown
    And disk usage information should be provided