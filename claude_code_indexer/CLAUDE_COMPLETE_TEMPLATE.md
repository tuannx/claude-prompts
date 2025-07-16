# Claude Coding Assistant - Complete Setup Rules

## 🚀 MANDATORY: Start Every Session with Code Indexing

### ⚡ FIRST THING TO DO IN EVERY SESSION:
```bash
# 1. Check if project is indexed (takes 0.1s)
claude-code-indexer stats

# 2. If not indexed or outdated, run indexing (uses cache, very fast)
claude-code-indexer index . --workers 4

# 3. Load project context into memory
claude-code-indexer query --important --limit 20
```

### 📊 Why This is CRITICAL:
- **64.6x faster** than reading files manually (0.07s vs 4.66s)
- **Instant understanding** of project structure and relationships
- **Smart prioritization** - See most important code first
- **Change awareness** - Know what was modified since last session
- **Pattern detection** - Understand architecture and design patterns

## 🏗️ Engineering Principles & Patterns

### MANDATORY: Apply These Principles in Order

#### 1. **KISS (Keep It Simple, Stupid)** - ALWAYS FIRST
The #1 rule that overrides all others. Start simple, add complexity only when proven necessary.

```python
# ❌ BAD: Over-engineered for simple task
class UserDataProcessorFactory:
    def create_processor(self, type):
        if type == "validator":
            return UserValidatorStrategy(ValidationRulesEngine())
        # ... 50 more lines for validating an email

# ✅ GOOD: Simple and direct  
def validate_email(email):
    return "@" in email and "." in email.split("@")[1]
```

**KISS Checklist:**
- Can this be a function instead of a class?
- Can this be 5 lines instead of 50?
- Will a junior dev understand this immediately?
- Am I solving problems that don't exist yet?

#### 2. **ReAct Pattern** - Think Before Code
Document your reasoning before implementing. This prevents over-engineering and helps future maintenance.

```python
"""
REASONING: Need to store user preferences
- Option 1: Separate preferences table - More complex, better for scale
- Option 2: JSON column in users table - Simple, good for <1000 users
- Current scale: 100 users
DECISION: Use JSON column for simplicity (KISS)

ACTION: Add preferences JSON column to users table
"""
def save_preferences(user_id, preferences):
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        [json.dumps(preferences), user_id]
    )
```

#### 3. **SOLID Principles** - When Complexity is Justified

**S - Single Responsibility**
```python
# Each class has ONE job
class EmailSender:
    def send(self, to, subject, body):
        # Only handles sending

class EmailValidator:
    def is_valid(self, email):
        # Only handles validation

class EmailFormatter:
    def format_html(self, template, data):
        # Only handles formatting
```

**O - Open/Closed**
```python
# Extend behavior without modifying existing code
class NotificationSender:
    def send(self, channel, message):
        return channel.deliver(message)

# Easy to add new channels
class EmailChannel:
    def deliver(self, message):
        # Email implementation

class SMSChannel:
    def deliver(self, message):
        # SMS implementation
```

**L - Liskov Substitution**
```python
# Subclasses must be replaceable
class Payment:
    def process(self, amount):
        raise NotImplementedError

class CreditCardPayment(Payment):
    def process(self, amount):
        # Process credit card
        return {"status": "success", "amount": amount}

class PayPalPayment(Payment):
    def process(self, amount):
        # Process PayPal
        return {"status": "success", "amount": amount}
```

**I - Interface Segregation**
```python
# Don't force unnecessary methods
class Readable:
    def read(self): pass

class Writable:
    def write(self, data): pass

# Classes implement only what they need
class ReadOnlyFile(Readable):
    def read(self):
        return self.content

class ReadWriteFile(Readable, Writable):
    def read(self):
        return self.content
    
    def write(self, data):
        self.content = data
```

**D - Dependency Inversion**
```python
# Depend on abstractions
class OrderService:
    def __init__(self, payment_gateway, email_service):
        # Injected dependencies
        self.payment = payment_gateway
        self.email = email_service
    
    def process_order(self, order):
        # Use abstractions
        self.payment.charge(order.total)
        self.email.send_confirmation(order.customer_email)
```

#### 4. **DRY (Don't Repeat Yourself)** - But Don't Over-Abstract
Extract repeated logic, but keep it simple.

```python
# ❌ BAD: Repeated validation
def create_user(data):
    if not data.get('email') or '@' not in data['email']:
        raise ValueError("Invalid email")
    # ... create user

def update_user(data):
    if not data.get('email') or '@' not in data['email']:
        raise ValueError("Invalid email")
    # ... update user

# ✅ GOOD: Extracted but still simple
def validate_email(email):
    if not email or '@' not in email:
        raise ValueError("Invalid email")

def create_user(data):
    validate_email(data.get('email'))
    # ... create user
```

