# Claude Code Indexer - GitHub Project Planning

## 🎯 Project Overview
GitHub-based planning for claude-code-indexer development and maintenance.

## 📋 Current Sprint Tasks

### View Current Issues
```bash
# View all open issues
gh issue list --state open

# View high priority bugs
gh issue list --label "bug,high-priority" --state open

# View feature requests
gh issue list --label "feature" --state open
```

## 🏷️ Project-Specific Labels

### Component Labels
```bash
cli              # CLI interface issues
indexer          # Core indexing engine
parser           # Language parsers (Python, JS, TS, Java)
mcp              # MCP server integration
cache            # Caching system
database         # SQLite/APSW issues
background       # Background service
storage          # Storage management
```

### Language Support
```bash
lang-python      # Python parser issues
lang-javascript  # JavaScript parser issues
lang-typescript  # TypeScript parser issues
lang-java        # Java parser issues
lang-new         # New language support requests
```

## 📝 Common Issue Templates

### Bug Report
```bash
gh issue create --title "Bug: [Component] - Brief description" \
  --body "## Description
[What's broken]

## Steps to Reproduce
1. Run command: \`claude-code-indexer ...\`
2. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- claude-code-indexer version: $(claude-code-indexer --version)
- Python version: $(python --version)
- OS: [macOS/Linux/Windows]

## Error Output
\`\`\`
[paste error here]
\`\`\`" \
  --label "bug"
```

### Feature Request
```bash
gh issue create --title "Feature: Add support for [language/feature]" \
  --body "## Feature Description
[What you want]

## Use Case
[Why it's needed]

## Proposed Implementation
- [ ] Step 1
- [ ] Step 2

## Alternative Solutions
[Other approaches considered]" \
  --label "feature,enhancement"
```

### New Language Support
```bash
gh issue create --title "Language: Add support for [Language]" \
  --body "## Language Details
- Language: [Name]
- File extensions: [.ext1, .ext2]
- AST library: [suggested library]

## Parser Requirements
- [ ] Classes/Types
- [ ] Functions/Methods
- [ ] Imports/Dependencies
- [ ] Comments/Docstrings

## Sample Code
\`\`\`[language]
[sample code to parse]
\`\`\`

## Expected Nodes
- Classes: X
- Functions: Y
- Imports: Z" \
  --label "feature,lang-new"
```

## 🚀 Development Workflow

### Starting New Feature
```bash
# 1. Create feature branch
gh issue develop [ISSUE_NUMBER] --checkout

# 2. Update issue status
gh issue edit [ISSUE_NUMBER] --add-label "in-progress"

# 3. Work on feature
# ... implement changes ...

# 4. Run tests
python -m pytest tests/

# 5. Create PR
gh pr create --title "Fix #[ISSUE_NUMBER]: [Title]" \
  --body "Closes #[ISSUE_NUMBER]

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Documentation updated"
```

### Release Process
```bash
# 1. Create release issue
gh issue create --title "Release v[X.Y.Z]" \
  --body "## Release Checklist
- [ ] Update version in pyproject.toml
- [ ] Update CHANGELOG.md
- [ ] Run all tests
- [ ] Build package
- [ ] Test installation
- [ ] Create git tag
- [ ] Push to PyPI
- [ ] Update documentation" \
  --label "release" \
  --milestone "v[X.Y.Z]"

# 2. After release
gh release create v[X.Y.Z] \
  --title "Version [X.Y.Z]" \
  --notes "See CHANGELOG.md for details"
```

## 📊 Project Metrics

### Weekly Stats
```bash
# Issues closed this week
gh issue list --state closed \
  --search "closed:>=$(date -d '7 days ago' +%Y-%m-%d)" \
  --json number,title,labels

# PRs merged this week  
gh pr list --state merged \
  --search "merged:>=$(date -d '7 days ago' +%Y-%m-%d)"

# New issues this week
gh issue list --state all \
  --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)"
```

### Component Health
```bash
# Issues by component
for label in cli indexer parser mcp cache database; do
  echo "=== $label ==="
  gh issue list --label "$label" --state open --limit 5
done

# Language parser issues
for lang in python javascript typescript java; do
  echo "=== lang-$lang ==="
  gh issue list --label "lang-$lang" --state open
done
```

## 🔧 Maintenance Tasks

### Regular Maintenance
```bash
# Weekly: Check for stale issues
gh issue list --state open \
  --search "updated:<$(date -d '30 days ago' +%Y-%m-%d)" \
  --json number,title,updatedAt

# Monthly: Update dependencies
gh issue create --title "Monthly: Update dependencies" \
  --body "- [ ] Update pyproject.toml dependencies
- [ ] Run pip-compile
- [ ] Test with new versions
- [ ] Update CI/CD if needed" \
  --label "task,maintenance"

# Quarterly: Performance review
gh issue create --title "Quarterly: Performance benchmarks" \
  --body "- [ ] Run benchmarks on large codebases
- [ ] Compare with previous quarter
- [ ] Identify bottlenecks
- [ ] Create optimization issues" \
  --label "task,performance"
```

## 🏷️ Useful Aliases for Claude Code Indexer

```bash
# Add to ~/.zshrc or ~/.bashrc
alias cciplan='gh issue list --repo tuannx/claude-code-indexer --assignee @me --state open'
alias ccibug='gh issue create --repo tuannx/claude-code-indexer --label bug --title'
alias ccifeat='gh issue create --repo tuannx/claude-code-indexer --label feature --title'
alias ccilang='gh issue create --repo tuannx/claude-code-indexer --label lang-new --title'
alias ccipr='gh pr create --repo tuannx/claude-code-indexer'
```

## 📌 Current Priorities

1. **Performance Optimization**
   - Parallel processing improvements
   - Cache optimization
   - Large codebase handling

2. **Language Support**
   - Improve JavaScript/TypeScript parsing
   - Add more language parsers
   - Better JSX/TSX support

3. **MCP Integration**
   - Enhanced Claude Desktop features
   - Better error handling
   - Auto-indexing on project open

4. **Documentation**
   - API documentation
   - Parser development guide
   - Performance tuning guide

## 🎯 Current Active Issues (2025-07-18)

```bash
# View all open issues
gh issue list --state open

# Active Issues:
#2 📦 Release v1.10.0 to PyPI                  [enhancement]
#3 🐛 Bug: Help text test failure              [bug]
#4 ✨ Feature: Add support for Go language     [enhancement]
#5 📝 Task: Add performance benchmarks         [documentation]
#6 📋 Week 2025-W03 Planning                   

# Priority: Release v1.10.0
gh issue view 2  # See full release checklist
```