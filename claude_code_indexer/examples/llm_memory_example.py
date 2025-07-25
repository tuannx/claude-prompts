#!/usr/bin/env python3
"""
Example: LLM Memory Storage with Claude Code Indexer

This example demonstrates how LLMs like Claude can store and retrieve
their own analysis, insights, and context as memory attached to code nodes.

This enables persistent understanding that builds up over time.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import claude_code_indexer
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_code_indexer.indexer import CodeGraphIndexer
from claude_code_indexer.llm_memory_storage import LLMMemoryStorage


def demonstrate_llm_memory():
    """Demonstrate LLM memory storage capabilities."""
    
    print("🧠 LLM Memory Storage Example")
    print("=" * 50)
    
    # Create a test project structure
    test_dir = Path("test_project")
    test_dir.mkdir(exist_ok=True)
    
    # Create a simple Python file to analyze
    test_file = test_dir / "user_service.py"
    test_file.write_text("""
class UserService:
    '''Service class for managing user operations'''
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache = {}
    
    def authenticate_user(self, username, password):
        '''Authenticate user credentials'''
        if not username or not password:
            raise ValueError("Username and password required")
        
        user = self.db.find_user(username)
        if user and user.verify_password(password):
            return user
        return None
    
    def create_user(self, user_data):
        '''Create a new user account'''
        if self.db.user_exists(user_data['email']):
            raise ValueError("User already exists")
        
        return self.db.create_user(user_data)
    
    def get_user_profile(self, user_id):
        '''Get user profile with caching'''
        if user_id in self.cache:
            return self.cache[user_id]
        
        profile = self.db.get_user_profile(user_id)
        self.cache[user_id] = profile
        return profile
