#!/bin/bash

echo "🚀 Claude Code Indexer v1.20.0 - Speed Test"
echo "==========================================="

# Ensure indexed
echo -e "\n📦 Ensuring project is indexed..."
claude-code-indexer index . > /dev/null 2>&1

# Function to measure time
measure_time() {
    local start=$(date +%s%N)
    "$@" > /dev/null 2>&1
    local end=$(date +%s%N)
    echo $(( ($end - $start) / 1000000 ))  # Convert to milliseconds
}

echo -e "\n🔍 Search Performance Tests:"
echo "----------------------------"

# Test different search queries
queries=("search" "index" "cache" "test" "migration" "FTS5" "performance")

echo -e "\nSingle keyword searches:"
for query in "${queries[@]}"; do
    time_ms=$(measure_time claude-code-indexer search "$query")
    echo "  '$query': ${time_ms}ms"
done

echo -e "\nMulti-keyword searches:"
time_ms=$(measure_time claude-code-indexer search index cache)
echo "  'index cache': ${time_ms}ms"

time_ms=$(measure_time claude-code-indexer search search performance)
echo "  'search performance': ${time_ms}ms"

time_ms=$(measure_time claude-code-indexer search FTS5 migration database)
echo "  'FTS5 migration database': ${time_ms}ms"

# Test cache performance
echo -e "\n💾 Cache Performance Test:"
echo "-------------------------"
echo "Running same search 3 times..."

for i in 1 2 3; do
    time_ms=$(measure_time claude-code-indexer search cache performance test)
    echo "  Run $i: ${time_ms}ms"
done

# Check database stats
echo -e "\n📊 Database Statistics:"
echo "----------------------"
claude-code-indexer stats | grep -E "(Total|Search|Cache|FTS5)" || echo "Stats not available"

echo -e "\n✅ Test completed!"