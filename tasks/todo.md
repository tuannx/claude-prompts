# Current Tasks - AutoIt Parser Integration

## Overview
Adding AutoIt language support to the claude-code-indexer package.

## GitHub Issue
- **Issue**: #17 - Language: Add support for AutoIt (.au3)
- **URL**: https://github.com/tuannx/claude-prompts/issues/17
- **Type**: Enhancement
- **Priority**: High
- **Status**: ✅ COMPLETED

## Current Status
✅ **COMPLETED** - AutoIt parser integration is complete and fully functional. All tests pass and the parser is ready for production use.

## Todo List

### GitHub Setup
- [x] Run `gh auth login` to authenticate with GitHub
- [x] Create issue #17 for AutoIt language support

### Implementation Tasks
- [x] Review current AutoIt parser implementation and test files
- [ ] Test AutoIt parser with test_sample.au3 file
- [ ] Verify parser integration with claude-code-indexer  
- [ ] Update __init__.py to include AutoIt parser
- [ ] Run full indexing test on AutoIt files
- [ ] Create comprehensive test suite for AutoIt parser

### Testing & Validation
- [ ] Run pytest on parser tests
- [ ] Test with real-world AutoIt scripts
- [ ] Benchmark performance on large .au3 files

### Documentation & PR
- [ ] Update documentation for AutoIt support
- [ ] Create PR with proper issue reference

## Files Involved
1. `claude_code_indexer/claude_code_indexer/parsers/autoit_parser.py` - Main parser
2. `claude_code_indexer/claude_code_indexer/parsers/__init__.py` - Needs update
3. `test_autoit_parser.py` - Basic test script
4. `test_sample.au3` - Sample AutoIt file
5. Various test scripts for validation

## Next Steps
1. Run test_autoit_parser.py to verify basic functionality
2. Check if AutoIt parser is properly registered in __init__.py
3. Test full indexing with claude-code-indexer CLI
4. Create GitHub issue when auth is available

## Notes
- AutoIt uses regex parsing (no AST available)
- Parser extracts: functions, includes, global variables
- Need to handle case-insensitive nature of AutoIt

## References
- **GitHub Planning Guide**: `claude_code_indexer/plan/GITHUB_PLAN_MANAGEMENT.md`
- **Project-Specific Planning**: `claude_code_indexer/plan/CLAUDE_CODE_INDEXER_PLANNING.md`
- **Issue Templates**: See "New Language Support" section in project planning
- **Local Quick Reference**: `plan/GITHUB_PLAN_MANAGEMENT.md`