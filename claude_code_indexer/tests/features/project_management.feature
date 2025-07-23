Feature: Project Management Commands
  As a developer using claude-code-indexer
  I want to manage multiple projects
  So that I can organize and maintain my indexed codebases

  Background:
    Given I have multiple indexed projects

  Scenario: List all projects
    Given I have 3 indexed projects
    When I run "claude-code-indexer projects"
    Then the command should succeed
    And all 3 projects should be listed
    And project paths should be displayed
    And database sizes should be shown
    And last indexed times should be shown

  Scenario: List all projects including non-existent
    Given I have projects with some non-existent paths
    When I run "claude-code-indexer projects --all"
    Then the command should succeed
    And both existing and non-existent projects should be listed
    And status indicators should differentiate them

  Scenario: Remove a project
    Given I have a project at "/path/to/project"
    When I run "claude-code-indexer remove /path/to/project"
    And I confirm the removal
    Then the command should succeed
    And the project should be removed from storage
    And associated database should be deleted

  Scenario: Remove project with cancellation
    Given I have a project at "/path/to/project"
    When I run "claude-code-indexer remove /path/to/project"
    And I cancel the removal
    Then the command should succeed
    And the project should remain in storage
    And no data should be deleted

  Scenario: Clean current project
    Given I am in an indexed project directory
    When I run "claude-code-indexer clean"
    And I confirm the cleaning
    Then the command should succeed
    And the current project's database should be deleted
    And cache should be cleared

  Scenario: Sync CLAUDE.md with latest template
    Given I have an outdated CLAUDE.md file
    When I run "claude-code-indexer sync"
    Then the command should succeed
    And CLAUDE.md should be updated with latest template
    And existing custom content should be preserved