Feature: Search Command Parameters
  As a developer using claude-code-indexer
  I want to use various search parameters
  So that I can find code elements using different search strategies

  Background:
    Given I have an indexed project with diverse code patterns

  Scenario: Search with single term
    When I run "claude-code-indexer search calculate"
    Then the command should succeed
    And search results should contain "calculate"
    And results should be ranked by relevance

  Scenario: Search with multiple terms - ANY mode (default)
    When I run "claude-code-indexer search user manager"
    Then the command should succeed
    And search results should contain "user" OR "manager"
    And results with both terms should rank higher

  Scenario: Search with multiple terms - ALL mode
    When I run "claude-code-indexer search user manager --mode all"
    Then the command should succeed
    And search results should contain both "user" AND "manager"
    And only matching results should be shown

  Scenario: Search with custom database path
    Given I have a custom database at "/tmp/search.db"
    When I run "claude-code-indexer search function --db /tmp/search.db"
    Then the command should succeed
    And the custom database should be searched
    And results should come from the specified database

  Scenario: Search with result limit
    When I run "claude-code-indexer search class --limit 5"
    Then the command should succeed
    And exactly 5 or fewer results should be displayed
    And top results should be shown first

  Scenario: Search with large limit
    When I run "claude-code-indexer search method --limit 100"
    Then the command should succeed
    And up to 100 results should be displayed
    And all relevant matches should be included

  Scenario: Search filtered by file type
    When I run "claude-code-indexer search main --type file"
    Then the command should succeed
    And only file nodes should be in results
    And file paths should be displayed

  Scenario: Search filtered by class type
    When I run "claude-code-indexer search Manager --type class"
    Then the command should succeed
    And only class nodes should be in results
    And class definitions should be shown

  Scenario: Search filtered by method type
    When I run "claude-code-indexer search get --type method"
    Then the command should succeed
    And only method nodes should be in results
    And method signatures should be displayed

  Scenario: Search filtered by function type
    When I run "claude-code-indexer search process --type function"
    Then the command should succeed
    And only function nodes should be in results
    And function definitions should be shown

  Scenario: Search filtered by import type
    When I run "claude-code-indexer search json --type import"
    Then the command should succeed
    And only import nodes should be in results
    And import statements should be displayed

  Scenario: Search filtered by interface type
    When I run "claude-code-indexer search API --type interface"
    Then the command should succeed
    And only interface nodes should be in results
    And interface definitions should be shown

  Scenario: Search with project specification
    Given I have multiple indexed projects
    When I run "claude-code-indexer search utils --project /path/to/project1"
    Then the command should succeed
    And only the specified project should be searched
    And results should be project-specific

  Scenario: Search with all parameters - ANY mode
    Given I have a custom database at "/tmp/full.db"
    When I run "claude-code-indexer search data process --mode any --limit 10 --type function --db /tmp/full.db --project /test/project"
    Then the command should succeed
    And search results should contain "data" OR "process"
    And only function nodes should be in results
    And exactly 10 or fewer results should be displayed
    And the custom database should be used
    And only the test project should be searched

  Scenario: Search with all parameters - ALL mode
    Given I have a custom database at "/tmp/full.db"
    When I run "claude-code-indexer search user manager --mode all --limit 15 --type class --db /tmp/full.db --project /test/project"
    Then the command should succeed
    And search results should contain both "user" AND "manager"
    And only class nodes should be in results
    And exactly 15 or fewer results should be displayed
    And the custom database should be used
    And only the test project should be searched

  Scenario: Search with zero limit
    When I run "claude-code-indexer search test --limit 0"
    Then the command should succeed
    And no results should be displayed
    And the search should complete successfully

  Scenario: Search with invalid type filter
    When I run "claude-code-indexer search test --type invalid_type"
    Then the command should fail
    And an error message about invalid type should be displayed

  Scenario: Search with invalid mode
    When I run "claude-code-indexer search test --mode invalid_mode"
    Then the command should fail
    And an error message about invalid mode should be displayed

  Scenario: Search with empty terms
    When I run "claude-code-indexer search"
    Then the command should fail
    And an error message about missing terms should be displayed