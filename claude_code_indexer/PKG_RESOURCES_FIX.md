# Fix pkg_resources Deprecation Warning

## ✅ Fixed: Replaced deprecated pkg_resources with importlib.metadata

### Problem
```
UserWarning: pkg_resources is deprecated as an API. 
The pkg_resources package is slated for removal as early as 2025-11-30.
```

### Solution
Replaced `pkg_resources` with modern `importlib.metadata`:

```python
# Old (deprecated)
import pkg_resources
version = pkg_resources.get_distribution("claude-code-indexer").version

# New (modern)
from importlib.metadata import version as get_version
version = get_version("claude-code-indexer")
```

### Implementation
- Updated `github_reporter.py` to use `importlib.metadata`
- Added fallback for Python < 3.8 using `importlib_metadata`
- No other files were using pkg_resources

### Result
- ✅ No more deprecation warning
- ✅ Future-proof (pkg_resources removal in late 2025)
- ✅ Backward compatible with older Python versions

### Testing
```bash
# Before: Shows pkg_resources warning
cci --version

# After: Clean output, no warning!
cci --version
```

The warning is now completely eliminated! 🎉