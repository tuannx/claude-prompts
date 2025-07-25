#!/usr/bin/env python3
"""
Example: LLM Pattern & Best Practices Storage

This example demonstrates how LLMs can store and retrieve coding patterns,
architectural decisions, and best practices to maintain consistency across projects.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import claude_code_indexer
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_code_indexer.indexer import CodeGraphIndexer
from claude_code_indexer.pattern_memory_manager import PatternMemoryManager, PatternType, BestPracticeCategory


def demonstrate_pattern_storage():
    """Demonstrate comprehensive pattern and best practices storage."""
    
    print("🎯 LLM Pattern & Best Practices Storage Example")
    print("=" * 60)
    
    # Create a test project structure
    test_dir = Path("pattern_demo_project")
    test_dir.mkdir(exist_ok=True)
    
    # Create sample code files
    api_file = test_dir / "api_service.py"
    api_file.write_text("""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user(self, user_id: int):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/users/{user_id}")
async def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return await service.get_user(user_id)
""")
    
    security_file = test_dir / "auth_middleware.py"
    security_file.write_text("""
from functools import wraps
from flask import request, jsonify
import jwt
import time

def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    '''Rate limiting decorator'''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Rate limiting logic here
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_auth(f):
    '''Authentication decorator'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    return decorated_function
""")
    
    print(f"📁 Created demo project at: {test_dir.absolute()}")
    
    # Index the code
    print("\n📊 Indexing code...")
    indexer = CodeGraphIndexer(project_path=test_dir)
    indexer.index_directory(str(test_dir))
    
    # Initialize pattern manager
    pattern_manager = PatternMemoryManager(indexer.db_path)
    
    print("✓ Pattern manager initialized")
    
    # Store various coding patterns
    print("\n🎯 Storing Coding Patterns...")
    
    # 1. Architecture Pattern
    arch_pattern_id = pattern_manager.store_pattern(
        pattern_type=PatternType.ARCHITECTURE,
        title="Service Layer Pattern",
        description="Separate business logic into dedicated service classes that encapsulate domain operations. Services are injected with dependencies (like database connections) and handle all business rules and validations.",
        example_code="""
class UserService:
    def __init__(self, db: Session, email_service: EmailService):
        self.db = db
        self.email_service = email_service
    
    async def create_user(self, user_data: UserCreate):
        # Business logic here
        user = User(**user_data.dict())
        self.db.add(user)
        await self.email_service.send_welcome_email(user.email)
        return user
""",
        when_to_use="Use when you need to separate business logic from controllers/endpoints. Ideal for complex business rules and when you need to reuse logic across multiple controllers.",
        benefits=[
            "Clear separation of concerns",
            "Reusable business logic",
            "Easier testing with dependency injection",
            "Consistent error handling"
        ],
        trade_offs=[
            "Additional abstraction layer",
            "More files to manage",
            "Potential over-engineering for simple CRUD"
        ],
        tags=["architecture", "service-layer", "dependency-injection", "business-logic"],
        llm_name="claude-3-opus",
        confidence=0.95
    )
    
    # 2. Security Pattern
    security_pattern_id = pattern_manager.store_pattern(
        pattern_type=PatternType.SECURITY,
        title="JWT Authentication with Rate Limiting",
        description="Implement JWT-based authentication combined with rate limiting to protect API endpoints from abuse while maintaining stateless authentication.",
        example_code="""
@rate_limit(max_requests=100, window_seconds=3600)
@require_auth
@app.route('/api/sensitive-data')
def get_sensitive_data():
    user_id = request.user_id
    return get_user_data(user_id)
""",
        anti_pattern="""
# AVOID: No rate limiting or authentication
@app.route('/api/sensitive-data')
def get_sensitive_data():
    return get_all_user_data()  # Exposes all data without protection
""",
        when_to_use="Use for protecting sensitive API endpoints that require authentication and protection from abuse or brute force attacks.",
        benefits=[
            "Stateless authentication",
            "Protection against brute force",
            "Scalable across multiple servers",
            "Fine-grained access control"
        ],
        trade_offs=[
            "Token management complexity",
            "Additional middleware overhead",
            "Potential for token-based attacks if not properly secured"
        ],
        tags=["security", "jwt", "rate-limiting", "authentication", "api-protection"],
        llm_name="claude-3-opus",
        confidence=0.92
    )
    
    # 3. Error Handling Pattern
    error_pattern_id = pattern_manager.store_pattern(
        pattern_type=PatternType.ERROR_HANDLING,
        title="Structured Exception Handling with Logging",
        description="Implement consistent error handling that logs detailed error information for debugging while returning user-friendly messages to clients.",
        example_code="""
async def get_user(self, user_id: int):
    try:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        logger.error(f"Unexpected error retrieving user {user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
""",
        when_to_use="Use in all service methods and API endpoints to ensure consistent error handling and debugging capabilities.",
        benefits=[
            "Consistent error responses",
            "Detailed logging for debugging",
            "User-friendly error messages",
            "Prevents sensitive information leakage"
        ],
        tags=["error-handling", "logging", "exceptions", "debugging"],
        confidence=0.88
    )
    
    print(f"✅ Stored {3} coding patterns")
    
    # Store best practices
    print("\n⭐ Storing Best Practices...")
    
    # 1. Team Standards
    naming_practice_id = pattern_manager.store_best_practice(
        category=BestPracticeCategory.TEAM_STANDARDS,
        title="Consistent Variable and Function Naming",
        description="Use descriptive, lowercase_with_underscores naming for variables and functions. Classes should use PascalCase. Constants should be UPPER_CASE.",
        rationale="Consistent naming improves code readability and reduces cognitive load when switching between different parts of the codebase. Following Python PEP 8 standards ensures compatibility with the broader Python ecosystem.",
        examples=[
            "user_service = UserService(db_connection)",
            "MAX_RETRY_ATTEMPTS = 3",
            "def calculate_monthly_revenue(transactions: List[Transaction]) -> float:"
        ],
        counter_examples=[
            "us = UserService(db)",  # Too abbreviated
            "Calculate_Monthly_Revenue()",  # Wrong case
            "maxRetryAttempts = 3"  # camelCase instead of UPPER_CASE
        ],
        enforcement_level="must",
        scope="project",
        tools_required=["flake8", "black", "pylint"],
        tags=["naming", "pep8", "readability", "standards"],
        priority="high"
    )
    
    # 2. Security Best Practice
    security_practice_id = pattern_manager.store_best_practice(
        category=BestPracticeCategory.PROJECT_RULES,
        title="Never Log Sensitive Information",
        description="Prevent logging of passwords, API keys, personal identifiable information (PII), or any sensitive data that could compromise security if logs are exposed.",
        rationale="Logs are often stored in plain text and may be accessed by multiple team members or external services. Logging sensitive information creates security vulnerabilities and potential compliance violations.",
        examples=[
            "logger.info(f'User {user.id} authenticated successfully')",
            "logger.error(f'Failed to process payment for order {order_id}')",
            "logger.debug(f'API call to {service_name} completed in {duration}ms')"
        ],
        counter_examples=[
            "logger.info(f'User password: {password}')",
            "logger.debug(f'API key: {api_key}')",
            "logger.error(f'Database query failed: {query_with_sensitive_data}')"
        ],
        enforcement_level="must",
        scope="company",
        tools_required=["pre-commit hooks", "log analysis tools"],
        tags=["security", "logging", "pii", "compliance"],
        priority="high"
    )
    
    # 3. Code Review Practice
    review_practice_id = pattern_manager.store_best_practice(
        category=BestPracticeCategory.CODE_REVIEW,
        title="Require Tests for All New Features",
        description="Every new feature or bug fix must include corresponding unit tests with at least 80% code coverage for the modified code paths.",
        rationale="Tests ensure code quality, prevent regressions, and make refactoring safer. Writing tests alongside code development leads to better design and more reliable software.",
        examples=[
            "test_user_service_create_user_success()",
            "test_user_service_create_user_duplicate_email_fails()",
            "test_rate_limiter_blocks_excessive_requests()"
        ],
        enforcement_level="should",
        scope="team",
        tools_required=["pytest", "coverage.py", "pre-commit"],
        tags=["testing", "quality", "coverage", "ci-cd"],
        priority="high"
    )
    
    # 4. Performance Practice  
    performance_practice_id = pattern_manager.store_best_practice(
        category=BestPracticeCategory.TOOL_USAGE,
        title="Use Database Connection Pooling",
        description="Always use connection pooling for database connections to improve performance and prevent connection exhaustion under high load.",
        rationale="Creating database connections is expensive. Connection pooling reuses existing connections, reduces latency, and prevents overwhelming the database with too many concurrent connections.",
        examples=[
            "SQLAlchemy with pool_size=20, max_overflow=10",
            "Redis connection pool with max_connections=50",
            "Async database pools for high-concurrency applications"
        ],
        tools_required=["SQLAlchemy", "Redis", "asyncpg"],
        enforcement_level="should",
        scope="project",
        tags=["performance", "database", "connection-pooling", "scalability"],
        priority="medium"
    )
    
    print(f"✅ Stored {4} best practices")
    
    # Demonstrate retrieval and search
    print("\n🔍 Demonstrating Pattern & Practice Retrieval...")
    
    # Get all security-related patterns
    security_patterns = pattern_manager.get_patterns(
        pattern_type=PatternType.SECURITY,
        tags=["security"]
    )
    print(f"\n🛡️ Security Patterns ({len(security_patterns)} found):")
    for pattern in security_patterns:
        print(f"  • {pattern['title']} (confidence: {pattern['confidence']:.2f})")
    
    # Get high-priority best practices
    high_priority_practices = pattern_manager.get_best_practices(priority="high")
    print(f"\n🚨 High Priority Practices ({len(high_priority_practices)} found):")
    for practice in high_priority_practices:
        print(f"  • {practice['title']} ({practice['enforcement_level']})")
    
    # Search across both patterns and practices
    auth_results = pattern_manager.search_patterns_and_practices("authentication")
    print(f"\n🔍 Search Results for 'authentication':")
    print(f"  Patterns: {len(auth_results['patterns'])}")
    print(f"  Practices: {len(auth_results['best_practices'])}")
    
    # Get project standards summary
    print("\n📊 Project Standards Summary:")
    summary = pattern_manager.get_project_standards_summary()
    stats = summary['summary']
    print(f"  • Total Patterns: {stats['total_patterns']}")
    print(f"  • Total Practices: {stats['total_practices']}")
    print(f"  • Avg Pattern Confidence: {stats['avg_pattern_confidence']:.2f}")
    print(f"  • Avg Practice Compliance: {stats['avg_practice_compliance']:.2f}")
    
    # Show pattern recommendations (simulate)
    print(f"\n💡 Pattern Usage Tracking:")
    
    # Record pattern usage
    pattern_manager.record_pattern_usage(
        pattern_id=arch_pattern_id,
        file_path="api_service.py",
        usage_context="Applied service layer pattern to UserService",
        effectiveness_score=0.9,
        notes="Successfully separated business logic from API endpoints"
    )
    
    pattern_manager.record_pattern_usage(
        pattern_id=security_pattern_id,
        file_path="auth_middleware.py", 
        usage_context="Implemented JWT auth with rate limiting",
        effectiveness_score=0.85,
        notes="Reduced unauthorized access attempts by 95%"
    )
    
    print("  ✅ Recorded pattern usage for tracking effectiveness")
    
    # Get updated patterns to show usage frequency
    updated_patterns = pattern_manager.get_patterns(limit=5)
    print(f"\n📈 Pattern Usage Statistics:")
    for pattern in updated_patterns:
        if pattern['usage_frequency'] > 0:
            print(f"  • {pattern['title']}: used {pattern['usage_frequency']} times")
    
    print("\n✅ Pattern & Best Practices Storage demonstration complete!")
    print("\nThis shows how LLMs can build up a comprehensive knowledge base of:")
    print("  🎯 Proven coding patterns with examples and trade-offs")
    print("  ⭐ Best practices with enforcement levels and rationale")
    print("  📊 Usage tracking for pattern effectiveness")
    print("  🔍 Search and retrieval for consistent application")
    print("  📈 Project standards evolution over time")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    print(f"\n🧹 Cleaned up demo directory: {test_dir}")


if __name__ == "__main__":
    demonstrate_pattern_storage()