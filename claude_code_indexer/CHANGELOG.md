# Changelog

## [1.24.2] - 2025-08-28

### Fixed
- Removed references to deleted god_mode module in CLI
- Fixed MCP server import errors (feedback_tool, error_tracker)
- Cleaned up orphaned files and empty directories

### Improved
- Project cleanup: removed 300+ unused files
- Reduced technical debt by removing deprecated modules
- Better error handling in MCP server

### Performance
- Maintained indexing speed: 30+ files/sec
- Graph building: 3901 edges for 112 files project
- Cache hit rate: 99%+ for unchanged files

## [1.24.1] - Previous release
- Multi-language code indexing with graph database
- Support for Python, JavaScript, TypeScript, Java, AutoIt
- MCP integration for Claude Desktop
- Parallel processing with auto-detection of CPU cores