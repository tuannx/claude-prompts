#!/bin/bash
echo "=== GOD Mode Demo Script ==="
echo ""

# 1. Check initial status
echo "1. Checking initial status..."
echo "----------------------------"
claude-code-indexer god-mode status
echo ""

# 2. Enable GOD mode
echo "2. Enabling GOD mode..."
echo "----------------------"
echo "y" | claude-code-indexer god-mode enable
echo ""

# 3. Execute some tasks
echo "3. Executing multi-agent tasks..."
echo "--------------------------------"
claude-code-indexer god-mode execute "Create REST API for user management"
echo ""
sleep 2

claude-code-indexer god-mode execute "Refactor database connection module"
echo ""
sleep 2

claude-code-indexer god-mode execute "Add real-time notification system"
echo ""

# 4. Check audit log
echo "4. Checking audit log..."
echo "-----------------------"
echo "Last 5 entries:"
tail -5 ~/.god-mode/audit.log | jq .
echo ""

# 5. Show final status with token usage
echo "5. Final status..."
echo "-----------------"
claude-code-indexer god-mode status
echo ""

# 6. Disable GOD mode
echo "6. Disabling GOD mode..."
echo "-----------------------"
claude-code-indexer god-mode stop
echo ""

echo "=== Demo completed! ==="
echo "Check full audit log at: ~/.god-mode/audit.log"
echo "Config file at: ~/.god-mode/config.yaml"