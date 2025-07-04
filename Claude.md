# Claude Coding Assistant - Setup Rules

## Core Workflow Rules

1. **First think through the problem**, read the codebase for relevant files, and write a plan to `tasks/todo.md`.

2. **The plan should have a list of todo items** that you can check off as you complete them.

3. **Before you begin working**, check in with me and I will verify the plan.

4. **Then, begin working on the todo items**, marking them as complete as you go.

5. **Please every step of the way** just give me a high level explanation of what changes you made.

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
- **Confirm before any code implementation**

## Required Workflow Steps

1. **Planning Phase** → Use planning mode prompt
2. **Implementation Phase** → Follow todo checklist
3. **Security Check** → Run security validation prompt
4. **Learning Phase** → Use explanation prompt for knowledge transfer