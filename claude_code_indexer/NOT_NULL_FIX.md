# Fix NOT NULL Constraint Failed for code_nodes.name

## ✅ Fixed: Node names validation and defaults

### Problem
```
Warning: Could not insert node 9: NOT NULL constraint failed: code_nodes.name
Error: Could not insert node 9 even with fallback: NOT NULL constraint failed: code_nodes.name
```

Some nodes were being created with `None` or empty names, causing database insertion to fail.

### Root Causes
1. Some parsers might create nodes with `None` names
2. When referencing `class_node.name` where class_node might have null name
3. No validation before database insertion

### Solution - Two-layer protection:

#### 1. Parser Level (base_parser.py)
```python
# Validate name in _create_node method
if not name or name == 'None' or (isinstance(name, str) and not name.strip()):
    # Generate meaningful default name
    file_name = Path(path).name if path else 'unknown'
    name = f"{node_type}_{node_id}_in_{file_name}"
```

#### 2. Database Level (indexer.py)
```python
# Validate before insertion
node_name = node_info.get('name', '').strip()
if not node_name:
    # Generate default based on node type and ID
    node_name = f"{node_info.get('node_type', 'unknown')}_{node_id}"
    log_warning(f"Node {node_id} has no name, using default: {node_name}")
```

### Benefits
- ✅ No more NOT NULL constraint errors
- ✅ Meaningful default names for debugging
- ✅ Warnings logged for troubleshooting
- ✅ Both primary and fallback insertions protected

### Testing
The fix ensures:
1. Nodes always have valid names
2. Database insertions don't fail
3. Default names are descriptive (e.g., `function_123_in_app.js`)

The error should no longer appear in indexing output!