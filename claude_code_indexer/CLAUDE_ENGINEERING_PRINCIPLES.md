# Claude Code Engineering Principles & Patterns Guide

## 🎯 Core Principles to Apply

### 1. **KISS (Keep It Simple, Stupid)**
**Apply at EVERY level - from architecture to single functions**

#### Module Level:
```python
# ❌ BAD: Over-engineered module
class AbstractDataProcessorFactory:
    def create_processor(self, type):
        if type == "csv":
            return CSVProcessorAdapter(CSVReaderStrategy())
        # ... 10 more classes for simple CSV reading

# ✅ GOOD: Simple and direct
def read_csv(filename):
    with open(filename) as f:
        return list(csv.DictReader(f))
```

#### Function Level:
```python
# ❌ BAD: Trying to do too much
def process_user_data_and_send_email_and_log_and_update_cache(user):
    # 100 lines of mixed concerns...

# ✅ GOOD: Single responsibility
def process_user_data(user):
    return validate_user(user)

def send_welcome_email(user):
    email_service.send(user.email, "Welcome!")
```

### 2. **ReAct Pattern (Reason + Act)**
**Think before coding, explain reasoning**

```python
# ReAct Example:
"""
REASONING: Need to fetch user data
- Could use raw SQL (fast but rigid)
- Could use ORM (flexible but slower)
- Decision: Use ORM for maintainability since performance is adequate

ACTION: Implement using SQLAlchemy ORM
"""
def get_user(user_id: int) -> User:
    return db.session.query(User).filter_by(id=user_id).first()
```

### 3. **DRY (Don't Repeat Yourself)**
**Extract common patterns, but don't over-abstract**

```python
# ❌ BAD: Repeated logic
def calculate_order_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total * 1.08  # tax

def calculate_cart_total(products):
    total = 0
    for product in products:
        total += product.price * product.quantity
    return total * 1.08  # tax

# ✅ GOOD: Extracted common logic
def calculate_total_with_tax(items, tax_rate=0.08):
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * (1 + tax_rate)
```

### 4. **SOLID Principles**

#### S - Single Responsibility
```python
# Each class has ONE reason to change
class User:
    def __init__(self, email):
        self.email = email

class UserValidator:
    def validate(self, user):
        return "@" in user.email

class UserRepository:
    def save(self, user):
        db.save(user)
```

#### O - Open/Closed
```python
# Open for extension, closed for modification
class PaymentProcessor:
    def process(self, payment_method):
        return payment_method.charge()

class CreditCard:
    def charge(self):
        return "Charging credit card"

class PayPal:
    def charge(self):
        return "Charging PayPal"
```

#### L - Liskov Substitution
```python
# Subtypes must be substitutable
class Bird:
    def move(self):
        return "Flying"

class Penguin(Bird):
    def move(self):
        return "Swimming"  # Still moving, just differently
```

#### I - Interface Segregation
```python
# Don't force clients to depend on interfaces they don't use
class Printable:
    def print(self): pass

class Scannable:
    def scan(self): pass

# Printer only implements what it needs
class SimplePrinter(Printable):
    def print(self):
        return "Printing..."
```

#### D - Dependency Inversion
```python
# Depend on abstractions, not concretions
class EmailService:
    def send(self, message): pass

class SMTPEmailService(EmailService):
    def send(self, message):
        # SMTP implementation

class UserService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service  # Depends on abstraction
```

### 5. **OOP Best Practices**

```python
# Encapsulation
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    @property
    def balance(self):
        return self._balance

# Composition over Inheritance
class EmailSender:
    def send(self, message):
        # send logic

class UserNotifier:
    def __init__(self):
        self.email_sender = EmailSender()  # Composition
    
    def notify(self, user, message):
        self.email_sender.send(message)
```

### 6. **DDD (Domain-Driven Design)**

```python
# Rich Domain Models
class Order:
    def __init__(self):
        self.items = []
        self.status = "pending"
    
    def add_item(self, product, quantity):
        # Business logic here
        if self.status != "pending":
            raise ValueError("Cannot modify confirmed order")
        self.items.append(OrderItem(product, quantity))
    
    def confirm(self):
        if not self.items:
            raise ValueError("Cannot confirm empty order")
        self.status = "confirmed"

# Value Objects
class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

# Repositories
class OrderRepository:
    def find_by_id(self, order_id):
        # Abstract away data access
        pass
    
    def save(self, order):
        # Persist domain object
        pass
```

### 7. **EARS (Easy Approach to Requirements Syntax)**

```python
"""
EARS Template Requirements:

[WHEN <trigger>] [WHERE <state>] 
the <system> SHALL <action> [WITHIN <performance>]

Examples:
- WHEN user clicks submit, the system SHALL validate form WITHIN 100ms
- WHERE user is authenticated, the system SHALL display dashboard
- The system SHALL encrypt passwords using bcrypt
"""

# Implementation following EARS requirement
class AuthenticationSystem:
    def login(self, username, password):
        """
        WHEN user submits credentials
        the system SHALL authenticate user
        WITHIN 500ms
        """
        start_time = time.time()
        
        user = self.find_user(username)
        if user and self.verify_password(password, user.password_hash):
            # Performance requirement check
            elapsed = time.time() - start_time
            if elapsed > 0.5:
                logger.warning(f"Login took {elapsed}s, exceeding 500ms requirement")
            return self.create_session(user)
        return None
```

