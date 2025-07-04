# Claude Coding Assistant - Usage Documentation

## 🎯 Purpose

This prompt system provides a structured workflow for using Claude as a coding assistant. It emphasizes planning, security, learning, and efficient session management to deliver high-quality, maintainable code.

## 📁 File Structure

```
claude-prompts/
├── CLAUDE.md                    # Main setup rules (start here)
├── prompts/
│   ├── planning-mode.md         # For creating detailed plans
│   ├── security-check.md        # Security validation
│   └── learning-explanation.md  # Knowledge transfer
├── templates/
│   ├── todo-template.md         # Task planning template
│   ├── workflow-guidelines.md   # Complete workflow process
│   └── session-management.md    # Session optimization
└── README.md                   # This file
```

## 🚀 Quick Start Guide

### 🔥 Vibecode Mode (Fast Flow)
- Type `!!!` at the start of your request to activate vibecode mode
- Claude will skip confirmations and execute immediately
- Get results faster with less back-and-forth
- Example: `!!! implement a todo list feature`

## 📖 Standard Workflow

### Step 1: Initial Setup
1. **Copy `CLAUDE.md`** content and paste into new Claude session
2. **Describe your project** briefly to establish context
3. **Switch to planning mode** using `Shift + Tab` (prefer Opus 4)

### Step 2: Planning Phase
1. **Use Planning Mode prompt** from `prompts/planning-mode.md`
2. **Generate detailed todo list** using `templates/todo-template.md`
3. **Get approval** before proceeding with implementation
4. **End planning session** with `/cancel`

### Step 3: Implementation Phase
1. **Start new session** with `CLAUDE.md` rules
2. **Reference your todo.md** file for task list
3. **Work through tasks** one by one, updating progress
4. **Keep changes minimal** and focused on single files
### Step 4: Security Validation
1. **Use Security Check prompt** from `prompts/security-check.md`
2. **Review all modified code** for vulnerabilities
3. **Generate security report** and fix any issues
4. **Ensure no sensitive data exposure**

### Step 5: Learning & Knowledge Transfer
1. **Use Learning prompt** from `prompts/learning-explanation.md`
2. **Get detailed technical explanation** of what was built
3. **Document key insights** and patterns learned
4. **Plan future improvements**

### Step 6: Session Management
1. **Complete todo review section**
2. **Use `/cancel`** to end session efficiently
3. **Start fresh session** for next major task

## 🔧 Core Workflow Commands

### Planning Commands
```bash
# Switch to planning mode
Shift + Tab

# Copy planning prompt
cat prompts/planning-mode.md

# Create todo from template
cp templates/todo-template.md tasks/todo.md
```

### Implementation Commands
```bash
# Start implementation session
cat CLAUDE.md

# Update progress
# ✅ Mark completed tasks in todo.md
# 🔄 Update status regularly
# 📝 Add implementation notes
```

### Security Commands
```bash
# Run security validation
cat prompts/security-check.md

# Generate security report
# 📋 Document findings
# 🔧 Fix identified issues
```

### Learning Commands
```bash
# Get technical explanation
cat prompts/learning-explanation.md

# Document insights
# 📚 Record key patterns
# 💡 Note improvements
```

## 📋 Best Practices

### File Management
- **Keep files small** and focused on single responsibility
- **Change only 1 file at a time** when debugging
- **Trust existing functionality** and work with current patterns
- **Use absolute paths** for reliability

### Communication
- **Confirm before implementation** - always get approval
- **Provide high-level updates** after each step
- **Update progress regularly** in todo.md
- **Explain reasoning** for technical decisions

### Quality Assurance
- **Run security check** after every implementation
- **Follow existing code patterns** and style
- **Keep changes minimal** and simple
- **Document all modifications**

### Session Management
- **End sessions** after completing logical units of work
- **Start fresh** for optimal performance
- **Use `/cancel`** to properly close sessions
- **Keep sessions focused** on single objectives

## ⚠️ Common Pitfalls

### What NOT to Do
- ❌ Skip the planning phase
- ❌ Make massive changes without approval
- ❌ Continue long sessions without breaks
- ❌ Ignore security validation
- ❌ Forget to update todo progress

### What TO Do Instead
- ✅ Always plan before implementing
- ✅ Make small, incremental changes
- ✅ Use fresh sessions for major tasks
- ✅ Run security checks religiously
- ✅ Track progress consistently

## 🎯 Success Metrics

### Quality Indicators
- All planned tasks completed successfully
- No security vulnerabilities detected
- Code follows existing patterns and standards
- Clear understanding gained through learning phase
- Efficient session usage and cost management

### Efficiency Indicators
- Minimal back-and-forth during implementation
- Fast problem resolution with focused changes
- Proper documentation and knowledge transfer
- Smooth transition between sessions

## 🆘 Troubleshooting

### If Claude seems confused or unfocused
1. **End current session** with `/cancel`
2. **Start fresh session** with `CLAUDE.md` rules
3. **Provide clear context** about current work
4. **Reference existing todo.md** for continuity

### If tasks are too complex
1. **Break down further** into smaller subtasks
2. **Update todo.md** with more granular steps
3. **Focus on single file changes**
4. **Get approval** for revised approach

### If security issues are found
1. **Stop implementation** immediately
2. **Address security concerns** first
3. **Re-run security check** after fixes
4. **Document security measures** taken

## 💡 Pro Tips

### For Better Planning
- Use Opus 4 when available for planning sessions
- Include time estimates for better planning
- Consider dependencies between tasks
- Plan for testing and validation

### For Efficient Implementation
- Keep implementation sessions under 60 minutes
- Focus on 3-5 related tasks per session
- Update todo.md after each completed task
- Provide brief explanations, not code details

### For Optimal Learning
- Ask for specific patterns and best practices
- Request explanation of alternative approaches
- Document reusable insights for future projects
- Connect new learnings to existing knowledge

**Remember**: This system prioritizes quality, security, and learning over speed. Take time to follow each phase properly for best results.