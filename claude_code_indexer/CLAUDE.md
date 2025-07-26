## Code Indexing

### Quick Start
```bash
pip install claude-code-indexer
claude-code-indexer init
claude-code-indexer index .
claude-code-indexer query --important
```

### Commands
- `init` - Initialize project
- `index <path>` - Index codebase
- `query --important` - Show key components  
- `search <term>` - Search code
- `stats` - View statistics

### Performance
- Fast with cache
- Smart ignore patterns
- Parallel processing

### Development Workflow 🧪
When making changes to this codebase:
1. **Before changes**: Run tests to ensure baseline
   ```bash
   pytest tests/test_file.py -v  # Specific test
   pytest tests/ -v              # All tests
   ```
2. **After changes**: 
   - Run relevant tests immediately
   - Update test cases if behavior changed
   - Add tests for new features
   - Fix failures before continuing
3. **Before commit**:
   ```bash
   pytest tests/ -v              # Full test suite
   python -m build               # Build package
   pip install dist/*.whl        # Test installation
   cci --version                 # Verify it works
   ```

### Testing Commands
```bash
# Run specific test file
pytest tests/test_cli.py -v

# Run specific test
pytest tests/test_cli.py::TestCLI::test_init_command_new_project -v

# Run with coverage
pytest tests/ --cov=claude_code_indexer --cov-report=html

# Run fast tests only
pytest tests/ -v -m "not slow"

# Debug failing test
pytest tests/test_file.py -vvs --tb=short
```

## important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.