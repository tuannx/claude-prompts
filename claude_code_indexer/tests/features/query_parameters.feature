Feature: Query Command Parameters
  As a developer using claude-code-indexer
  I want to use various query parameters
  So that I can find specific code elements efficiently

  Background:
    Given I have an indexed project with 100 nodes

  Scenario: Query with important nodes filter
    When I run "claude-code-indexer query --important"
    Then the command should succeed
    And only important nodes should be displayed
    And nodes should be sorted by importance score
    And importance scores should be shown

  Scenario: Query with node type filter - classes
    When I run "claude-code-indexer query --type class"
    Then the command should succeed
    And only class nodes should be displayed
    And node types should be filtered correctly

  Scenario: Query with node type filter - methods
    When I run "claude-code-indexer query --type method"
    Then the command should succeed
    And only method nodes should be displayed
    And method signatures should be shown

  Scenario: Query with node type filter - functions
    When I run "claude-code-indexer query --type function"
    Then the command should succeed
    And only function nodes should be displayed
    And function definitions should be shown

  Scenario: Query with node type filter - files
    When I run "claude-code-indexer query --type file"
    Then the command should succeed
    And only file nodes should be displayed
    And file paths should be shown

  Scenario: Query with custom result limit
    When I run "claude-code-indexer query --limit 5"
    Then the command should succeed
    And exactly 5 results should be displayed
    And results should be truncated appropriately

  Scenario: Query with large result limit
    When I run "claude-code-indexer query --limit 50"
    Then the command should succeed
    And up to 50 results should be displayed
    And pagination should work correctly

  Scenario: Query with custom database path
    Given I have a custom database at "/tmp/custom.db"
    When I run "claude-code-indexer query --db /tmp/custom.db"
    Then the command should succeed
    And the custom database should be queried
    And results should come from the specified database

  Scenario: Query with project specification
    Given I have multiple indexed projects
    When I run "claude-code-indexer query --project /path/to/specific/project"
    Then the command should succeed
    And only the specified project should be queried
    And results should be project-specific

  Scenario: Query with combined filters - important classes
    When I run "claude-code-indexer query --important --type class --limit 10"
    Then the command should succeed
    And only important class nodes should be displayed
    And exactly 10 or fewer results should be shown
    And results should be sorted by importance

  Scenario: Query with all parameters combined
    Given I have a custom database at "/tmp/test.db"
    When I run "claude-code-indexer query --important --type method --limit 15 --db /tmp/test.db --project /test/project"
    Then the command should succeed
    And only important method nodes should be displayed
    And exactly 15 or fewer results should be shown
    And the custom database should be used
    And only the test project should be queried

  Scenario: Query with zero limit
    When I run "claude-code-indexer query --limit 0"
    Then the command should succeed
    And no results should be displayed
    And the query should complete successfully

  Scenario: Query with invalid node type
    When I run "claude-code-indexer query --type invalid_type"
    Then the command should fail
    And an error message about invalid type should be displayed