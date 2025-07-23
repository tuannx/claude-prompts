Feature: Index Command Parameters
  As a developer using claude-code-indexer
  I want to use various indexing parameters
  So that I can customize the indexing process for my needs

  Background:
    Given I have a sample project with Python and JavaScript files

  Scenario: Index with custom file patterns
    When I run "claude-code-indexer index . --patterns *.py,*.js"
    Then the command should succeed
    And only Python and JavaScript files should be processed
    And the patterns should be applied correctly

  Scenario: Index with specific database path
    When I run "claude-code-indexer index . --db /tmp/custom.db"
    Then the command should succeed
    And the database should be created at the specified path
    And indexing data should be stored in the custom database

  Scenario: Index with cache disabled
    When I run "claude-code-indexer index . --no-cache"
    Then the command should succeed
    And caching should be disabled
    And all files should be processed fresh

  Scenario: Index with force re-indexing
    Given I have previously indexed files
    When I run "claude-code-indexer index . --force"
    Then the command should succeed
    And existing cache should be ignored
    And all files should be re-processed

  Scenario: Index with custom worker count
    When I run "claude-code-indexer index . --workers 4"
    Then the command should succeed
    And parallel processing should use 4 workers
    And processing should be parallelized

  Scenario: Index with database optimizations disabled
    When I run "claude-code-indexer index . --no-optimize"
    Then the command should succeed
    And database optimizations should be skipped
    And raw indexing data should be preserved

  Scenario: Index with benchmark mode
    When I run "claude-code-indexer index . --benchmark"
    Then the command should succeed
    And performance metrics should be collected
    And benchmark results should be displayed

  Scenario: Index with custom ignore patterns
    When I run "claude-code-indexer index . --custom-ignore *.test.py --custom-ignore *.spec.js"
    Then the command should succeed
    And test files should be ignored
    And specification files should be ignored
    And custom ignore patterns should be applied

  Scenario: Index with show ignored files
    When I run "claude-code-indexer index . --show-ignored"
    Then the command should succeed
    And ignored file patterns should be displayed
    And ignored files list should be shown

  Scenario: Index with verbose output
    When I run "claude-code-indexer index . --verbose"
    Then the command should succeed
    And detailed processing information should be displayed
    And I should see file-by-file progress
    And parsing errors should be shown if any

  Scenario: Index with multiple parameters combined
    When I run "claude-code-indexer index . --patterns *.py --workers 2 --verbose --force"
    Then the command should succeed
    And only Python files should be processed
    And parallel processing should use 2 workers
    And detailed processing information should be displayed
    And all files should be re-processed

  Scenario: Index with all ignore-related parameters
    When I run "claude-code-indexer index . --custom-ignore *.tmp --custom-ignore build/ --show-ignored"
    Then the command should succeed
    And temporary files should be ignored
    And build directory should be ignored
    And ignored patterns should be displayed
    And the ignore list should include custom patterns