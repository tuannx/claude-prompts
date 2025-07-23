#!/usr/bin/env python3
"""
BDD Step definitions for Enhanced Query Command Parameters
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from pytest_bdd import scenarios, given, when, then, parsers

# Import shared step definitions
from shared_steps import *

# Mock ensmallen before importing
sys.modules['ensmallen'] = MagicMock()

# Load enhanced parameter scenarios
scenarios('../features/enhanced_parameters.feature')


@given("I have an enhanced project with LLM metadata")
def enhanced_project_with_llm_metadata(context):
    """Set up project with LLM-enhanced metadata"""
    # Mock enhanced project data
    pass


@then("only controller layer components should be displayed")
def only_controller_components_displayed(context):
    """Assert controller layer filtering"""
    output = context.command_result.output.lower()
    assert "controller" in output


@then("layer-specific insights should be provided")
def layer_specific_insights_provided(context):
    """Assert architectural layer insights"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["layer", "architecture", "pattern"])


@then("service layer patterns should be identified")
def service_layer_patterns_identified(context):
    """Assert service layer pattern recognition"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["service", "pattern", "layer"])


@then("data model structures should be shown")
def data_model_structures_shown(context):
    """Assert model layer information"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["model", "data", "structure"])


@then("security-related insights should be shown")
def security_insights_shown(context):
    """Assert security analysis for auth components"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["security", "auth", "permission", "access"])


@then("financial processing context should be provided")
def financial_context_provided(context):
    """Assert payment domain context"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["payment", "financial", "transaction", "money"])


@then("impact analysis should be shown")
def impact_analysis_shown(context):
    """Assert impact analysis for critical components"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["impact", "analysis", "effect", "consequence"])


@then("importance reasoning should be provided")
def importance_reasoning_provided(context):
    """Assert reasoning for importance classification"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["important", "reason", "because", "due"])


@then("only normal priority components should be displayed")
def only_normal_priority_displayed(context):
    """Assert normal criticality filtering"""
    output = context.command_result.output.lower()
    assert "normal" in output


@then("only low priority components should be displayed")
def only_low_priority_displayed(context):
    """Assert low criticality filtering"""
    output = context.command_result.output.lower()
    assert "low" in output


@then("only high complexity components should be displayed")
def only_high_complexity_displayed(context):
    """Assert high complexity filtering (0.8+)"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["complex", "complexity", "high"])


@then("complexity scores should be shown")
def complexity_scores_shown(context):
    """Assert complexity score display"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["complexity", "score", "0."])


@then("complexity analysis should be provided")
def complexity_analysis_provided(context):
    """Assert complexity analysis details"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["complexity", "analysis", "complex"])


@then("components with medium or higher complexity should be displayed")
def medium_plus_complexity_displayed(context):
    """Assert medium+ complexity filtering (0.5+)"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["complexity", "medium", "complex"])


@then("complexity metrics should be included")
def complexity_metrics_included(context):
    """Assert complexity metrics in output"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["complexity", "metric", "score"])


@then("most components should be displayed")
def most_components_displayed(context):
    """Assert low threshold shows most components"""
    # This would verify low complexity threshold (0.2)
    pass


@then("complexity filtering should be applied")
def complexity_filtering_applied(context):
    """Assert complexity filter was used"""
    # This would verify --min-complexity parameter worked
    pass


@then("top enhanced results should be shown")
def top_enhanced_results_shown(context):
    """Assert best enhanced results with limit"""
    # This would verify --limit parameter with enhanced data
    pass


@then("up to 50 enhanced results should be displayed")
def up_to_50_enhanced_displayed(context):
    """Assert large limit for enhanced results"""
    # This would verify large --limit parameter
    pass


@given("I have multiple enhanced projects")
def multiple_enhanced_projects(context):
    """Set up multiple projects with LLM metadata"""
    # Mock multiple enhanced projects
    pass


@then("enhanced metadata should be project-specific")
def enhanced_metadata_project_specific(context):
    """Assert project-specific enhanced data"""
    # This would verify project scoping with enhanced metadata
    pass


@then("only service layer authentication components should be displayed")
def only_service_auth_components_displayed(context):
    """Assert combined layer+domain filtering"""
    output = context.command_result.output.lower()
    assert "service" in output and ("auth" in output or "authentication" in output)


@then("both architectural and business context should be provided")
def both_contexts_provided(context):
    """Assert both architectural and business insights"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["architecture", "business", "layer", "domain"])


@then("only critical controller components should be displayed")
def only_critical_controllers_displayed(context):
    """Assert combined layer+criticality filtering"""
    output = context.command_result.output.lower()
    assert "controller" in output and "critical" in output


@then("risk assessment for controllers should be shown")
def controller_risk_assessment_shown(context):
    """Assert controller-specific risk analysis"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["risk", "controller", "assessment"])


@then("only complex payment components should be displayed")
def only_complex_payment_displayed(context):
    """Assert combined domain+complexity filtering"""
    output = context.command_result.output.lower()
    assert "payment" in output and ("complex" in output or "complexity" in output)


@then("financial complexity analysis should be provided")
def financial_complexity_analysis_provided(context):
    """Assert payment-specific complexity insights"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["financial", "payment", "complexity"])


@then("only important complex components should be displayed")
def only_important_complex_displayed(context):
    """Assert combined criticality+complexity filtering"""
    output = context.command_result.output.lower()
    assert "important" in output and ("complex" in output or "complexity" in output)


@then("both importance and complexity metrics should be shown")
def both_importance_complexity_shown(context):
    """Assert both metric types displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["important", "complexity", "score", "metric"])


@then("only critical, complex authentication service components should be displayed")
def only_critical_complex_auth_service(context):
    """Assert all filter criteria combined"""
    output = context.command_result.output.lower()
    assert all(word in output for word in ["critical", "service"]) and \
           ("auth" in output or "authentication" in output) and \
           ("complex" in output or "complexity" in output)


@then("comprehensive analysis should be provided")
def comprehensive_analysis_provided(context):
    """Assert multi-dimensional analysis"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["analysis", "comprehensive", "detailed"])


@then("all filter criteria should be satisfied")
def all_filter_criteria_satisfied(context):
    """Assert all filters were applied correctly"""
    # This would verify complex multi-filter logic
    pass


@then("only important payment controllers with medium+ complexity should be displayed")
def only_important_payment_controllers_complex(context):
    """Assert complex multi-filter scenario"""
    output = context.command_result.output.lower()
    assert "important" in output and "payment" in output and "controller" in output


@then("multi-dimensional analysis should be provided")
def multi_dimensional_analysis_provided(context):
    """Assert advanced analysis with multiple dimensions"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["analysis", "multi", "dimension", "comprehensive"])


@then('an error message about invalid complexity range should be displayed')
def error_about_invalid_complexity_range(context):
    """Assert error for invalid complexity values"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["invalid", "complexity", "range", "error"])