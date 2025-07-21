Feature: High-Performance Memory Cache with Auto-Expiration
  As a developer using claude-code-indexer
  I want a fast in-memory cache with automatic expiration
  So that frequently accessed data loads instantly without memory bloat

  Background:
    Given I have a memory cache with 100MB size limit
    And the default TTL is 3 days
    And the cache has entity-specific policies configured

  Scenario: Cache 5000 entries efficiently
    Given I prepare 5000 test entries of various sizes
    When I cache all 5000 entries
    Then the cache should complete within 2 seconds
    And the memory usage should not exceed 100MB
    And the cache statistics should show correct entry count
    And the hit rate for immediate retrieval should be 100%

  Scenario: LRU eviction under memory pressure
    Given I have filled the cache to 90MB capacity
    When I add new entries totaling 20MB
    Then the least recently used entries should be evicted
    And the total memory usage should remain under 100MB
    And the eviction count should be tracked correctly
    And the most recently used entries should remain cached

  Scenario: Auto-expiration after TTL
    Given I cache 100 entries with 1 second TTL
    When I wait for 2 seconds
    And I run the cleanup process
    Then all 100 entries should be expired
    And the memory should be fully reclaimed
    And the expiration count should equal 100

  Scenario: Entity-specific cache policies
    Given I have different TTL policies per entity type:
      | entity_type | ttl_days | max_size_mb |
      | file        | 7.0      | 10.0        |
      | function    | 3.0      | 5.0         |
      | class       | 5.0      | 8.0         |
      | import      | 1.0      | 2.0         |
    When I cache entities of each type
    Then each entity should use its specific TTL
    And oversized entities should be rejected
    And the cache should track entities by type

  Scenario: Access-based TTL refresh
    Given I cache an entry with 3-day access TTL
    When I access the entry after 2 days
    And I wait another 2 days
    Then the entry should still be in cache
    And the access count should be 2
    And the last accessed time should be updated

  Scenario: Thread-safe concurrent operations
    Given I have 10 concurrent threads
    When each thread performs 500 cache operations
    Then all 5000 operations should complete successfully
    And there should be no race conditions
    And the final cache state should be consistent
    And no memory corruption should occur

  Scenario: Cache statistics accuracy
    Given I perform the following operations:
      | operation | count |
      | put       | 1000  |
      | get_hit   | 800   |
      | get_miss  | 200   |
      | eviction  | 50    |
      | expiration| 30    |
    Then the statistics should show:
      | metric      | value |
      | hits        | 800   |
      | misses      | 200   |
      | hit_rate    | 80.0  |
      | evictions   | 50    |
      | expirations | 30    |

  Scenario: Memory size estimation accuracy
    Given I have objects of known sizes:
      | object_type | size_mb |
      | small_dict  | 0.001   |
      | medium_list | 0.1     |
      | large_data  | 5.0     |
      | complex_obj | 10.0    |
    When I cache these objects
    Then the estimated sizes should be within 10% of actual
    And the total cache size should be accurately tracked

  Scenario: Cache warming from disk
    Given I have 500 entries in disk cache
    And the memory cache is empty
    When I warm the memory cache with top 100 entries
    Then the memory cache should contain 100 entries
    And subsequent gets should hit memory cache
    And the warming should complete within 1 second

  Scenario: Graceful degradation under load
    Given the cache is at 95% capacity
    When I rapidly add 1000 new entries
    Then the cache should maintain stability
    And evictions should keep memory under limit
    And performance should degrade gracefully
    And no errors should be thrown