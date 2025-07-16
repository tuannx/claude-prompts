# 🎯 Engineering Quick Reference Card

## 📋 Order of Operations (ALWAYS)

1. **KISS** → Simplest solution first
2. **ReAct** → Document reasoning  
3. **EARS** → Clear requirements
4. **SOLID** → When complexity justified
5. **DRY** → Extract repetition
6. **DDD** → For business complexity

## ⚡ Quick Patterns

### KISS Function vs Class
```python
# Use function if stateless
def calculate_tax(amount):
    return amount * 0.08

# Use class if stateful or complex
class TaxCalculator:
    def __init__(self, rate):
        self.rate = rate
    
    def calculate(self, amount):
        return amount * self.rate
```

### ReAct Documentation
```python
"""
REASONING: [Problem and constraints]
OPTIONS: 
  1. [Option] - [Pros/Cons]
  2. [Option] - [Pros/Cons]
DECISION: [Choice] because [reason]
"""
```

### EARS Requirements
```
WHEN <user action>
WHERE <system state>  
the system SHALL <behavior>
WITHIN <performance>
```

### SOLID Quick Check
- **S**: One reason to change?
- **O**: Can extend without modify?
- **L**: Can substitute subtype?
- **I**: Minimal interfaces?
- **D**: Depend on abstractions?

### DRY Decision Tree
```
Repeated 2x → Wait
Repeated 3x → Extract function
Repeated 4x+ → Consider abstraction
```

### DDD Triggers
- Complex business rules → Domain model
- Money/measurements → Value object
- Data access → Repository pattern
- Multi-step process → Service layer

## 🚨 Red Flags

1. **Method > 20 lines** → Split it
2. **Class > 200 lines** → Split responsibilities  
3. **Nesting > 3 levels** → Extract method
4. **Parameters > 4** → Use object
5. **Comments explaining what** → Refactor code
6. **Copy-paste code** → Extract common

## ✅ Green Flags  

1. **Method < 10 lines** → Good
2. **Clear single purpose** → Good
3. **No comments needed** → Self-documenting
4. **Easy to test** → Loosely coupled
5. **New req = new file** → Open/Closed
6. **Junior can understand** → KISS achieved

## 🎯 Decision Matrix

| Code Complexity | Apply |
|----------------|-------|
| Trivial (1-10 lines) | KISS only |
| Simple (10-50 lines) | KISS + DRY |
| Medium (50-200 lines) | + SOLID principles |
| Complex (200+ lines) | + DDD patterns |
| Business critical | All principles |

## 📝 Before Every PR

```markdown
- [ ] KISS: Is this the simplest solution?
- [ ] ReAct: Is reasoning documented?  
- [ ] SOLID: Single responsibility maintained?
- [ ] DRY: No copy-paste code?
- [ ] Tests: Cover the requirements?
- [ ] EARS: Requirements traceable?
```

## 🚀 Common Refactorings

### Extract Method (Most Common)
```python
# Before
def process_order(order):
    # ... 50 lines doing 3 things

# After  
def process_order(order):
    validate_order(order)
    calculate_totals(order)
    send_confirmation(order)
```

### Replace Conditional with Polymorphism
```python
# Before
if type == "credit":
    # process credit
elif type == "debit":
    # process debit

# After
payment_method.process()
```

### Extract Class
```python
# Before: User class doing emails
class User:
    def send_welcome_email(self):
        # email logic

# After: Separate concern
class EmailService:
    def send_welcome(self, user):
        # email logic
```

## 💡 Remember

> "Make it work, make it right, make it fast" - Kent Beck

1. **Working** > Perfect
2. **Simple** > Clever  
3. **Clear** > Concise
4. **Testable** > Elegant
5. **Maintainable** > Optimal

**When in doubt, choose SIMPLE!**