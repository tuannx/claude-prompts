# GitHub-based Project Planning Template

## 🎯 Overview
Use GitHub Issues, Projects, and CLI (gh) as a comprehensive planning and tracking system for any project.

## 📋 GitHub Issues as Tasks

### Creating Issues with gh CLI
```bash
# Create high-priority bug
gh issue create --title "Fix [Component] issue" \
  --body "Detailed description of the problem" \
  --label "bug,high-priority" \
  --milestone "v1.0"

# Create feature request
gh issue create --title "Add [Feature Name]" \
  --body "Feature description and requirements" \
  --label "feature,enhancement" \
  --assignee @me

# Create task with checklist
gh issue create --title "[Task Description]" \
  --body "- [ ] Step 1
- [ ] Step 2  
- [ ] Step 3
- [ ] Document changes" \
  --label "task"
```

### Issue Labels System
```bash
# Priority levels
high-priority    # Must fix immediately
medium-priority  # Important but not blocking
low-priority     # Nice to have

# Issue types
bug             # Something broken
feature         # New functionality
enhancement     # Improvement to existing feature
task            # Operational work
documentation   # Docs updates
refactor        # Code improvements
test            # Test additions/fixes

# Status indicators
blocked         # Waiting on something
in-progress     # Currently being worked on
needs-review    # Ready for review
```

## 🗂️ GitHub Projects for Sprint Planning

### Create Project Board
```bash
# Create new project
gh project create "[Project Name] Sprint X" \
  --owner [USERNAME/ORG] \
  --description "Sprint goals and tasks"

# Add columns (if using classic projects)
gh project field-create "Status" \
  --owner [USERNAME/ORG] \
  --project "[Project Name] Sprint X" \
  --single-select-options "Backlog,In Progress,Review,Done"
```

### Link Issues to Project
```bash
# Add issue to project
gh project item-add [ISSUE_NUMBER] \
  --owner [USERNAME/ORG] \
  --project "[Project Name] Sprint X"

# Update issue status
gh project item-edit \
  --owner [USERNAME/ORG] \
  --project "[Project Name] Sprint X" \
  --id [ITEM_ID] \
  --field-id [STATUS_FIELD_ID] \
  --single-select-option-id "In Progress"
```

## 📊 Tracking Progress

### Daily Status Check
```bash
# View open issues by priority
gh issue list --label "high-priority" --state open

# View my assigned issues
gh issue list --assignee @me --state open

# View issues by label
gh issue list --label "bug" --state open
gh issue list --label "in-progress"

# View sprint progress
gh issue list --label "sprint-current" --state open
```

### Weekly Planning
```bash
# Create weekly planning issue
gh issue create --title "Week $(date +%Y-W%V) Planning" \
  --body "## This Week's Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Carried Over
- Items from last week

## Blocked
- List blockers here" \
  --label "planning,weekly"
```

## 🔄 Automation with GitHub Actions

### Auto-close completed tasks
```yaml
# .github/workflows/auto-close.yml
name: Auto Close Completed Tasks
on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:     # Manual trigger
jobs:
  close-completed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v6
        with:
          script: |
            const issues = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              labels: 'task',
              state: 'open'
            });
            
            for (const issue of issues.data) {
              // Check if all checklist items are completed
              const checklistComplete = !issue.body.includes('- [ ]');
              if (checklistComplete && issue.body.includes('- [x]')) {
                await github.rest.issues.update({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: issue.number,
                  state: 'closed',
                  labels: [...issue.labels.map(l => l.name), 'auto-closed']
                });
              }
            }
```

## 🚀 Quick Commands Reference

### Planning
```bash
# Create epic
gh issue create --title "EPIC: [Major Feature]" --label "epic"

# Create sub-tasks
gh issue create --title "Sub: [Specific Task]" --body "Part of #[EPIC_NUMBER]" --label "task"

# View roadmap
gh issue list --label "epic" --state all

# Create milestone
gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="v1.0" \
  --field description="First release" \
  --field due_on="2025-12-31T23:59:59Z"
```

### Daily Work
```bash
# Start work on issue
gh issue develop [ISSUE_NUMBER] --checkout

# Update status
gh issue comment [ISSUE_NUMBER] --body "Progress: Completed X, working on Y"

# Add labels
gh issue edit [ISSUE_NUMBER] --add-label "in-progress"

# Complete task
gh issue close [ISSUE_NUMBER] --comment "Completed: [summary of what was done]"
```

### Reporting
```bash
# Generate sprint report
gh issue list --state closed \
  --search "closed:>=$(date -d '7 days ago' +%Y-%m-%d)" \
  --json number,title,closedAt,labels \
  --jq '.[] | "#\(.number) \(.title) [\(.labels[].name)]"'

# View velocity (issues closed per day)
gh issue list --state closed \
  --search "closed:>=$(date -d '30 days ago' +%Y-%m-%d)" \
  --json closedAt \
  --jq 'group_by(.closedAt[0:10]) | map({date: .[0].closedAt[0:10], count: length})'

# Generate changelog
gh issue list --state closed \
  --milestone "v1.0" \
  --json number,title,labels \
  --jq '.[] | "- \(.title) (#\(.number))"'
```

## 📝 Integration with Claude/AI Assistants

### Workflow Integration
1. **Start session**: Check assigned issues
   ```bash
   gh issue list --assignee @me --state open
   ```

2. **Pick issue**: View details
   ```bash
   gh issue view [ISSUE_NUMBER]
   ```

3. **Update progress**: Add comments
   ```bash
   gh issue comment [ISSUE_NUMBER] --body "Progress update..."
   ```

4. **Complete**: Close with summary
   ```bash
   gh issue close [ISSUE_NUMBER] --comment "Completed: [what was done]"
   ```

### AI-Friendly Issue Templates
```bash
# Create detailed implementation issue
gh issue create --title "Implement [Feature]" \
  --body "## Context
[Background information]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Technical Details
- Language: [Python/JS/etc]
- Dependencies: [list]
- Files to modify: [list]

## Acceptance Criteria
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code reviewed" \
  --label "feature,needs-implementation"
```

## 🎯 Example Sprint Board

```bash
# View current sprint
gh issue list --label "sprint-current" --state open

# Example output:
#101 🐛 Fix database connection timeout        [bug, high-priority, sprint-current]
#102 ✨ Add user authentication               [feature, high-priority, sprint-current]  
#103 🔧 Refactor API error handling           [refactor, medium-priority, sprint-current]
#104 📝 Update API documentation              [documentation, low-priority, sprint-current]
#105 ✅ Add integration tests                 [test, medium-priority, sprint-current]
```

## 🔗 Useful Aliases

Add to ~/.zshrc or ~/.bashrc:
```bash
# Quick planning commands
alias ghplan='gh issue list --assignee @me --state open'
alias ghtask='gh issue create --label task --assignee @me --title'
alias ghbug='gh issue create --label bug,high-priority --title'
alias ghfeat='gh issue create --label feature --title'
alias ghdone='gh issue close --comment "Completed"'
alias ghsprint='gh issue list --label sprint-current --state open'
alias ghprogress='gh issue comment'

# Quick filters
alias ghblocked='gh issue list --label blocked --state open'
alias ghhigh='gh issue list --label high-priority --state open'
alias ghreview='gh issue list --label needs-review --state open'
```

## 📌 Project-Specific Configuration

To customize for your project:
1. Replace `[PROJECT_NAME]` with your project name
2. Replace `[USERNAME/ORG]` with your GitHub username or organization
3. Adjust labels to match your workflow
4. Add project-specific milestones
5. Customize sprint duration and planning cycles