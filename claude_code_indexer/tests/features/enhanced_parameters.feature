Feature: Enhanced Query Command Parameters
  As a developer using claude-code-indexer
  I want to use enhanced query parameters with LLM metadata
  So that I can find code elements using AI-powered insights

  Background:
    Given I have an enhanced project with LLM metadata

  Scenario: Enhanced query with architectural layer filter - controller
    When I run "claude-code-indexer enhanced . --layer controller"
    Then the command should succeed
    And only controller layer components should be displayed
    And architectural classification should be shown
    And layer-specific insights should be provided

  Scenario: Enhanced query with architectural layer filter - service
    When I run "claude-code-indexer enhanced . --layer service"
    Then the command should succeed
    And only service layer components should be displayed
    And service layer patterns should be identified

  Scenario: Enhanced query with architectural layer filter - model
    When I run "claude-code-indexer enhanced . --layer model"
    Then the command should succeed
    And only model layer components should be displayed
    And data model structures should be shown

  Scenario: Enhanced query with business domain filter - authentication
    When I run "claude-code-indexer enhanced . --domain authentication"
    Then the command should succeed
    And only authentication-related components should be displayed
    And business context should be provided
    And security-related insights should be shown

  Scenario: Enhanced query with business domain filter - payment
    When I run "claude-code-indexer enhanced . --domain payment"
    Then the command should succeed
    And only payment-related components should be displayed
    And financial processing context should be provided

  Scenario: Enhanced query with criticality filter - critical
    When I run "claude-code-indexer enhanced . --criticality critical"
    Then the command should succeed
    And only critical components should be displayed
    And risk assessment should be provided
    And impact analysis should be shown

  Scenario: Enhanced query with criticality filter - important
    When I run "claude-code-indexer enhanced . --criticality important"
    Then the command should succeed
    And only important components should be displayed
    And importance reasoning should be provided

  Scenario: Enhanced query with criticality filter - normal
    When I run "claude-code-indexer enhanced . --criticality normal"
    Then the command should succeed
    And only normal priority components should be displayed

  Scenario: Enhanced query with criticality filter - low
    When I run "claude-code-indexer enhanced . --criticality low"
    Then the command should succeed
    And only low priority components should be displayed

  Scenario: Enhanced query with minimum complexity filter - high
    When I run "claude-code-indexer enhanced . --min-complexity 0.8"
    Then the command should succeed
    And only high complexity components should be displayed
    And complexity scores should be shown
    And complexity analysis should be provided

  Scenario: Enhanced query with minimum complexity filter - medium
    When I run "claude-code-indexer enhanced . --min-complexity 0.5"
    Then the command should succeed
    And components with medium or higher complexity should be displayed
    And complexity metrics should be included

  Scenario: Enhanced query with minimum complexity filter - low threshold
    When I run "claude-code-indexer enhanced . --min-complexity 0.2"
    Then the command should succeed
    And most components should be displayed
    And complexity filtering should be applied

  Scenario: Enhanced query with custom result limit
    When I run "claude-code-indexer enhanced . --limit 5"
    Then the command should succeed
    And exactly 5 or fewer results should be displayed
    And top enhanced results should be shown

  Scenario: Enhanced query with large limit
    When I run "claude-code-indexer enhanced . --limit 50"  
    Then the command should succeed
    And up to 50 enhanced results should be displayed

  Scenario: Enhanced query with project specification
    Given I have multiple enhanced projects
    When I run "claude-code-indexer enhanced . --project /path/to/enhanced/project"
    Then the command should succeed
    And only the specified project should be queried
    And enhanced metadata should be project-specific

  Scenario: Enhanced query with layer and domain combination
    When I run "claude-code-indexer enhanced . --layer service --domain authentication"
    Then the command should succeed
    And only service layer authentication components should be displayed
    And both architectural and business context should be provided

  Scenario: Enhanced query with layer and criticality combination
    When I run "claude-code-indexer enhanced . --layer controller --criticality critical"
    Then the command should succeed
    And only critical controller components should be displayed
    And risk assessment for controllers should be shown

  Scenario: Enhanced query with domain and complexity combination
    When I run "claude-code-indexer enhanced . --domain payment --min-complexity 0.7"
    Then the command should succeed
    And only complex payment components should be displayed
    And financial complexity analysis should be provided

  Scenario: Enhanced query with criticality and complexity combination
    When I run "claude-code-indexer enhanced . --criticality important --min-complexity 0.6"
    Then the command should succeed
    And only important complex components should be displayed
    And both importance and complexity metrics should be shown

  Scenario: Enhanced query with all filters combined
    When I run "claude-code-indexer enhanced . --layer service --domain authentication --criticality critical --min-complexity 0.8 --limit 10"
    Then the command should succeed
    And only critical, complex authentication service components should be displayed
    And exactly 10 or fewer results should be shown
    And comprehensive analysis should be provided
    And all filter criteria should be satisfied

  Scenario: Enhanced query with project and all filters
    Given I have multiple enhanced projects
    When I run "claude-code-indexer enhanced . --layer controller --domain payment --criticality important --min-complexity 0.5 --limit 20 --project /test/project"
    Then the command should succeed
    And only important payment controllers with medium+ complexity should be displayed
    And exactly 20 or fewer results should be shown
    And only the test project should be queried
    And multi-dimensional analysis should be provided

  Scenario: Enhanced query with invalid complexity value - too high
    When I run "claude-code-indexer enhanced . --min-complexity 1.5"
    Then the command should fail
    And an error message about invalid complexity range should be displayed

  Scenario: Enhanced query with invalid complexity value - negative
    When I run "claude-code-indexer enhanced . --min-complexity -0.1"
    Then the command should fail
    And an error message about invalid complexity range should be displayed

  Scenario: Enhanced query with zero limit
    When I run "claude-code-indexer enhanced . --limit 0"
    Then the command should succeed
    And no results should be displayed
    And the query should complete successfully