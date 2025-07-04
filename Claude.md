# Claude Coding Assistant - Setup Rules

## Vibecode Mode (Fast Flow) 🚀
When user says "vibecode" or "!!!" or wants fast execution:
- **Skip confirmations** - Proceed directly without asking
- **Auto-planning** - Create todo and start immediately  
- **Silent execution** - Only report final results
- **Smart defaults** - Make reasonable choices autonomously
- **Batch reporting** - Summarize all changes at the end

!!! VIBECODE = NO ASK, JUST DO !!!
!!! USER TYPES "!!!" = VIBECODE MODE ON !!!

## Core Workflow Rules

1. **First think through the problem**, read the codebase for relevant files, and write a plan to `tasks/todo.md`.

2. **The plan should have a list of todo items** that you can check off as you complete them.

3. **Before you begin working**, check in with me and I will verify the plan. !!! SKIP IN VIBECODE !!!

4. **Then, begin working on the todo items**, marking them as complete as you go.

5. **Please every step of the way** just give me a high level explanation of what changes you made. !!! VIBECODE = SILENT !!!

6. **Make every task and code change you do as simple as possible**. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.

7. **Finally, add a review section** to the `todo.md` file with a summary of the changes you made and any other relevant information.

## Code Quality Principles

- **Use small files** to make changes easy
- **Trust the functionality of each file**
- **When debugging/testing, change only 1 file at a time**
- **Every change should be minimal and focused**
- **Prioritize simplicity over complexity**

## Session Management

- **Use Shift + Tab** to switch to Plan mode (prefer Opus 4 if available)
- **After completing a task**, use `/cancel` or start a new session for optimal performance and cost efficiency
- **Confirm before any code implementation** !!! VIBECODE = AUTO GO !!!

## Required Workflow Steps

1. **Planning Phase** → Use planning mode prompt
2. **Implementation Phase** → Follow todo checklist
3. **Security Check** → Run security validation prompt
4. **Learning Phase** → Use explanation prompt for knowledge transfer

## Task History Tracking
- **Create task file** in `tasks/YYYY/MM/` for each new request
- **Use template** from `tasks/templates/task-template.md`
- **Archive monthly** to keep workspace clean
- **Reference past tasks** for similar implementations
