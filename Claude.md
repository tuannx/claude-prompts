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
5. Minimal changes only
6. Close issue

## Principles
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