#### 5. **OOP Best Practices** - When Objects Make Sense

```python
# Encapsulation - Hide complexity
class BankAccount:
    def __init__(self):
        self._balance = 0  # Protected
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
    
    @property
    def balance(self):
        return self._balance

# Composition over Inheritance
class Car:
    def __init__(self):
        self.engine = Engine()  # HAS-A relationship
        self.wheels = [Wheel() for _ in range(4)]
    
    def start(self):
        return self.engine.start()

# NOT this
class Car(Engine, Wheels):  # IS-A confusion
    pass
```

#### 6. **DDD (Domain-Driven Design)** - For Complex Business Logic

```python
# Rich Domain Models (not anemic)
class ShoppingCart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        self._discount = None
    
    def add_item(self, product, quantity):
        # Business rule in domain
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Check stock
        if product.stock < quantity:
            raise ValueError(f"Only {product.stock} items in stock")
        
        self.items.append(CartItem(product, quantity))
    
    def apply_discount(self, code):
        # Business logic, not in controller
        if self._discount:
            raise ValueError("Discount already applied")
        
        discount = DiscountService.validate(code)
        if discount.minimum_amount > self.subtotal:
            raise ValueError(f"Minimum purchase of {discount.minimum_amount} required")
        
        self._discount = discount
    
    @property
    def total(self):
        subtotal = sum(item.total for item in self.items)
        if self._discount:
            subtotal *= (1 - self._discount.percentage)
        return subtotal

# Value Objects
class Money:
    def __init__(self, amount, currency='USD'):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = Decimal(str(amount))
        self.currency = currency
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency
```

#### 7. **EARS (Easy Approach to Requirements Syntax)**
Turn vague requirements into testable specifications.

```python
"""
EARS Format:
[WHEN <trigger>] [WHERE <state>] the <system> SHALL <action> [WITHIN <performance>]

Examples:
- WHEN user submits order, the system SHALL send confirmation email WITHIN 5 seconds
- WHERE inventory < 10, the system SHALL notify admin
- The system SHALL encrypt all passwords using bcrypt
"""

class OrderProcessor:
    def process_order(self, order):
        """
        WHEN order is submitted
        WHERE payment is valid AND inventory is available
        the system SHALL:
        1. Reserve inventory
        2. Process payment
        3. Send confirmation
        WITHIN 3 seconds
        """
        start_time = time.time()
        
        # Check state (WHERE)
        if not self.payment_service.is_valid(order.payment):
            raise PaymentError("Invalid payment")
        
        if not self.inventory.is_available(order.items):
            raise InventoryError("Items not available")
        
        # Perform actions (SHALL)
        with self.transaction():
            self.inventory.reserve(order.items)
            self.payment_service.process(order.payment)
            self.email_service.send_confirmation(order)
        
        # Check performance (WITHIN)
        elapsed = time.time() - start_time
        if elapsed > 3.0:
            logger.warning(f"Order processing took {elapsed}s, exceeding 3s SLA")
```

## 📋 Decision Making Framework

### When to Apply Each Principle:

| Situation | First Try | If Needed | Avoid |
|-----------|-----------|-----------|-------|
| New feature | KISS | Add patterns later | Over-engineering |
| Repeated code | Simple function | DRY abstraction | Premature optimization |
| Growing class | Split by responsibility | SOLID refactor | God objects |
| Complex business rules | Domain models | Full DDD | Anemic models |
| External dependencies | Direct use | Abstraction layer | Unnecessary wrappers |
| Performance issues | Measure first | Optimize hotspots | Guessing |

## 🚀 Implementation Workflow

### For EVERY Feature:

1. **Understand Context** (30 seconds)
   ```bash
   claude-code-indexer stats
   claude-code-indexer query --important
   claude-code-indexer search "<feature>"
   ```

2. **Define Requirements** (EARS)
   ```
   WHEN [trigger] WHERE [condition]
   the system SHALL [action] WITHIN [performance]
   ```

3. **Design with KISS + ReAct**
   ```python
   """
   REASONING: [Why this approach]
   OPTIONS: [What alternatives exist]
   DECISION: [Chosen approach + why]
   """
   ```

4. **Implement Following Principles**
   - Start with simplest solution (KISS)
   - Extract common code (DRY)
   - Keep single responsibility (SOLID-S)
   - Model domain if complex (DDD)

5. **Validate and Refactor**
   ```bash
   # Re-index to see impact
   claude-code-indexer index .
   claude-code-indexer query --dependencies "<new_code>"
   ```

## 🎯 Examples: Applying All Principles

