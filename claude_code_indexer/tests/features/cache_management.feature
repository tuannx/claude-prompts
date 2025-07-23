Feature: Cache Management Commands
  As a developer using claude-code-indexer
  I want to manage cache efficiently
  So that I can optimize performance and storage

  Background:
    Given I have a project with cached data

  Scenario: Cache stats command
    Given I have cached indexing data
    When I run "claude-code-indexer cache"
    Then the command should succeed
    And cache hit rate should be displayed
    And cache size information should be shown
    And cache entry count should be displayed

  Scenario: Cache clear command
    Given I have old cached data
    When I run "claude-code-indexer cache --clear"
    Then the command should succeed
    And old cache entries should be removed
    And current cache should be preserved
    And storage space should be reclaimed

  Scenario: Cache clear with specific age
    Given I have cached data of various ages
    When I run "claude-code-indexer cache --clear --days 7"
    Then the command should succeed
    And old cache entries should be removed
    And current cache should be preserved
    And storage space should be reclaimed