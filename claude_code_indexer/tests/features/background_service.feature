Feature: Background Indexing Service
  As a developer using claude-code-indexer
  I want to run background indexing
  So that my projects stay up-to-date automatically

  Background:
    Given the background service is available

  Scenario: Start background service
    Given the background service is stopped
    When I run "claude-code-indexer background start"
    Then the command should succeed
    And the background service should be running
    And a confirmation message should be displayed

  Scenario: Stop background service
    Given the background service is running
    When I run "claude-code-indexer background stop"
    Then the command should succeed
    And the background service should be stopped
    And a confirmation message should be displayed

  Scenario: Restart background service
    Given the background service is running
    When I run "claude-code-indexer background restart"
    Then the command should succeed
    And the service should be restarted
    And existing processes should be terminated cleanly

  Scenario: Check background service status
    Given the background service is in any state
    When I run "claude-code-indexer background status"
    Then the command should succeed
    And the current service status should be displayed
    And monitored projects should be listed

  Scenario: Configure background service
    Given the background service is available
    When I run "claude-code-indexer background config --enable"
    Then the command should succeed
    And the service should be enabled
    And configuration should be saved

  Scenario: Disable background service
    Given the background service is enabled
    When I run "claude-code-indexer background config --disable"
    Then the command should succeed
    And the service should be disabled
    And no automatic indexing should occur

  Scenario: Set indexing interval for current project
    Given I am in a project directory
    When I run "claude-code-indexer background set-interval --interval 300"
    Then the command should succeed
    And the current project's interval should be set to 300 seconds
    And the setting should be persisted

  Scenario: Set global default interval
    When I run "claude-code-indexer background set-interval --interval 600"
    Then the command should succeed
    And the global default interval should be set to 600 seconds
    And new projects should use this interval