""")
    
    print(f"📁 Created test project at: {test_dir.absolute()}")
    
    # Index the code
    print("\n📊 Indexing code...")
    indexer = CodeGraphIndexer(project_path=test_dir)
    indexer.index_directory(str(test_dir))
    
    # Initialize LLM memory storage
    memory_storage = LLMMemoryStorage(indexer.db_path)
    
    # Get indexed nodes
    stats = indexer.get_stats()
    print(f"✓ Indexed {stats.get('total_nodes', 0)} nodes")
    
    # Find the UserService class node
    important_nodes = indexer.query_important_nodes(limit=10)
    user_service_node = None
    
    for node in important_nodes:
        if node['name'] == 'UserService':
            user_service_node = node
            break
    
    if not user_service_node:
        print("❌ Could not find UserService node")
        return
    
    node_id = user_service_node['id']
    print(f"\n🎯 Found UserService node (ID: {node_id})")
    
    # Simulate Claude storing various types of memories
    print("\n🤖 Claude storing analysis memories...")
    
    # 1. Architecture Analysis
    memory_storage.store_memory(
        node_id=node_id,
        llm_name="claude-3-opus",
        memory_type="analysis",
        content="""This UserService class follows a typical service layer pattern. It encapsulates user-related business logic and provides a clean interface for user operations. The class uses dependency injection for the database connection, which is good for testability and separation of concerns.""",
        metadata={"confidence": 0.92, "analysis_type": "architectural"},
        tags=["architecture", "service-layer", "dependency-injection"]
    )
    
    # 2. Security Insight
    memory_storage.store_memory(
        node_id=node_id,
        llm_name="claude-3-opus",
        memory_type="insight",
        content="""Security consideration: The authenticate_user method should implement rate limiting and account lockout mechanisms to prevent brute force attacks. Also consider using secure password hashing with salt.""",
        metadata={"priority": "high", "category": "security"},
        tags=["security", "authentication", "vulnerability"]
    )
    
    # 3. Performance TODO
    memory_storage.store_memory(
        node_id=node_id,
        llm_name="claude-3-opus",
        memory_type="todo",
        content="""Performance optimization needed: The get_user_profile method uses a simple dictionary cache, but this could lead to memory leaks in long-running applications. Consider implementing an LRU cache with size limits.""",
        metadata={"effort": "medium", "impact": "medium"},
        tags=["performance", "caching", "memory-management"]
    )
    
    # 4. Code Quality Warning
    memory_storage.store_memory(
        node_id=node_id,
        llm_name="claude-3-opus",
        memory_type="warning",
        content="""Code quality issue: The create_user method should validate the user_data structure before attempting to create the user. Missing input validation could lead to runtime errors.""",
        metadata={"severity": "medium"},
        tags=["validation", "error-handling", "robustness"]
    )
    
    print("✓ Stored 4 memory entries")
    
    # Demonstrate memory retrieval
    print("\n📖 Retrieving memories...")
    
    # Get all memories for this node
    all_memories = memory_storage.get_memories(node_id=node_id)
    print(f"Total memories for UserService: {len(all_memories)}")
    
    # Get memories by type
    print("\n🔍 Memories by type:")
    for memory_type in ["analysis", "insight", "todo", "warning"]:
        memories = memory_storage.get_memories(node_id=node_id, memory_type=memory_type)
        if memories:
            print(f"\n{memory_type.upper()}:")
            for memory in memories:
                print(f"  • {memory['content'][:100]}...")
                if memory.get('tags'):
                    print(f"    Tags: {', '.join(memory['tags'])}")
    
    # Demonstrate search functionality
    print("\n🔍 Searching memories...")
    
    security_memories = memory_storage.search_memories("security")
    print(f"\nFound {len(security_memories)} memories about 'security':")
    for memory in security_memories:
        print(f"  • [{memory['memory_type']}] {memory['content'][:80]}...")
    
    performance_memories = memory_storage.search_memories("performance")
    print(f"\nFound {len(performance_memories)} memories about 'performance':")
    for memory in performance_memories:
        print(f"  • [{memory['memory_type']}] {memory['content'][:80]}...")
    
    # Get comprehensive summary
    print("\n📋 Memory Summary:")
    summary = memory_storage.get_node_summary(node_id)
    print(f"Total memories: {summary['total_memories']}")
    print(f"Types: {list(summary['by_type'].keys())}")
    print(f"LLMs: {list(summary['by_llm'].keys())}")
    print(f"Tags: {', '.join(summary['tags'])}")
    
    # Simulate updating existing memory
    print("\n🔄 Updating existing memory...")
    memory_storage.store_memory(
        node_id=node_id,
        llm_name="claude-3-opus",
        memory_type="analysis",
        content="""UPDATED: This UserService class follows a typical service layer pattern with good separation of concerns. The class demonstrates proper dependency injection and encapsulates user business logic effectively. However, it could benefit from implementing proper error handling and input validation throughout all methods.""",
        metadata={"confidence": 0.95, "analysis_type": "architectural", "updated": True},
        tags=["architecture", "service-layer", "dependency-injection", "updated"]
    )
    
    # Verify update
    updated_memories = memory_storage.get_memories(node_id=node_id, memory_type="analysis")
    print("✓ Memory updated - should still have only 1 analysis entry")
    print(f"Updated content: {updated_memories[0]['content'][:100]}...")
    
    # Demonstrate tag-based retrieval
    print("\n🏷️ Retrieving by tags...")
    security_tagged = memory_storage.get_memories(tags=["security"])
    performance_tagged = memory_storage.get_memories(tags=["performance"])
    
    print(f"Memories tagged 'security': {len(security_tagged)}")
    print(f"Memories tagged 'performance': {len(performance_tagged)}")
    
    print("\n✅ LLM Memory Storage demonstration complete!")
    print("\nThis shows how LLMs can build persistent understanding of code")
    print("by storing analysis, insights, TODOs, and warnings that accumulate")
    print("over time, creating a knowledge base about the codebase.")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    print(f"\n🧹 Cleaned up test directory: {test_dir}")


if __name__ == "__main__":
    demonstrate_llm_memory()