# GitHub Plan Management - Quick Reference

This is a quick reference. For comprehensive guides, see:
- **General Guide**: `claude_code_indexer/plan/GITHUB_PLAN_MANAGEMENT.md`
- **Project-Specific**: `claude_code_indexer/plan/CLAUDE_CODE_INDEXER_PLANNING.md`

## Current Work: AutoIt Parser Integration

### GitHub Issue #17
- **Created**: https://github.com/tuannx/claude-prompts/issues/17
- **Status**: In Progress
- **Label**: enhancement

### Progress Tracking
```bash
# View issue details
gh issue view 17

# Add progress update
gh issue comment 17 --body "Progress: [description]"

# Close when complete
gh issue close 17 --comment "Completed: AutoIt parser integrated and tested"
```

### Local Task Tracking
See: `tasks/2025/01/autoit-parser-integration.md`

## Quick Commands
```bash
# Setup GitHub auth
gh auth login

# Check issues
gh issue list --state open

# Create AutoIt issue
gh issue create --title "Language: Add support for AutoIt"
```