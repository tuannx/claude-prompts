# Đề xuất cải tiến cho Claude Code Indexer

## 1. Cải thiện Test Coverage

### Immediate Actions:
- Enable lại các MCP tests đang bị skip
- Viết unit tests cho `StorageManager` class
- Tăng coverage cho `mcp_server.py` từ 12% lên ít nhất 80%
- Thêm integration tests kiểm tra tương tác thực giữa components

### Test Strategy:
```python
# Thêm test kiểm tra method names
def test_storage_manager_interface():
    storage = StorageManager()
    assert hasattr(storage, 'get_project_dir')
    assert not hasattr(storage, 'get_project_storage_dir')
```

## 2. Local History & Learning System

### Implement Error Pattern Tracking:
```python
class ErrorHistoryTracker:
    def __init__(self):
        self.history_file = Path.home() / ".claude-code-indexer" / "error_history.json"
        
    def record_error(self, error_type, error_msg, fix_applied=None):
        # Lưu pattern lỗi và cách fix
        
    def suggest_fix(self, current_error):
        # Tìm lỗi tương tự trong lịch sử
        # Suggest fix đã áp dụng trước đó
```

### Enhance Crash Handler:
- Lưu thêm context về state trước khi crash
- Track các action dẫn đến crash
- Suggest recovery dựa trên crash patterns

## 3. Git History Integration

### Implement GitHistoryAnalyzer:
```python
class GitHistoryAnalyzer:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)
        
    def find_similar_fixes(self, error_keyword):
        # Search commits có fix tương tự
        commits = self.repo.git.log('--grep', f'fix.*{error_keyword}', '--oneline')
        return self.analyze_fix_patterns(commits)
        
    def learn_from_history(self):
        # Analyze bug fix patterns
        # Build knowledge base từ commit history
```

### Use Cases:
- Khi gặp lỗi, search git history xem đã fix tương tự chưa
- Analyze commit patterns để detect code smell
- Suggest best practices từ historical fixes

## 4. Enhanced Memory System

### Project Memory:
```python
class ProjectMemory:
    def __init__(self, project_id):
        self.memory_dir = storage.get_project_dir(project_id) / ".memory"
        
    def remember_issue(self, issue_type, context, resolution=None):
        # Lưu vấn đề đã gặp và cách giải quyết
        
    def recall_similar_issues(self, current_context):
        # Tìm vấn đề tương tự đã gặp
```

### Benefits:
- Không lặp lại lỗi đã gặp
- Học từ kinh nghiệm trước
- Cải thiện suggestions theo thời gian

## 5. Automated Learning Loop

### Workflow:
1. Detect error/issue
2. Search local history + git history
3. Suggest fixes từ historical data
4. Apply fix và record outcome
5. Update knowledge base

### Implementation Priority:
1. **High**: Fix test coverage issues
2. **High**: Implement basic error history tracking
3. **Medium**: Git history analyzer
4. **Medium**: Enhanced project memory
5. **Low**: Full learning system

## Next Steps:
1. Create GitHub issue để track việc implement các features này
2. Start với việc fix test coverage
3. Gradually build memory/learning features