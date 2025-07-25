# LLM Memory Storage Guide

## Overview

The LLM Memory Storage system allows Language Models (like Claude) to store and retrieve their own analysis, insights, and contextual understanding as persistent memory attached to code nodes. This enables LLMs to build cumulative knowledge about codebases over time.

## Key Features

### 🧠 Persistent Memory
- Store analysis, insights, TODOs, warnings, and contextual notes
- Build up understanding over multiple sessions
- Tag and categorize memories for easy retrieval

### 🔍 Flexible Retrieval
- Search memories by content, type, tags, or node
- Get comprehensive summaries by node
- Filter by LLM name or session

### 🏷️ Rich Metadata
- Structured metadata (JSON)
- Tag-based categorization
- Session isolation for different conversations

## Memory Types

### Core Types
- **`analysis`**: Architectural analysis, design pattern detection
- **`insight`**: Security insights, performance observations
- **`todo`**: Action items, improvement suggestions  
- **`warning`**: Code quality issues, potential problems
- **`context`**: Background information, business logic explanations
- **`explanation`**: How-to guides, usage examples

## MCP Tools for Claude Desktop

### Store Memory
```
store_llm_memory(
    project_path: str,
    node_id: int,
    memory_type: str,
    content: str,
    llm_name: str = "claude",
    metadata: Optional[Dict] = None,
    tags: Optional[List[str]] = None
)
```

**Example:**
```python
# Store architectural analysis
store_llm_memory(
    project_path="/Users/dev/myproject",
    node_id=42,
    memory_type="analysis",
    content="This UserService class follows the repository pattern with dependency injection for database access.",
    tags=["architecture", "repository-pattern", "dependency-injection"]
)
```

### Retrieve Memories
```
get_llm_memories(
    project_path: str,
    node_id: Optional[int] = None,
    memory_type: Optional[str] = None,
    limit: int = 50
)
```

### Search Memories
```
search_llm_memories(
    project_path: str,
    search_term: str,
    limit: int = 30
)
```

### Node Summary
```
get_node_memory_summary(
    project_path: str,
    node_id: int
)
```

## Usage Patterns

### 1. Code Review Assistant
```python
# Store security insight during code review
store_llm_memory(
    project_path=".",
    node_id=user_auth_node,
    memory_type="warning",
    content="Missing rate limiting on authentication endpoint - potential for brute force attacks",
    metadata={"severity": "high", "cve_risk": True},
    tags=["security", "authentication", "rate-limiting"]
)
```

### 2. Architecture Documentation
```python
# Document architectural decisions
store_llm_memory(
    project_path=".",
    node_id=api_gateway_node,
    memory_type="analysis",
    content="API Gateway uses NGINX for load balancing and request routing. Implements circuit breaker pattern for downstream service failures.",
    tags=["architecture", "api-gateway", "circuit-breaker"]
)
```

### 3. Performance Optimization Tracking
```python
# Track performance improvements
store_llm_memory(
    project_path=".",
    node_id=database_layer_node,
    memory_type="todo",
    content="Implement connection pooling to reduce database connection overhead. Current implementation creates new connections per request.",
    metadata={"priority": "medium", "estimated_effort": "2-3 days"},
    tags=["performance", "database", "connection-pooling"]
)
```

### 4. Bug Investigation
```python
# Document bug analysis
store_llm_memory(
    project_path=".",
    node_id=payment_processor_node,
    memory_type="insight",
    content="Payment failures occur when timeout is <30s. Stripe webhook requires 30s minimum timeout. Fixed by increasing timeout to 45s.",
    metadata={"bug_id": "PAY-2024-001", "fix_applied": True},
    tags=["bug-fix", "payment", "webhook", "timeout"]
)
```

## Best Practices

### 1. Consistent Tagging
Use consistent tag patterns:
- `security-*`: security-critical, security-review-needed
- `performance-*`: performance-critical, performance-bottleneck  
- `architecture-*`: architecture-decision, architecture-pattern
- `bug-*`: bug-potential, bug-fixed, bug-investigation

### 2. Structured Metadata
Include useful metadata for filtering and sorting:
```python
metadata = {
    "confidence": 0.9,           # How confident you are (0.0-1.0)
    "priority": "high",          # high, medium, low
    "effort": "2-3 days",        # estimated effort
    "impact": "high",            # potential impact
    "author": "claude-3-opus",   # which model version
    "review_needed": True        # requires human review
}
```

### 3. Memory Hygiene
- Use specific, actionable content
- Include context and reasoning
- Update outdated memories
- Clean up resolved TODOs

### 4. Session Management
Use session IDs to isolate different conversations:
```python
store_llm_memory(
    ...,
    session_id="code-review-2024-01-15"
)
```

## Integration with Claude Code

### MCP Server Integration
The LLM Memory Storage is fully integrated with the MCP server, allowing Claude Desktop to:

1. **Store insights during code analysis**
2. **Retrieve previous analysis for context**
3. **Build cumulative understanding**
4. **Track decisions and improvements**

### Usage in CLAUDE.md
Add memory storage instructions to your CLAUDE.md:

```markdown
## LLM Memory Usage

When analyzing code:
1. Store architectural insights with `store_llm_memory`
2. Mark security concerns with appropriate tags
3. Document performance observations
4. Track improvement suggestions as TODOs

Retrieve context with `get_llm_memories` before providing analysis.
```

## Example Workflow

```python
# 1. Analyze a new component
analysis = analyze_component(node_id=123)

# 2. Store the analysis
store_llm_memory(
    project_path=".",
    node_id=123,
    memory_type="analysis",
    content=analysis,
    tags=["new-component", "architecture"]
)

# 3. Later, retrieve context
memories = get_llm_memories(project_path=".", node_id=123)

# 4. Build on previous understanding
enhanced_analysis = build_on_previous_analysis(memories, new_observations)

# 5. Update memory
store_llm_memory(
    project_path=".",
    node_id=123,
    memory_type="analysis", 
    content=enhanced_analysis,  # This updates the existing memory
    tags=["architecture", "updated"]
)
```

## API Reference

### LLMMemoryStorage Class

#### `store_memory(node_id, llm_name, memory_type, content, metadata=None, session_id=None, tags=None)`
Store a memory entry.

#### `get_memories(node_id=None, memory_type=None, llm_name=None, session_id=None, tags=None, limit=100)`
Retrieve memories with filters.

#### `search_memories(search_term, limit=50)`
Search memories by content.

#### `get_node_summary(node_id)`
Get comprehensive summary for a node.

#### `get_related_memories(node_id, relationship_types)`
Get memories from related nodes.

#### `cleanup_old_memories(days_old=30, keep_important=True)`
Clean up old memories.

## Benefits

### For LLMs
- **Persistent context** across sessions
- **Cumulative learning** about codebases
- **Better recommendations** based on history
- **Consistent analysis** patterns

### For Developers  
- **AI-powered documentation** that grows over time
- **Automated code review** insights
- **Architecture decision tracking**
- **Performance optimization guidance**

### For Teams
- **Knowledge sharing** through AI insights
- **Consistent code quality** standards
- **Architectural guidance** for new team members
- **Technical debt tracking**

## Security & Privacy

- **Local storage**: All memories stored in local SQLite database
- **No external calls**: No data sent to external services
- **User control**: Complete control over what gets stored
- **Easy cleanup**: Simple commands to remove old memories

The LLM Memory Storage system transforms CCI from a simple code indexer into an intelligent knowledge base that grows smarter with every interaction!