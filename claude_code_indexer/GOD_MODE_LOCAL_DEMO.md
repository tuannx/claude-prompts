# Hướng dẫn Demo GOD Mode - Claude Code Indexer

## 1. Cài đặt Claude Code Indexer (nếu chưa có)

```bash
# Clone repo
git clone https://github.com/tuannx/claude-prompts.git
cd claude-prompts/claude_code_indexer

# Cài đặt package
pip install -e .

# Hoặc nếu đã có sẵn
pip install --upgrade claude-code-indexer
```

## 2. Demo GOD Mode Step-by-Step

### Bước 1: Kiểm tra trạng thái ban đầu
```bash
claude-code-indexer god-mode status
```

Output mẫu:
```
                GOD Mode Status                
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting       ┃ Value                       ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Enabled       │ ✗ No                        │
│ Auto-accept   │ ✓ Yes                       │
│ Vibecode mode │ ✓ Yes                       │
│ Config path   │ ~/.god-mode                 │
└───────────────┴─────────────────────────────┘
```

### Bước 2: Kích hoạt GOD mode
```bash
claude-code-indexer god-mode enable
```

Sẽ hiện warning và yêu cầu xác nhận:
```
╭──────────────── GOD Mode (BETA) ─────────────────╮
│ ⚡ GOD MODE ACTIVATION ⚡                        │
│                                                  │
│ WARNING: This mode enables autonomous execution! │
│ - Auto-accept ALL operations                     │
│ - Vibecode mode always ON                        │
│ - Multi-agent coordination active                │
│                                                  │
│ Safety features:                                 │
│ - Audit logging to ~/.god-mode/audit.log         │
│ - Emergency stop: god-mode --stop                │
│ - Token usage tracking                           │
╰──────────────────────────────────────────────────╯
Enable GOD mode? [y/N]: 
```

Nhập `y` để kích hoạt.

### Bước 3: Thực thi task với multi-agent
```bash
# Ví dụ 1: Tạo module authentication
claude-code-indexer god-mode execute "Create user authentication module with JWT"

# Ví dụ 2: Refactor code
claude-code-indexer god-mode execute "Refactor database connection module"

# Ví dụ 3: Add feature
claude-code-indexer god-mode execute "Add real-time notification system"
```

Output mẫu:
```
╭────────────────── Multi-Agent Execution ──────────────────╮
│ Task: Create user authentication module with JWT         │
╰──────────────────────────────────────────────────────────╯

Architect analyzing task... ━━━━━━━━━━━━━━━━━━━━━ 100%

╭────────────────────────── Architect's Plan ──────────────────────────╮
│ 1. Parse requirements                                                │
│ 2. Design solution                                                   │
│ 3. Implement code                                                    │
│ 4. Test implementation                                               │
╰─────────────────────────────────────────────────────────────────────╯

Developer implementing... ━━━━━━━━━━━━━━━━━━━━━ 100%

╭─────────────────── Developer's Implementation ───────────────────╮
│ Code implementation completed (simulation)                       │
╰─────────────────────────────────────────────────────────────────╯

✓ Multi-agent task completed!

     Token Usage      
┏━━━━━━━━━━━┳━━━━━━━━┓
┃ Agent     ┃ Tokens ┃
┡━━━━━━━━━━━╇━━━━━━━━┩
│ architect │ 150    │
│ developer │ 300    │
│ Total     │ 450    │
└───────────┴────────┘
```

### Bước 4: Kiểm tra audit log
```bash
# Xem audit log dạng JSON
cat ~/.god-mode/audit.log | jq .

# Hoặc xem raw
cat ~/.god-mode/audit.log
```

### Bước 5: Emergency stop
```bash
# Dừng khẩn cấp GOD mode
claude-code-indexer god-mode stop

# Hoặc
claude-code-indexer god-mode disable
```

## 3. File Configuration

Xem và chỉnh sửa config tại `~/.god-mode/config.yaml`:

```bash
cat ~/.god-mode/config.yaml
```

Nội dung mẫu:
```yaml
enabled: false
auto_accept: true
vibecode_mode: true
agents:
  architect:
    role: Planning and task decomposition
    model: claude-opus-4
  developer:
    role: Code implementation
    model: claude-sonnet-4
safety:
  forbidden_operations:
  - rm -rf /
  - DROP DATABASE
  - DELETE FROM users
  max_tokens_per_session: 100000
  require_confirmation:
  - production deployment
  - database migration
```

## 4. Xem Help

```bash
# Help chung
claude-code-indexer god-mode --help

# Output:
# Commands:
#   disable  Disable GOD mode (emergency stop).
#   enable   Enable GOD mode for autonomous execution.
#   execute  Execute a task using multi-agent coordination.
#   status   Show GOD mode status and statistics.
#   stop     Emergency stop for GOD mode (alias for disable).
```

## 5. Demo Script Đầy Đủ

```bash
#!/bin/bash
echo "=== GOD Mode Demo ==="

# 1. Check initial status
echo -e "\n1. Checking initial status..."
claude-code-indexer god-mode status

# 2. Enable GOD mode
echo -e "\n2. Enabling GOD mode..."
echo "y" | claude-code-indexer god-mode enable

# 3. Execute a task
echo -e "\n3. Executing multi-agent task..."
claude-code-indexer god-mode execute "Create REST API for user management"

# 4. Check audit log
echo -e "\n4. Checking audit log..."
tail -5 ~/.god-mode/audit.log | jq .

# 5. Disable GOD mode
echo -e "\n5. Disabling GOD mode..."
claude-code-indexer god-mode stop

echo -e "\n=== Demo completed! ==="
```

## Lưu ý

1. **BETA Feature**: Đây là tính năng đang phát triển
2. **Simulation**: Hiện tại chỉ là simulation, chưa gọi Claude API thật
3. **Safety**: Luôn review audit log và config trước khi sử dụng
4. **Token Usage**: Tracking token chỉ là ước tính cho POC

## Troubleshooting

1. **Lỗi import**: Đảm bảo đã cài đặt claude-code-indexer mới nhất
2. **Permission denied**: Check quyền ghi vào ~/.god-mode/
3. **YAML error**: Cài PyYAML nếu chưa có: `pip install pyyaml`

---

🎉 Have fun với GOD mode! Report issues tại: https://github.com/tuannx/claude-prompts/issues