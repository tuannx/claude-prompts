# Examples & Use Cases

## 🎯 Real-World Example: Building User Authentication

### Scenario
"I need to add user authentication to my React app with JWT tokens and password hashing."

### Complete Workflow

#### Session 1: Planning (Opus 4 Preferred)
```markdown
USER: Copy Claude.md rules first, then use planning mode prompt to create a todo for user authentication system

CLAUDE: [Creates detailed todo.md with tasks like:]
- [ ] Create auth middleware (auth/middleware.js)
- [ ] Add password hashing utility (utils/bcrypt.js) 
- [ ] Create JWT token service (services/jwt.js)
- [ ] Build login API endpoint (routes/auth.js)
- [ ] Add protected route wrapper (components/ProtectedRoute.js)

USER: Approved, let's implement
CLAUDE: Plan confirmed. Use /cancel to end planning session and start fresh implementation session.
```

#### Session 2: Implementation
```markdown
USER: [Paste Claude.md rules] + Reference todo.md for auth system

CLAUDE: Starting with auth middleware implementation...
✅ Task 1: Created auth/middleware.js with JWT verification
✅ Task 2: Added bcrypt utility for password hashing
[Updates todo.md progress after each task]

USER: Continue with remaining tasks
CLAUDE: ✅ Task 3: JWT service implemented
✅ Task 4: Login endpoint created
[High-level explanations, no code dumps]
```

#### Session 3: Security Review
```markdown
USER: [Paste security check prompt]

CLAUDE: 
## Security Review Report
✅ Passwords properly hashed with bcrypt
✅ JWT secrets in environment variables
⚠️ Consider adding rate limiting to login endpoint
🔧 Recommend HTTPS enforcement for production
```

#### Session 4: Learning
```markdown
USER: [Paste learning explanation prompt]

CLAUDE: 
# Authentication System Explanation
## 🎯 Problem Solved: Secure user authentication with JWT
## 🏗️ Architecture: Middleware-based approach with bcrypt hashing
[Detailed technical walkthrough and rationale]
```
---

## 🔧 Common Use Case Patterns

### 1. Feature Development
**Best For**: Adding new functionality to existing applications
**Session Pattern**: Plan → Implement → Security → Learning
**Key Focus**: Integration with existing patterns

#### Example Tasks
- Adding payment processing
- Building notification system
- Creating admin dashboard
- Implementing search functionality

#### Sample Todo Structure
```markdown
- [ ] Research existing patterns (research/patterns.md)
- [ ] Create service layer (services/payment.js)
- [ ] Add API endpoints (routes/payment.js)
- [ ] Build frontend components (components/Payment/)
- [ ] Add error handling (utils/errors.js)
- [ ] Write tests (tests/payment.test.js)
```

### 2. Bug Fixing & Debugging
**Best For**: Resolving specific issues or unexpected behavior
**Session Pattern**: Plan → Debug → Security → Learning
**Key Focus**: Minimal changes, root cause analysis

#### Example Tasks
- Memory leak investigation
- Performance optimization
- Cross-browser compatibility
- API response issues

#### Sample Todo Structure
```markdown
- [ ] Reproduce bug consistently (debug/reproduction.md)
- [ ] Identify root cause (debug/analysis.md)
- [ ] Create minimal fix (fix specific file)
- [ ] Add regression test (tests/regression.test.js)
- [ ] Validate fix works (manual testing)
```

### 3. Security Hardening
**Best For**: Improving application security posture
**Session Pattern**: Plan → Implement → Security → Learning
**Key Focus**: Security-first approach, comprehensive validation

#### Example Tasks
- Input validation improvements
- Authentication strengthening
- Authorization fixes
- Dependency updates

#### Sample Todo Structure
```markdown
- [ ] Security audit current code (audit/findings.md)
- [ ] Add input validation (validators/input.js)
- [ ] Strengthen auth middleware (auth/security.js)
- [ ] Update vulnerable dependencies (package.json)
- [ ] Add security headers (middleware/security.js)
```

---

## 🎛️ Session Management Examples

### Short Task Example (Single Session)
```markdown
Objective: Fix specific CSS bug
Duration: 15-20 minutes

Flow:
1. Paste Claude.md rules
2. Describe bug with reproduction steps
3. Create mini-todo (3-4 tasks)
4. Implement fix
5. Test solution
6. Use /cancel

Result: Quick, focused fix with proper workflow
```

### Medium Task Example (2-3 Sessions)
```markdown
Objective: Add new API endpoint
Duration: 45-75 minutes total

Session 1 (Planning):
- Create detailed todo
- Plan implementation approach
- Get approval

Session 2 (Implementation):
- Build endpoint and tests
- Update documentation
- Basic validation

Session 3 (Security + Learning):
- Security review
- Technical explanation
- Knowledge transfer
```

### Large Task Example (5+ Sessions)
```markdown
Objective: Implement full user management system
Duration: 2-3 hours total

Session 1: Planning and architecture
Session 2: Database and models
Session 3: API endpoints
Session 4: Frontend components
Session 5: Authentication integration
Session 6: Security review
Session 7: Learning and documentation
```

---

## 🚀 Success Stories

### Story 1: E-commerce Integration
**Challenge**: Add Stripe payment processing to existing app
**Approach**: 4-session workflow over 2 days
**Result**: Secure payment system with comprehensive testing

**Key Success Factors**:
- Detailed planning prevented scope creep
- Single-file focus made debugging easy
- Security review caught potential issues
- Learning session provided long-term understanding

### Story 2: Database Performance Fix
**Challenge**: Slow queries affecting user experience  
**Approach**: 3-session debugging workflow
**Result**: 10x performance improvement with minimal code changes

**Key Success Factors**:
- Systematic debugging approach
- Small, targeted optimizations
- Comprehensive testing after each change
- Documentation of optimization patterns

**Remember**: These examples show the power of structured, session-based development. The key is breaking large problems into manageable, focused sessions.