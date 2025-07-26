# Architecture Guidelines - Avoiding Circular Dependencies

## 1. Dependency Rules

### Layer Dependencies
```
CLI/API → Services → Core → Infrastructure
         ↘         ↙
          Interfaces
```

- **CLI/API Layer**: Only imports from Services
- **Services Layer**: Imports from Core and Interfaces
- **Core Layer**: Imports from Interfaces only
- **Infrastructure Layer**: Implements Interfaces
- **Interfaces**: No imports (pure abstractions)

## 2. Common Anti-patterns to Avoid

### ❌ Circular Import
```python
# file: indexer.py
from .cli import CLI

# file: cli.py
from .indexer import Indexer  # Circular!
```

### ✅ Solution: Dependency Injection
```python
# file: indexer.py
class Indexer:
    # No import of CLI

# file: cli.py
from .indexer import Indexer

class CLI:
    def __init__(self, indexer: Indexer):
        self.indexer = indexer
```

## 3. Design Patterns for Clean Architecture

### Factory Pattern
```python
# factories/parser_factory.py
from interfaces import IParser
from parsers import PythonParser, JavaParser

class ParserFactory:
    @staticmethod
    def create_parser(language: str) -> IParser:
        if language == "python":
            return PythonParser()
        elif language == "java":
            return JavaParser()
```

### Repository Pattern
```python
# interfaces/repository_interface.py
class INodeRepository(ABC):
    @abstractmethod
    def save(self, node: CodeNode) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[CodeNode]:
        pass

# infrastructure/node_repository.py
from interfaces import INodeRepository

class SQLiteNodeRepository(INodeRepository):
    def save(self, node: CodeNode) -> None:
        # Implementation
        pass
```

### Service Layer Pattern
```python
# services/indexing_service.py
from interfaces import IParser, INodeRepository

class IndexingService:
    def __init__(self, parser: IParser, repository: INodeRepository):
        self.parser = parser
        self.repository = repository
    
    def index_file(self, file_path: str) -> None:
        # Use parser and repository
        pass
```

## 4. Dependency Injection Container

```python
# di_container.py
class DIContainer:
    def __init__(self):
        self._services = {}
        self._singletons = {}
    
    def register(self, interface, implementation, singleton=False):
        self._services[interface] = (implementation, singleton)
    
    def resolve(self, interface):
        implementation, is_singleton = self._services[interface]
        
        if is_singleton:
            if interface not in self._singletons:
                self._singletons[interface] = implementation()
            return self._singletons[interface]
        
        return implementation()

# Usage
container = DIContainer()
container.register(IParser, PythonParser, singleton=True)
container.register(INodeRepository, SQLiteNodeRepository)

# In your service
parser = container.resolve(IParser)
```

## 5. Import Organization

### Import Order
```python
# 1. Standard library imports
import os
import sys
from typing import List, Optional

# 2. Third-party imports
import click
import networkx as nx

# 3. Local application imports (absolute)
from claude_code_indexer.interfaces import IParser
from claude_code_indexer.models import CodeNode
from claude_code_indexer.core import GraphBuilder

# 4. Relative imports (minimize these)
from .utils import helpers
```

## 6. Testing Without Circular Dependencies

```python
# tests/test_indexer.py
from unittest.mock import Mock
from claude_code_indexer.interfaces import IParser
from claude_code_indexer.core import Indexer

def test_indexer():
    # Mock dependencies
    mock_parser = Mock(spec=IParser)
    mock_parser.parse.return_value = ParseResult(...)
    
    # Test without circular imports
    indexer = Indexer(parser=mock_parser)
    result = indexer.index("test.py")
    
    assert result is not None
```

## 7. Configuration Without Circular Imports

```python
# config.py
from dataclasses import dataclass

@dataclass
class Config:
    db_path: str
    cache_size: int
    workers: int

# app.py
from config import Config
from di_container import DIContainer

def create_app(config: Config):
    container = DIContainer()
    # Register all services
    return container
```

## 8. Event System for Decoupling

```python
# events/event_bus.py
class EventBus:
    def __init__(self):
        self._handlers = {}
    
    def subscribe(self, event_type: str, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def publish(self, event_type: str, data):
        for handler in self._handlers.get(event_type, []):
            handler(data)

# Usage - no direct coupling
event_bus = EventBus()
event_bus.subscribe("file_indexed", lambda data: print(f"Indexed: {data}"))
event_bus.publish("file_indexed", {"file": "test.py"})
```

## 9. Checklist for New Modules

- [ ] Module only imports from lower layers
- [ ] No imports from CLI/API layer
- [ ] Interfaces defined for external dependencies
- [ ] Dependencies injected, not created
- [ ] Unit tests use mocks, not real implementations
- [ ] No relative imports outside current package
- [ ] Clear separation of concerns

## 10. Refactoring Strategy

1. **Identify circular dependencies**
   ```bash
   python -m pydeps claude_code_indexer --show-cycles
   ```

2. **Extract interfaces**
   - Create abstract base classes
   - Move to interfaces package

3. **Implement dependency injection**
   - Constructor injection preferred
   - Use factory pattern for complex creation

4. **Test in isolation**
   - Mock all dependencies
   - Verify no import errors

5. **Gradual migration**
   - Refactor one module at a time
   - Keep tests passing throughout