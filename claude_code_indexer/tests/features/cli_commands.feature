Feature: CLI Commands
  As a developer using claude-code-indexer
  I want to use CLI commands to manage code indexing
  So that I can efficiently index and query my codebase

  Background:
    Given I have a sample project with Python and JavaScript files

  Scenario: Init command with default behavior
    Given I am in an empty project directory
    When I run "claude-code-indexer init"
    Then the command should succeed
    And a CLAUDE.md file should be created
    And the file should contain "Code Indexing with Graph Database"

  Scenario: Init command with force flag
    Given I have an existing CLAUDE.md file
    When I run "claude-code-indexer init --force"
    Then the command should succeed
    And the CLAUDE.md file should be updated
    And the file should contain the latest template

  Scenario: Index command with default parameters
    Given I have a project with Python files
    When I run "claude-code-indexer index ."
    Then the command should succeed
    And files should be indexed in the database
    And the indexing stats should be displayed

  Scenario: Index command with verbose flag
    Given I have a project with Python files
    When I run "claude-code-indexer index . --verbose"
    Then the command should succeed
    And detailed processing information should be displayed
    And I should see file-by-file progress

  Scenario: Index command with no-cache flag
    Given I have a project with Python files
    When I run "claude-code-indexer index . --no-cache"
    Then the command should succeed
    And caching should be disabled
    And all files should be processed fresh

  Scenario: Index command with custom workers
    Given I have a project with Python files
    When I run "claude-code-indexer index . --workers 4"
    Then the command should succeed
    And parallel processing should use 4 workers

  Scenario: Index command with invalid worker count
    Given I have a project with Python files
    When I run "claude-code-indexer index . --workers 0"
    Then the command should fail
    And an error message about invalid worker count should be displayed

  Scenario: Query command without flags
    Given I have an indexed project
    When I run "claude-code-indexer query"
    Then the command should succeed
    And all nodes should be displayed
    And the output should be formatted nicely

  Scenario: Query command with important flag
    Given I have an indexed project
    When I run "claude-code-indexer query --important"
    Then the command should succeed
    And only important nodes should be displayed
    And nodes should be sorted by importance score

  Scenario: Search command with single term
    Given I have an indexed project
    When I run "claude-code-indexer search function"
    Then the command should succeed
    And search results should contain "function"
    And results should be ranked by relevance

  Scenario: Search command with multiple terms
    Given I have an indexed project
    When I run "claude-code-indexer search class method"
    Then the command should succeed
    And search results should contain both "class" and "method"

  Scenario: Stats command
    Given I have an indexed project
    When I run "claude-code-indexer stats"
    Then the command should succeed
    And statistics should include total nodes count
    And statistics should include total edges count
    And language breakdown should be displayed

  Scenario: Version command
    When I run "claude-code-indexer --version"
    Then the command should succeed
    And the version number should be displayed
    And the application name should be displayed

  Scenario: Help command
    When I run "claude-code-indexer --help"
    Then the command should succeed
    And usage information should be displayed
    And all available commands should be listed

  Scenario: LLM Guide command
    When I run "claude-code-indexer llm-guide"
    Then the command should succeed
    And LLM usage guide should be displayed
    And security warnings should be included
    And quick start instructions should be shown