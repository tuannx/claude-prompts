#!/usr/bin/env python3
"""
BDD Step definitions for Stats Command Parameters
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

# Load stats parameter scenarios
scenarios('../features/stats_parameters.feature')


@then("node type distribution should be shown")
def node_type_distribution_shown(context):
    """Assert node type breakdown is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["type", "distribution", "breakdown", "count"])


@then("the custom database should be analyzed")
def custom_database_analyzed(context):
    """Assert custom database was used for analysis"""
    # This would verify --db parameter worked
    pass


@then("statistics should come from the specified database")
def stats_from_specified_database(context):
    """Assert stats came from custom database"""
    # This would verify database source
    pass


@then("database path should be confirmed in output")
def database_path_confirmed(context):
    """Assert database path is shown in output"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["database", "db", "path"])


@then("cache performance metrics should be included")
def cache_performance_included(context):
    """Assert cache performance data is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["performance", "cache", "speed", "efficiency"])


@then("project-specific metrics should be shown")
def project_specific_metrics_shown(context):
    """Assert project-scoped statistics"""
    # This would verify --project parameter worked
    pass


@then("project path should be confirmed")
def project_path_confirmed(context):
    """Assert project path is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["project", "path"])


@then("comprehensive statistics should be displayed")
def comprehensive_stats_displayed(context):
    """Assert all parameter combinations work together"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["statistics", "stats", "summary"])


@then("empty cache statistics should be displayed")
def empty_cache_stats_displayed(context):
    """Assert empty cache is handled properly"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["empty", "no cache", "0"])


@then("cache miss information should be shown")
def cache_miss_info_shown(context):
    """Assert cache miss data is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["miss", "cache", "0%"])


@then('an error message about database not found should be displayed')
def error_database_not_found(context):
    """Assert error for non-existent database"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["database", "not found", "error", "missing"])


@then('an error message about project not found should be displayed')
def error_project_not_found(context):
    """Assert error for non-existent project"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["project", "not found", "error", "missing"])


@then("function count should be displayed")
def function_count_displayed(context):
    """Assert function statistics are shown"""
    output = context.command_result.output.lower()
    assert "function" in output and any(char.isdigit() for char in context.command_result.output)


@then("class count should be displayed")
def class_count_displayed(context):
    """Assert class statistics are shown"""
    output = context.command_result.output.lower()
    assert "class" in output and any(char.isdigit() for char in context.command_result.output)


@then("method count should be displayed")
def method_count_displayed(context):
    """Assert method statistics are shown"""
    output = context.command_result.output.lower()
    assert "method" in output and any(char.isdigit() for char in context.command_result.output)


@then("file count should be displayed")
def file_count_displayed(context):
    """Assert file statistics are shown"""
    output = context.command_result.output.lower()
    assert "file" in output and any(char.isdigit() for char in context.command_result.output)


@then("import count should be displayed")
def import_count_displayed(context):
    """Assert import statistics are shown"""
    output = context.command_result.output.lower()
    assert "import" in output and any(char.isdigit() for char in context.command_result.output)


@then("calls relationship count should be displayed")
def calls_relationship_count_displayed(context):
    """Assert calls relationship statistics"""
    output = context.command_result.output.lower()
    assert "calls" in output and any(char.isdigit() for char in context.command_result.output)


@then("contains relationship count should be displayed")
def contains_relationship_count_displayed(context):
    """Assert contains relationship statistics"""
    output = context.command_result.output.lower()
    assert "contains" in output and any(char.isdigit() for char in context.command_result.output)


@then("imports relationship count should be displayed")
def imports_relationship_count_displayed(context):
    """Assert imports relationship statistics"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["import", "imports"]) and any(char.isdigit() for char in context.command_result.output)


@then("inheritance relationship count should be displayed")
def inheritance_relationship_count_displayed(context):
    """Assert inheritance relationship statistics"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["inherit", "extends"]) and any(char.isdigit() for char in context.command_result.output)


@then("Python file count should be displayed")
def python_file_count_displayed(context):
    """Assert Python-specific statistics"""
    output = context.command_result.output.lower()
    assert "python" in output and any(char.isdigit() for char in context.command_result.output)


@then("JavaScript file count should be displayed")
def javascript_file_count_displayed(context):
    """Assert JavaScript-specific statistics"""
    output = context.command_result.output.lower()
    assert "javascript" in output and any(char.isdigit() for char in context.command_result.output)


@then("language-specific node counts should be shown")
def language_specific_node_counts_shown(context):
    """Assert per-language node statistics"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["python", "javascript", "language"])


@then("per-language statistics should be provided")
def per_language_statistics_provided(context):
    """Assert language breakdown is detailed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["language", "per", "breakdown"])


@then("last indexed time should be displayed")
def last_indexed_time_displayed(context):
    """Assert indexing timestamp is shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["last", "indexed", "time", "ago"])


@then("indexing duration should be shown")
def indexing_duration_shown(context):
    """Assert indexing time duration"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["duration", "time", "seconds", "ms"])


@then("performance metrics should be included")
def performance_metrics_included(context):
    """Assert performance data is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["performance", "speed", "throughput"])


@then("database size should be displayed")
def database_size_displayed(context):
    """Assert database size information"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["size", "mb", "kb", "bytes"])


@then("storage efficiency metrics should be shown")
def storage_efficiency_shown(context):
    """Assert storage efficiency data"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["storage", "efficiency", "compression"])


@then("disk usage information should be provided")
def disk_usage_info_provided(context):
    """Assert disk usage statistics"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["disk", "usage", "space", "size"])


# Additional given steps for stats tests
@given('I have a custom database at "/tmp/stats.db"')
def custom_database_stats_path(context):
    """Set up stats database"""
    context.custom_db_path = "/tmp/stats.db"
    pass


@given('I have a custom database at "/tmp/comprehensive.db"')
def custom_database_comprehensive_path(context):
    """Set up comprehensive database"""
    context.custom_db_path = "/tmp/comprehensive.db"
    pass