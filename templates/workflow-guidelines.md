# Claude Coding Workflow Guidelines

## Complete Workflow Process

### 🎯 Phase 1: Planning (Use Opus 4 if available)
1. **Switch to Planning Mode**: Use `Shift + Tab` to switch to planning mode
2. **Use Planning Prompt**: Copy and paste the Planning Mode prompt
3. **Create Todo**: Generate detailed `tasks/todo.md` using the template
4. **Get Approval**: Confirm plan before implementation

### 🔧 Phase 2: Implementation
1. **Follow Todo List**: Work through tasks one by one
2. **Mark Progress**: Update checklist after each task
3. **Single File Focus**: Change only 1 file at a time when debugging
4. **High-Level Updates**: Provide brief explanation after each step
5. **Simple Changes**: Keep every change as minimal as possible

### 🔒 Phase 3: Security Validation
1. **Run Security Check**: Use Security Check prompt after implementation
2. **Review All Code**: Check for vulnerabilities and sensitive data exposure
3. **Generate Security Report**: Document findings and recommendations
4. **Fix Issues**: Address any security concerns identified

### 📚 Phase 4: Learning & Knowledge Transfer
1. **Use Learning Prompt**: Apply Learning/Explanation prompt
2. **Generate Explanation**: Get detailed technical explanation
3. **Document Insights**: Record key learnings and patterns
4. **Plan Improvements**: Note future optimization opportunities

### 🔄 Phase 5: Session Management
1. **Complete Review**: Finish todo review section
2. **End Session**: Use `/cancel` to end current session
3. **Start Fresh**: Begin new session for optimal performance
4. **Cost Optimization**: Manage token usage efficiently
---

## Best Practices

### File Management
- **Small Files**: Keep files focused on single responsibility
- **Trust Functionality**: Work with existing patterns
- **Minimal Impact**: Change as little code as possible
- **Version Control**: Consider git commits after each major task

### Communication
- **Confirm First**: Always get approval before implementation
- **High-Level Updates**: Brief explanations, not code details
- **Progress Tracking**: Regular checklist updates
- **Clear Rationale**: Explain why certain approaches were chosen

### Quality Assurance
- **Security First**: Always run security validation
- **Test Early**: Validate functionality as you build
- **Follow Patterns**: Maintain existing code style and architecture
- **Document Changes**: Keep clear record of modifications

---

## Workflow Commands & Shortcuts

### Planning Phase Commands
```
Shift + Tab → Switch to Planning Mode
Copy Planning Prompt → Start structured planning
```

### Implementation Phase Commands
```
✅ Mark task complete in todo.md
🔄 Update progress status
📝 Add implementation notes
```

### Security Phase Commands
```
Copy Security Prompt → Run security validation
📋 Generate security report
🔧 Fix identified issues
```

### Learning Phase Commands
```
Copy Learning Prompt → Get technical explanation
📚 Document key insights
💡 Record improvement ideas
```

### Session Management Commands
```
/cancel → End current session
New Session → Fresh start for next task
```

---

## Common Pitfalls & Solutions

### ❌ Common Mistakes
- Making too many changes at once
- Not confirming plan before implementation
- Skipping security validation
- Continuing long sessions without breaks
- Not updating todo checklist

### ✅ Best Practices
- One small change at a time
- Always confirm before coding
- Security check after every implementation
- Fresh session for each major task
- Consistent progress tracking

---

## Quality Gates

### Before Implementation
- [ ] Planning prompt completed
- [ ] Todo.md created and approved
- [ ] Approach confirmed with user
- [ ] File structure planned

### During Implementation
- [ ] Following todo checklist
- [ ] Marking progress regularly
- [ ] Providing high-level updates
- [ ] Keeping changes minimal

### After Implementation
- [ ] Security prompt executed
- [ ] All vulnerabilities addressed
- [ ] Learning prompt completed
- [ ] Todo review section filled
- [ ] Session properly ended

---

## Success Metrics

### Efficiency Indicators
- All tasks completed as planned
- Minimal code changes required
- No security vulnerabilities found
- Clear understanding gained through learning phase

### Quality Indicators
- Code follows existing patterns
- Implementation is simple and maintainable
- Documentation is updated and accurate
- Knowledge transfer is complete

**Remember**: This workflow prioritizes quality, security, and learning over speed. Take time to do each phase properly.