# Task Management System

## Structure
```
tasks/
├── README.md           # This file
├── 2025/              # Current year tasks
│   ├── 01/            # January
│   ├── 02/            # February
│   └── ...            # Other months
├── archive/           # Completed/old tasks
└── templates/         # Task templates
```

## File Naming Convention
- `YYYY-MM-DD-task-name.md` - Individual task files
- `YYYY-MM-DD-prompt-name.md` - Prompt history files
- `todo-active.md` - Current active todo list

## Task File Format
```markdown
# Task: [Task Name]
Date: YYYY-MM-DD
Status: pending|in_progress|completed
Tags: #feature #bugfix #refactor

## Original Prompt
[User's original request]

## Todo List
- [ ] Task item 1
- [ ] Task item 2

## Implementation Notes
[Notes during implementation]

## Changes Made
[List of files changed]

## Review
[Final review and outcomes]
```

## Usage
1. Create new task file when starting work
2. Copy prompt into "Original Prompt" section
3. Generate todo list
4. Track progress with checkboxes
5. Archive completed tasks monthly