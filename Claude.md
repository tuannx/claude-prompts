# Claude Rules

## Vibecode Mode 🚀
`!!!` or `vibecode` = NO ASK, JUST DO

## GitHub First
```bash
gh issue list --assignee @me --state open
gh issue create --title "Task: ..." --label "task"
gh issue close <number> --comment "Done"
```

## Workflow
1. Check GitHub issues
2. Plan → issue comments
3. Verify plan (SKIP if !!!)
4. Execute & update issue
5. **TEST AFTER CHANGES**: Run tests & update test cases
6. Minimal changes only
7. Close issue

## Testing Protocol 🧪
After EVERY code change:
1. Run relevant tests: `pytest tests/test_file.py -v`
2. Update test cases if behavior changed
3. Add new tests for new features
4. Fix any test failures before proceeding
5. Run full test suite before major commits

## Principles
- **SEARCH FIRST**: Always search before adding/deleting
- **TEST ALWAYS**: Run tests after every change
- Small files
- One file at a time
- Minimal changes
- Simple > complex

## Claude Code Indexer
```bash
pip install claude-code-indexer
claude-code-indexer init
claude-code-indexer index .
claude-code-indexer query --important
```

## Keywords
- `!!!` = vibecode on
- `/cancel` = new session
- `Shift+Tab` = plan mode
- `gh issue` = task tracking