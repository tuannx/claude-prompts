Feature: LLM Enhancement Commands
  As a developer using claude-code-indexer
  I want to use LLM enhancement features
  So that I can get AI-powered insights about my codebase

  Background:
    Given I have an indexed project with diverse code patterns

  Scenario: Enhance command with default parameters
    Given I have an indexed project
    When I run "claude-code-indexer enhance ."
    Then the command should succeed
    And LLM metadata should be generated
    And enhancement progress should be displayed
    And a summary of enhanced nodes should be shown

  Scenario: Enhance command with sample limit
    Given I have an indexed project with 100 nodes
    When I run "claude-code-indexer enhance . --limit 10"
    Then the command should succeed
    And only 10 nodes should be enhanced
    And the sample should be representative

  Scenario: Enhance command with force flag
    Given I have previously enhanced nodes
    When I run "claude-code-indexer enhance . --force"
    Then the command should succeed
    And existing enhancements should be overwritten
    And fresh analysis should be performed

  Scenario: Insights command
    Given I have an enhanced project
    When I run "claude-code-indexer insights ."
    Then the command should succeed
    And architectural insights should be displayed
    And complexity hotspots should be identified
    And codebase health metrics should be shown

  Scenario: Enhanced query by architectural layer
    Given I have an enhanced project
    When I run "claude-code-indexer enhanced . --layer service"
    Then the command should succeed
    And only service layer components should be displayed
    And architectural classification should be shown

  Scenario: Enhanced query by business domain
    Given I have an enhanced project
    When I run "claude-code-indexer enhanced . --domain authentication"
    Then the command should succeed
    And only authentication-related components should be displayed
    And business context should be provided

  Scenario: Critical components analysis
    Given I have an enhanced project
    When I run "claude-code-indexer critical ."
    Then the command should succeed
    And critical components should be identified
    And risk assessment should be provided
    And recommendations should be included

  Scenario: Critical components with custom limit
    Given I have an enhanced project
    When I run "claude-code-indexer critical . --limit 5"
    Then the command should succeed
    And exactly 5 critical components should be displayed
    And they should be ranked by criticality