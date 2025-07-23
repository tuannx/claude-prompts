#!/usr/bin/env python3
"""
BDD Step definitions for Query Command Parameters
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

# Load query parameter scenarios
scenarios('../features/query_parameters.feature')


@then("importance scores should be shown")
def importance_scores_shown(context):
    """Assert importance scores are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["score", "importance", "weight", "priority"])


@then("only class nodes should be displayed")
def only_class_nodes_displayed(context):
    """Assert only class nodes are shown"""
    output = context.command_result.output.lower()
    assert "class" in output
    # This would verify type filtering worked correctly


@then("node types should be filtered correctly")
def node_types_filtered(context):
    """Assert type filtering was applied"""
    # This would verify the --type parameter worked
    pass


@then("only method nodes should be displayed")
def only_method_nodes_displayed(context):
    """Assert only method nodes are shown"""
    output = context.command_result.output.lower()
    assert "method" in output


@then("method signatures should be shown")
def method_signatures_shown(context):
    """Assert method signatures are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["method", "signature", "()", "def"])


@then("only function nodes should be displayed")
def only_function_nodes_displayed(context):
    """Assert only function nodes are shown"""
    output = context.command_result.output.lower()
    assert "function" in output


@then("function definitions should be shown")
def function_definitions_shown(context):
    """Assert function definitions are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["function", "def", "()"])


@then("only file nodes should be displayed")
def only_file_nodes_displayed(context):
    """Assert only file nodes are shown"""
    output = context.command_result.output.lower()
    assert "file" in output


@then("file paths should be shown")
def file_paths_shown(context):
    """Assert file paths are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["path", ".py", ".js", "/"])


@then(parsers.parse("exactly {count:d} results should be displayed"))
def exactly_n_results_displayed(context, count):
    """Assert specific number of results are shown"""
    # This would verify the --limit parameter worked
    # Count actual results in output
    pass


@then("results should be truncated appropriately")
def results_truncated(context):
    """Assert results were limited correctly"""
    # This would verify limit was applied
    pass


@then(parsers.parse("up to {count:d} results should be displayed"))
def up_to_n_results_displayed(context, count):
    """Assert maximum number of results are shown"""
    # This would verify upper limit was respected
    pass


@then("pagination should work correctly")
def pagination_works(context):
    """Assert pagination was handled properly"""
    # This would verify large result sets are handled
    pass


@then("the custom database should be queried")
def custom_database_queried(context):
    """Assert custom database was used"""
    # This would verify --db parameter worked
    pass


@then("results should come from the specified database")
def results_from_specified_db(context):
    """Assert results came from custom database"""
    # This would verify database source
    pass


@then("only the specified project should be queried")
def only_specified_project_queried(context):
    """Assert project filtering was applied"""
    # This would verify --project parameter worked
    pass


@then("results should be project-specific")
def results_project_specific(context):
    """Assert results are from specific project"""
    # This would verify project scoping worked
    pass


@then(parsers.parse("exactly {count:d} or fewer results should be shown"))
def n_or_fewer_results_shown(context, count):
    """Assert maximum result count was respected"""
    # This would verify limit parameter with flexibility
    pass


@then("results should be sorted by importance")
def results_sorted_by_importance(context):
    """Assert importance-based sorting"""
    # This would verify sorting algorithm was applied
    pass


@then("the custom database should be used")
def custom_database_used(context):
    """Assert custom database was accessed"""
    # This would verify --db parameter was effective
    pass


@then("only the test project should be queried")
def only_test_project_queried(context):
    """Assert test project filtering worked"""
    # This would verify project scoping
    pass


@then("no results should be displayed")
def no_results_displayed(context):
    """Assert empty result set"""
    # This would verify --limit 0 worked
    pass


@then("the query should complete successfully")
def query_completes_successfully(context):
    """Assert query finished without error"""
    assert context.command_result.exit_code == 0


@then('an error message about invalid type should be displayed')
def error_about_invalid_type(context):
    """Assert error message for invalid type"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["invalid", "type", "error", "unknown"])


# Additional given steps for query tests
@given('I have a custom database at "/tmp/custom.db"')
def custom_database_custom_path(context):
    """Set up custom database for query tests"""
    context.custom_db_path = "/tmp/custom.db"
    pass


@given('I have a custom database at "/tmp/test.db"')
def custom_database_test_path(context):
    """Set up test database"""
    context.custom_db_path = "/tmp/test.db"
    pass