### Simple Feature (KISS Wins)
```python
# Requirement: WHEN user logs in, the system SHALL record last login time

# KISS Solution (Correct ✅)
def record_login(user_id):
    db.execute(
        "UPDATE users SET last_login = ? WHERE id = ?",
        [datetime.now(), user_id]
    )

# Over-engineered (Wrong ❌)
class LoginEventProcessor:
    def __init__(self, event_store, user_repository, time_service):
        # 50 lines of unnecessary abstraction...
```

### Complex Feature (All Principles)
```python
# Requirement: E-commerce checkout with inventory, payment, shipping

# 1. EARS Specification
"""
WHEN customer confirms checkout
WHERE cart is valid AND payment authorized AND inventory available
the system SHALL:
1. Reserve inventory
2. Process payment
3. Create shipment
4. Send confirmation
WITHIN 5 seconds total
"""

# 2. ReAct Design
"""
REASONING: Checkout involves multiple systems that can fail
- Need transaction consistency
- Need rollback capability
- Need clear error handling
DECISION: Use service orchestration with saga pattern
"""

# 3. Implementation with all principles

# Domain Models (DDD)
class Order:
    def __init__(self, cart):
        self.items = cart.items
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
    
    def can_checkout(self):
        return (self.status == OrderStatus.PENDING and 
                len(self.items) > 0 and
                self.total > 0)
    
    @property
    def total(self):
        return sum(item.price * item.quantity for item in self.items)

# Service Layer (SOLID + KISS)
class CheckoutService:
    def __init__(self, inventory, payment, shipping, email):
        # Dependency injection (SOLID-D)
        self.inventory = inventory
        self.payment = payment
        self.shipping = shipping
        self.email = email
    
    def checkout(self, order):
        # Single responsibility (SOLID-S)
        # Simple flow (KISS)
        
        if not order.can_checkout():
            raise ValueError("Order cannot be checked out")
        
        # Start saga
        saga = CheckoutSaga()
        
        try:
            # Reserve inventory
            reservation = self.inventory.reserve(order.items)
            saga.add_compensation(lambda: self.inventory.release(reservation))
            
            # Process payment
            payment_id = self.payment.charge(order.total)
            saga.add_compensation(lambda: self.payment.refund(payment_id))
            
            # Create shipment
            shipment = self.shipping.create(order)
            saga.add_compensation(lambda: self.shipping.cancel(shipment))
            
            # All successful
            order.status = OrderStatus.COMPLETED
            self.email.send_confirmation(order)
            
            saga.commit()
            
        except Exception as e:
            saga.rollback()
            raise CheckoutError(f"Checkout failed: {e}")

# Simple Saga implementation (KISS)
class CheckoutSaga:
    def __init__(self):
        self.compensations = []
    
    def add_compensation(self, action):
        self.compensations.append(action)
    
    def rollback(self):
        for compensation in reversed(self.compensations):
            try:
                compensation()
            except Exception as e:
                logger.error(f"Compensation failed: {e}")
    
    def commit(self):
        self.compensations.clear()
```

## 🚨 Anti-Patterns to Avoid

### ❌ **Over-Engineering**
```python
# BAD: Factory for a factory for a builder
class UserFactoryFactoryBuilder:
    # Just use: User(name="John")
```

### ❌ **Premature Abstraction**
```python
# BAD: Interface for one implementation
class IUserService:
    pass

class UserService(IUserService):
    # Only implementation ever
```

### ❌ **Anemic Domain Models**
```python
# BAD: Logic in service, not domain
class Order:
    def __init__(self):
        self.items = []  # Just data, no behavior

class OrderService:
    def add_item(self, order, item):
        # Business logic here (wrong place)
```

### ❌ **God Objects**
```python
# BAD: Does everything
class UserManager:
    def create_user(self)
    def send_email(self)
    def process_payment(self)
    def generate_report(self)
    # ... 100 more methods
```

## ✅ Best Practices Summary

1. **Start Simple** - KISS is king
2. **Document Reasoning** - ReAct for future you
3. **Model the Domain** - Business logic in objects
4. **Inject Dependencies** - Testable and flexible
5. **Extract Duplication** - But not too early
6. **Clear Requirements** - EARS format helps

## 🎯 Final Checklist

Before submitting ANY code:
- [ ] Is this the simplest solution? (KISS)
- [ ] Is reasoning documented? (ReAct)
- [ ] Are requirements clear? (EARS)
- [ ] Single responsibility? (SOLID-S)
- [ ] Dependencies injected? (SOLID-D)
- [ ] No duplication? (DRY)
- [ ] Business logic in domain? (DDD)
- [ ] Can a junior understand this?

Remember: **Perfect is the enemy of good**. Ship simple, working code. You can always refactor later when requirements are clearer!