## 🏗️ Architecture Patterns

### 1. **Layered Architecture (KISS-friendly)**
```
presentation/
├── api/          # REST endpoints
├── cli/          # Command line interface
└── web/          # Web UI

application/
├── services/     # Business logic
├── dto/          # Data transfer objects
└── mappers/      # Object mapping

domain/
├── entities/     # Core business objects
├── value_objects/
└── repositories/ # Interfaces only

infrastructure/
├── persistence/  # Database implementation
├── external/     # Third-party integrations
└── config/       # Configuration
```

### 2. **Module Organization (KISS)**
```python
# user_service.py - Everything about users in one place
class User:
    """Domain entity"""
    pass

class UserService:
    """Business logic"""
    def create_user(self, data):
        # KISS: Simple validation
        if not data.get('email'):
            raise ValueError("Email required")
        
        user = User(email=data['email'])
        return self.repo.save(user)

class UserRepository:
    """Data access"""
    def save(self, user):
        # Simple and direct
        db.users.insert_one(user.to_dict())
```

## 📋 Decision Making Framework

### When to Apply Each Principle:

| Situation | Apply | Example |
|-----------|-------|---------|
| New feature | KISS first | Start with simplest solution |
| Repeated code | DRY | Extract common functionality |
| Complex logic | ReAct | Document reasoning |
| Growing class | SOLID-S | Split responsibilities |
| External dependencies | SOLID-D | Use abstractions |
| Business complexity | DDD | Rich domain models |
| Requirements unclear | EARS | Formalize requirements |

## 🚀 Implementation Checklist

Before implementing ANY feature:

1. **Requirements (EARS)**
   - [ ] Clear trigger/condition?
   - [ ] Specific action defined?
   - [ ] Performance criteria?

2. **Design (KISS + ReAct)**
   - [ ] Simplest solution considered?
   - [ ] Reasoning documented?
   - [ ] Future changes anticipated?

3. **Code Structure (SOLID + OOP)**
   - [ ] Single responsibility per class/function?
   - [ ] Dependencies injected?
   - [ ] Interfaces segregated?

4. **Domain Logic (DDD)**
   - [ ] Business rules in domain objects?
   - [ ] Value objects for concepts?
   - [ ] Repository pattern for persistence?

5. **Quality (DRY + Patterns)**
   - [ ] No duplicated logic?
   - [ ] Appropriate patterns used?
   - [ ] Tests following same principles?

## 💡 Example: Applying All Principles

```python
# EARS Requirement:
# WHEN customer places order WHERE inventory is available
# the system SHALL reserve items and process payment WITHIN 2 seconds

# ReAct: Reasoning
# Need to coordinate inventory and payment - use service pattern
# Keep domain logic in entities, infrastructure separate

# Domain Entity (DDD + OOP)
class Order:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.items = []
        self.status = OrderStatus.PENDING
    
    def add_item(self, product, quantity):
        # KISS: Simple validation
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items.append(OrderItem(product, quantity))
    
    def can_be_placed(self):
        # Business rule in domain
        return len(self.items) > 0 and self.status == OrderStatus.PENDING

# Service Layer (SOLID + DRY)
class OrderService:
    def __init__(self, order_repo, inventory_service, payment_service):
        # Dependency Injection (SOLID-D)
        self.order_repo = order_repo
        self.inventory = inventory_service
        self.payment = payment_service
    
    def place_order(self, order):
        # Single Responsibility
        if not order.can_be_placed():
            raise BusinessError("Order cannot be placed")
        
        # KISS: Clear, simple flow
        with self.start_transaction():
            self.inventory.reserve_items(order.items)
            self.payment.process(order.total())
            order.status = OrderStatus.CONFIRMED
            self.order_repo.save(order)

# Infrastructure (Separated concerns)
class InventoryService:
    def reserve_items(self, items):
        # Implementation details hidden
        pass

class PaymentService:
    def process(self, amount):
        # External system integration
        pass
```

## 🎯 Quick Reference

### For Every Feature:
1. **Start with KISS** - Simplest solution first
2. **Apply ReAct** - Document your reasoning
3. **Follow SOLID** - Keep it maintainable
4. **Use DDD** - When business logic is complex
5. **Check DRY** - Extract repeated patterns
6. **Validate with EARS** - Requirements met?

### Red Flags to Avoid:
- 🚫 Classes doing multiple things
- 🚫 Functions longer than 20 lines
- 🚫 Deeply nested code (>3 levels)
- 🚫 Copy-pasted code blocks
- 🚫 Tight coupling to implementations
- 🚫 Business logic in controllers/views
- 🚫 Anemic domain models

### Green Flags to Pursue:
- ✅ Clear single purpose per module
- ✅ Easy to test in isolation
- ✅ Business rules in domain
- ✅ Dependencies injected
- ✅ Common patterns extracted
- ✅ Requirements traceable to code

---

Remember: **KISS trumps all** - It's better to have simple, clear code than perfectly architected but complex code. Apply other principles only when they make things simpler, not more complex!