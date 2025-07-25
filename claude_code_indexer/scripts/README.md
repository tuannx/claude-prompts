# Scripts Directory

This directory contains utility, testing, and development scripts for claude-code-indexer.

## Categories

### Benchmarking & Performance
- `benchmark_*.py` - Various benchmarking scripts
- `*performance*.py` - Performance testing scripts
- `profile_*.py` - Profiling scripts for optimization
- `simple_speed_test.sh` - Simple speed testing

### Testing & Debugging
- `test_*.py` - Various test scripts (not unit tests)
- `debug_*.py` - Debugging utilities
- `run_tests.py` - Test runner utility

### Build & Publishing
- `build.sh` - Build script (use `publish.sh` in root instead)
- `publish_pypirc.sh` - PyPI configuration helper

### Utilities
- `demo_god_mode.sh` - Demo script for god mode feature
- `optimized_search.py` - Search optimization experiments
- `fast_search.py` - Fast search implementation

## Important Note

**For publishing, always use `/publish.sh` in the root directory.**

This script includes:
- Pre-publish tests
- Version checking
- Build process
- Safety checks

Never publish directly without running the main publish script!