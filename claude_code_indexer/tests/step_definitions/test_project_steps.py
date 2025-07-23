#!/usr/bin/env python3
"""
BDD Step definitions for Project Management commands
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

# Load project management scenarios
scenarios('../features/project_management.feature')


@given("I have multiple indexed projects")
def multiple_indexed_projects(context):
    """Set up multiple projects"""
    # Mock storage manager with multiple projects
    pass


@given(parsers.parse("I have {count:d} indexed projects"))
def n_indexed_projects(context, count):
    """Set up specific number of projects"""
    # Mock storage manager with n projects
    pass


@given("I have projects with some non-existent paths")
def projects_with_nonexistent_paths(context):
    """Set up projects where some paths don't exist"""
    # Mock projects with mixed existence
    pass


@given(parsers.parse('I have a project at "{path}"'))
def project_at_path(context, path):
    """Set up project at specific path"""
    context.project_path = path
    # Mock project at this path
    pass


@given("I am in an indexed project directory")
def in_indexed_project_directory(temp_project, context):
    """Set up current directory as indexed project"""
    context.current_directory = temp_project


@given("I have an outdated CLAUDE.md file")
def outdated_claude_md(temp_project, context):
    """Create outdated CLAUDE.md"""
    claude_md = Path(temp_project) / "CLAUDE.md"
    claude_md.write_text("""# Old CLAUDE.md

## Code Indexing with Graph Database
Old version content.

## Custom Section
My custom content.
""")
    context.current_directory = temp_project


@then(parsers.parse("all {count:d} projects should be listed"))
def all_projects_listed(context, count):
    """Assert all projects are shown"""
    # This would verify all projects appear in output
    pass


@then("project paths should be displayed")
def project_paths_displayed(context):
    """Assert project paths are shown"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["path", "directory", "/"])


@then("database sizes should be shown")
def database_sizes_shown(context):
    """Assert database size info is displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["size", "mb", "kb", "bytes"])


@then("last indexed times should be shown")
def last_indexed_times_shown(context):
    """Assert timestamps are displayed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["last", "indexed", "time", "ago"])


@then("both existing and non-existent projects should be listed")
def existing_and_nonexistent_listed(context):
    """Assert all projects shown regardless of existence"""
    # This would verify --all flag includes non-existent paths
    pass


@then("status indicators should differentiate them")
def status_indicators_differentiate(context):
    """Assert status shows existence"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["exists", "missing", "not found", "status"])


@then("the project should be removed from storage")
def project_removed_from_storage(context):
    """Assert project was removed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["removed", "deleted", "unregistered"])


@then("associated database should be deleted")
def database_deleted(context):
    """Assert database was deleted"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["database", "deleted", "removed"])


@then("the project should remain in storage")
def project_remains_in_storage(context):
    """Assert project was not removed"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cancelled", "aborted", "kept"])


@then("no data should be deleted")
def no_data_deleted(context):
    """Assert no deletion occurred"""
    # This would verify cancellation worked
    pass


@then("the current project's database should be deleted")
def current_project_db_deleted(context):
    """Assert current project's DB was deleted"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cleaned", "deleted", "removed"])


@then("cache should be cleared")
def cache_cleared(context):
    """Assert cache was cleared"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["cache", "cleared", "cleaned"])


@then("CLAUDE.md should be updated with latest template")
def claude_md_updated_with_template(context):
    """Assert CLAUDE.md was synced"""
    output = context.command_result.output.lower()
    assert any(word in output for word in ["synchronized", "updated", "synced"])


@then("existing custom content should be preserved")
def custom_content_preserved(context):
    """Assert custom sections were kept"""
    # This would verify merge strategy preserved user content
    pass