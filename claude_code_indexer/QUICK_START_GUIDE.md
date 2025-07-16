# 🚀 Quick Start: Enhance Your CLAUDE.md for Maximum Performance

## Why Update Your CLAUDE.md?

Claude Code Indexer gives Claude **instant project understanding** with:
- **64.6x faster** context loading (0.07s vs 4.66s)
- **Smart code ranking** - Most important code shown first
- **Relationship awareness** - How components connect
- **Change detection** - What's new since last session

## 🎯 Add This to Your CLAUDE.md

Add this section at the **TOP** of your existing CLAUDE.md file:

```markdown
## 🚀 MANDATORY: Start Every Session with Code Indexing

### ⚡ FIRST THING TO DO IN EVERY SESSION:
```bash
# 1. Check if project is indexed (takes 0.1s)
claude-code-indexer stats

# 2. If not indexed or outdated, run indexing (uses cache, very fast)
claude-code-indexer index . --workers 4

# 3. Load project context into memory
claude-code-indexer query --important --limit 20
```

### 📊 Why This is CRITICAL:
- **64.6x faster** than reading files manually
- **Instant understanding** of project structure
- **Smart prioritization** - See most important code first
- **Change awareness** - Know what was modified
```

## 🔧 One-Time Setup

```bash
# 1. Install the indexer
pip install claude-code-indexer

# 2. Initialize in your project (auto-updates CLAUDE.md)
claude-code-indexer init

# 3. Run first indexing
claude-code-indexer index . --workers 4
```

## 📈 Expected Performance Gains

| Task | Without Indexer | With Indexer | Speedup |
|------|----------------|--------------|---------|
| Load project context | 5-10s | 0.1s | 50-100x |
| Search for code | 2-5s | 0.05s | 40-100x |
| Find important files | Trial & error | Instant | ∞ |
| Re-analyze after changes | 5-10s | 0.07s | 64.6x |

## 💡 Pro Tips

1. **Always start sessions with `claude-code-indexer stats`**
2. **Use `search` instead of grep/find** - It's graph-aware
3. **Trust the importance scores** - PageRank knows what matters
4. **Re-index after major changes** - It's instant with cache

## 🎯 Example Workflow

```bash
# Start of session
$ claude-code-indexer stats
📊 Project has 500 files, 2000 functions, last indexed 2 min ago

# See what's important
$ claude-code-indexer query --important --limit 10
🔍 Top components: MainApp, DatabaseManager, AuthService...

# Search for feature
$ claude-code-indexer search "payment"
📍 Found: PaymentProcessor, handle_payment(), Payment model...

# After making changes
$ claude-code-indexer index .
⚡ Re-indexed in 0.2s (498 cached, 2 updated)
```

## 🚨 Common Mistakes to Avoid

❌ **DON'T** skip initial indexing - You lose 64.6x speed boost  
❌ **DON'T** use traditional search - Graph search is smarter  
❌ **DON'T** manually read many files - Let importance guide you  
❌ **DON'T** disable cache - It's the secret to speed  

✅ **DO** run `stats` at session start  
✅ **DO** use `query --important` for context  
✅ **DO** leverage `search` for finding code  
✅ **DO** re-index after changes (it's fast!)  

---

**Remember:** The 5 seconds you spend running `claude-code-indexer stats` at the start saves 5+ minutes of context loading throughout your session!