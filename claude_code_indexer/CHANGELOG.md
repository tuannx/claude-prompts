# Changelog

All notable changes to this project will be documented in this file.

## [1.2.1] - 2024-01-16

### Fixed
- Fixed `--important` query returning no results due to low importance scores
- Improved importance score calculation with type-based boosting
- Added smart fallback to show classes and functions when no high-scoring nodes exist
- Priority sorting now considers both node type and importance score

### Changed
- Classes get +0.3 importance boost
- Functions get +0.1 importance boost  
- Nodes with many connections get additional boost
- Importance scores are now normalized better (multiplied by 2)

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2024-01-16

### Changed
- **IMPORTANT**: Updated CLAUDE.md template to clearly indicate that the package is already implemented
- Added warning to prevent Claude Code from re-implementing existing functionality
- Simplified instructions to focus on using CLI commands only

## [1.0.1] - 2024-01-16

### Added
- Auto-update functionality with `claude-code-indexer update` command
- CLAUDE.md synchronization with `claude-code-indexer sync` command
- Update notifications on CLI startup
- Support for Python 3.12
- packaging dependency for version comparison

### Changed
- Updated project URLs to use anthropics organization
- Improved package metadata for PyPI

### Fixed
- Template path resolution in package installation

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Code indexing with graph database using Ensmallen
- CLI commands: init, index, query, search, stats
- SQLite database for persistent storage
- Node importance scoring with PageRank and centrality
- Relevance tagging for code entities
- Auto-append to CLAUDE.md on initialization
- Rich terminal interface with tables and progress bars