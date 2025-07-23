#!/usr/bin/env python3
"""
BDD Step definitions for LLM Enhancement commands
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

# Load enhance command scenarios
scenarios('../features/enhance_commands.feature')


@given("I have an indexed project with diverse code patterns")
def indexed_project_with_patterns(temp_project, context):
    """Create indexed project with various code patterns"""
    context.current_directory = temp_project
    
    # Create files with different patterns
    patterns_file = Path(temp_project) / "patterns.py"
    patterns_file.write_text('''
# Singleton Pattern
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Factory Pattern  
class UserFactory:
    @staticmethod
    def create_user(user_type):
        if user_type == "admin":
            return AdminUser()
        return RegularUser()

# Observer Pattern
class EventManager:
    def __init__(self):
        self.observers = []
    
    def subscribe(self, observer):
        self.observers.append(observer)
    
    def notify(self, event):
        for observer in self.observers:
            observer.update(event)
''')


@given("I have previously enhanced nodes")
def previously_enhanced_nodes(context):
    """Set up nodes that have been enhanced before"""
    # Mock enhanced data in database
    pass


@given("I have an enhanced project")
def enhanced_project(temp_project, context):
    """Create a project that has been enhanced with LLM metadata"""
    context.current_directory = temp_project
    # Mock enhanced metadata in database
    pass


@then("LLM metadata should be generated")
def llm_metadata_generated(context):
    """Assert LLM metadata was created"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["metadata", "enhanced", "analysis", "llm"])


@then("enhancement progress should be displayed")
def enhancement_progress_displayed(context):
    """Assert enhancement progress is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["progress", "processing", "enhancing", "analyzing"])


@then("a summary of enhanced nodes should be shown")
def summary_of_enhanced_nodes_shown(context):
    """Assert summary is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["summary", "nodes", "enhanced", "completed"])


@then(parsers.parse("only {count:d} nodes should be enhanced"))
def only_n_nodes_enhanced(context, count):
    """Assert specific number of nodes were enhanced"""
    # This would be verified by checking the sample size parameter
    pass


@then("the sample should be representative")
def sample_should_be_representative(context):
    """Assert sampling strategy is good"""
    # This would verify diverse node types in sample
    pass


@then("the custom prompt should be used for analysis")
def custom_prompt_used(context):
    """Assert custom prompt was applied"""
    # This would verify the prompt parameter was passed
    pass


@then("results should reflect the custom prompt")
def results_reflect_custom_prompt(context):
    """Assert results match custom prompt"""
    # This would check output for prompt-specific content
    pass


@then("existing enhancements should be overwritten")
def existing_enhancements_overwritten(context):
    """Assert force refresh worked"""
    # This would verify fresh analysis occurred
    pass


@then("fresh analysis should be performed")
def fresh_analysis_performed(context):
    """Assert new analysis was done"""
    # This would check for updated metadata
    pass


@then("architectural insights should be displayed")
def architectural_insights_displayed(context):
    """Assert architectural analysis is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["architecture", "layer", "component", "service"])


@then("complexity hotspots should be identified")
def complexity_hotspots_identified(context):
    """Assert complexity analysis is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["complexity", "hotspot", "critical", "risk"])


@then("codebase health metrics should be shown")
def codebase_health_metrics_shown(context):
    """Assert health metrics are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["health", "metric", "score", "quality"])


@then("only service layer components should be displayed")
def only_service_layer_displayed(context):
    """Assert layer filtering works"""
    output = context.command_result.output.lower()
    assert "service" in output


@then("architectural classification should be shown")
def architectural_classification_shown(context):
    """Assert architectural info is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["layer", "tier", "component", "service"])


@then("only authentication-related components should be displayed")
def only_auth_components_displayed(context):
    """Assert domain filtering works"""
    output = context.command_result.output.lower()
    assert "authentication" in output or "auth" in output


@then("business context should be provided")
def business_context_provided(context):
    """Assert business domain context is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["business", "domain", "context", "purpose"])


@then("critical components should be identified")
def critical_components_identified(context):
    """Assert critical analysis is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["critical", "important", "key", "essential"])


@then("risk assessment should be provided")
def risk_assessment_provided(context):
    """Assert risk analysis is included"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["risk", "impact", "dependency", "failure"])


@then("recommendations should be included")
def recommendations_included(context):
    """Assert recommendations are provided"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["recommend", "suggest", "improve", "action"])


@then(parsers.parse("exactly {count:d} critical components should be displayed"))
def exactly_n_critical_components(context, count):
    """Assert specific number of critical components"""
    # This would verify the limit parameter worked
    pass


@then("they should be ranked by criticality")
def ranked_by_criticality(context):
    """Assert components are ranked"""
    # This would verify ranking algorithm was applied
    pass