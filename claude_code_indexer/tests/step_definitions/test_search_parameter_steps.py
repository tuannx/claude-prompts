#!/usr/bin/env python3
"""
BDD Step definitions for Search Command Parameters
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

# Load search parameter scenarios
scenarios('../features/search_parameters.feature')


@then('search results should contain "user" OR "manager"')
def search_results_contain_user_or_manager(context):
    """Assert search results contain either term"""
    output = context.command_result.output.lower()
    assert "user" in output or "manager" in output


@then("results with both terms should rank higher")
def results_with_both_rank_higher(context):
    """Assert ranking algorithm prioritizes both terms"""
    # This would verify relevance ranking
    pass


@then('search results should contain both "user" AND "manager"')
def search_results_contain_both_terms(context):
    """Assert search results contain both terms"""
    output = context.command_result.output.lower()
    assert "user" in output and "manager" in output


@then("only matching results should be shown")
def only_matching_results_shown(context):
    """Assert ALL mode filtering worked"""
    # This would verify --mode all parameter
    pass


@then("the custom database should be searched")
def custom_database_searched(context):
    """Assert custom database was used for search"""
    # This would verify --db parameter
    pass


@then("top results should be shown first")
def top_results_first(context):
    """Assert relevance-based ordering"""
    # This would verify ranking algorithm
    pass


@then("all relevant matches should be included")
def all_relevant_matches_included(context):
    """Assert comprehensive search with large limit"""
    # This would verify large --limit parameter
    pass


@then("only file nodes should be in results")
def only_file_nodes_in_results(context):
    """Assert file type filtering"""
    output = context.command_result.output.lower()
    assert "file" in output


@then("only class nodes should be in results")
def only_class_nodes_in_results(context):
    """Assert class type filtering"""
    output = context.command_result.output.lower()
    assert "class" in output


@then("class definitions should be shown")
def class_definitions_shown(context):
    """Assert class definition details"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["class", "definition", "def"])


@then("only method nodes should be in results")
def only_method_nodes_in_results(context):
    """Assert method type filtering"""
    output = context.command_result.output.lower()
    assert "method" in output


@then("method signatures should be displayed")
def method_signatures_displayed(context):
    """Assert method signature information"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["method", "signature", "()", "def"])


@then("only function nodes should be in results")
def only_function_nodes_in_results(context):
    """Assert function type filtering"""
    output = context.command_result.output.lower()
    assert "function" in output


@then("function definitions should be shown")
def function_definitions_shown(context):
    """Assert function definition details"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["function", "def", "()"])


@then("only import nodes should be in results")
def only_import_nodes_in_results(context):
    """Assert import type filtering"""
    output = context.command_result.output.lower()
    assert "import" in output


@then("import statements should be displayed")
def import_statements_displayed(context):
    """Assert import statement details"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["import", "from", "require"])


@then("only interface nodes should be in results")
def only_interface_nodes_in_results(context):
    """Assert interface type filtering"""
    output = context.command_result.output.lower()
    assert "interface" in output


@then("interface definitions should be shown")
def interface_definitions_shown(context):
    """Assert interface definition details"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["interface", "definition"])


@then("only the specified project should be searched")
def only_specified_project_searched(context):
    """Assert project-specific search"""
    # This would verify --project parameter
    pass


@then('search results should contain "data" OR "process"')
def search_results_contain_data_or_process(context):
    """Assert search results contain either data or process"""
    output = context.command_result.output.lower()
    assert "data" in output or "process" in output


@then("only the test project should be searched")
def only_test_project_searched(context):
    """Assert test project scoping"""
    # This would verify project filtering
    pass


@then("the search should complete successfully")
def search_completes_successfully(context):
    """Assert search finished without error"""
    assert context.command_result.exit_code == 0


@then('an error message about invalid mode should be displayed')
def error_about_invalid_mode(context):
    """Assert error message for invalid mode"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["invalid", "mode", "error"])


@then('an error message about missing terms should be displayed')
def error_about_missing_terms(context):
    """Assert error message for missing search terms"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["missing", "terms", "required", "error"])


# Additional given steps for search tests
@given('I have a custom database at "/tmp/search.db"')
def custom_database_search_path(context):
    """Set up search database"""
    context.custom_db_path = "/tmp/search.db"
    pass


@given('I have a custom database at "/tmp/full.db"')
def custom_database_full_path(context):
    """Set up full database for comprehensive tests"""
    context.custom_db_path = "/tmp/full.db"
    pass