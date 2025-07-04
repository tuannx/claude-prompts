# Session Management Guidelines

## Why Session Management Matters

### Performance Benefits
- **Fresh Context**: New sessions start with clean context window
- **Optimal Performance**: Claude works best with shorter, focused sessions
- **Memory Management**: Prevents context overflow and degraded responses
- **Token Efficiency**: Reduces token usage and associated costs

### Cost Optimization
- **Reduced Token Count**: Shorter sessions = fewer tokens per request
- **Efficient Processing**: Less context to process = faster responses
- **Budget Control**: Better control over API usage costs
- **Resource Management**: Optimal use of computational resources

---

## Session Lifecycle Management

### 🚀 Starting a New Session

#### When to Start Fresh
- Beginning a new project or major feature
- After completing a todo list
- When context becomes too long (>50 messages)
- When switching between different projects
- After encountering errors or confusion

#### Session Initialization
```markdown
1. Copy Claude.md setup rules
2. Paste into new session
3. Brief context about current project
4. Reference existing todo.md if continuing work
```
### 🔄 During Active Session

#### Session Health Indicators
- **Good Session**: Clear, focused responses
- **Degrading Session**: Repetitive or confused responses
- **Time to Reset**: When Claude seems to "forget" context

#### Maintaining Session Quality
- Keep conversations focused on single task
- Avoid jumping between unrelated topics
- Provide clear, specific instructions
- Reference previous work when needed

### 🛑 Ending a Session

#### When to End
- After completing a major task or todo list
- When session becomes unfocused or lengthy
- Before switching to different project
- After encountering persistent issues

#### Proper Session Closure
```markdown
1. Complete current task
2. Update todo.md progress
3. Run final security check if needed
4. Use /cancel command
5. Document session outcomes
```

---

## Session Types & Strategies

### 🎯 Planning Sessions (Prefer Opus 4)
**Duration**: 15-30 minutes  
**Purpose**: Create detailed project plans  
**End Trigger**: When todo.md is complete and approved

### 🔧 Implementation Sessions
**Duration**: 20-45 minutes  
**Purpose**: Execute specific tasks from todo list  
**End Trigger**: When 3-5 tasks completed or hitting complexity

### 🔒 Security Review Sessions
**Duration**: 10-20 minutes  
**Purpose**: Comprehensive security validation  
**End Trigger**: When security report completed

### 📚 Learning Sessions
**Duration**: 15-25 minutes  
**Purpose**: Knowledge transfer and explanation  
**End Trigger**: When explanation is complete

---

## Session Optimization Strategies

### Context Management
- **Summarize Previous Work**: Brief recap when starting new session
- **Reference Key Files**: Point to important documents/code
- **Focus on Current Task**: Avoid bringing up unrelated history
- **Use External Documentation**: Keep important info in files, not chat

### Communication Efficiency
- **Clear Objectives**: State session goals upfront
- **Specific Questions**: Ask focused, actionable questions
- **Progress Updates**: Regular checkpoints during long tasks
- **Explicit Confirmations**: Confirm understanding before proceeding

### Resource Optimization
- **Task Batching**: Group related tasks in same session
- **Logical Breakpoints**: End at natural completion points
- **Preparation**: Have materials ready before starting
- **Documentation**: Keep external records of decisions

---

## Session Performance Monitoring

### Quality Indicators
- **Response Clarity**: Clear, focused answers
- **Context Retention**: Remembers recent conversation
- **Task Execution**: Follows instructions accurately
- **Code Quality**: Maintains standards and patterns

### Warning Signs
- **Repetitive Responses**: Same suggestions repeatedly
- **Context Loss**: Forgetting recent decisions
- **Degraded Quality**: Lower quality code or explanations
- **Confusion**: Misunderstanding clear instructions

### Action Triggers
- **Performance Drop**: Start new session immediately
- **Long Duration**: Plan session end after 60 minutes
- **Task Completion**: Natural breakpoint reached
- **Scope Change**: Switching to different type of work

**Remember**: Good session management is key to maintaining high-quality output and cost efficiency. When in doubt, start fresh!