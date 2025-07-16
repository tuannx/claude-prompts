#!/usr/bin/env python3
"""
Demo analyzing code structure using graph database vs traditional search
"""

import sqlite3
import json
import time
from pathlib import Path
import subprocess

class GraphAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        
    def analyze_code_structure(self):
        """Analyze overall code structure from graph"""
        print("=== CODE STRUCTURE ANALYSIS FROM GRAPH ===\n")
        
        # 1. Get central/hub components
        cursor = self.conn.cursor()
        print("🔍 Most important components (hubs):")
        cursor.execute("""
        SELECT name, node_type, importance_score, relevance_tags
        FROM code_nodes
        WHERE importance_score > 0.01
        ORDER BY importance_score DESC
        LIMIT 10
        """)
        
        for name, node_type, score, tags in cursor.fetchall():
            tags_list = json.loads(tags) if tags else []
            print(f"  • {name} ({node_type}): {score:.3f} - {', '.join(tags_list)}")
        
        # 2. Analyze relationships
        print("\n🔗 Key relationships:")
        cursor.execute("""
        SELECT cn1.name, r.relationship_type, cn2.name
        FROM relationships r
        JOIN code_nodes cn1 ON r.source_id = cn1.id
        JOIN code_nodes cn2 ON r.target_id = cn2.id
        WHERE cn1.node_type = 'file' OR cn1.node_type = 'class'
        LIMIT 20
        """)
        
        relationships = {}
        for source, rel_type, target in cursor.fetchall():
            if source not in relationships:
                relationships[source] = []
            relationships[source].append(f"{rel_type} {target}")
        
        for source, rels in list(relationships.items())[:5]:
            print(f"  • {source}: {', '.join(rels[:3])}")
            
        # 3. Component statistics
        print("\n📊 Component statistics:")
        cursor.execute("""
        SELECT node_type, COUNT(*) as count
        FROM code_nodes
        GROUP BY node_type
        ORDER BY count DESC
        """)
        
        for node_type, count in cursor.fetchall():
            print(f"  • {node_type}: {count}")
            
    def find_related_components(self, component_name):
        """Find all components related to a specific one"""
        print(f"\n=== FINDING COMPONENTS RELATED TO '{component_name}' ===\n")
        
        cursor = self.conn.cursor()
        
        # Find the component
        cursor.execute("""
        SELECT id, node_type 
        FROM code_nodes 
        WHERE name LIKE ?
        """, (f'%{component_name}%',))
        
        results = cursor.fetchall()
        if not results:
            print(f"Component '{component_name}' not found")
            return
            
        for comp_id, node_type in results[:1]:  # Take first match
            print(f"Found: {component_name} ({node_type})")
            
            # Find directly connected components
            cursor.execute("""
            SELECT DISTINCT cn.name, cn.node_type, r.relationship_type, 'outgoing' as direction
            FROM relationships r
            JOIN code_nodes cn ON r.target_id = cn.id
            WHERE r.source_id = ?
            UNION
            SELECT DISTINCT cn.name, cn.node_type, r.relationship_type, 'incoming' as direction
            FROM relationships r
            JOIN code_nodes cn ON r.source_id = cn.id
            WHERE r.target_id = ?
            """, (comp_id, comp_id))
            
            connections = cursor.fetchall()
            print(f"\n📍 Direct connections ({len(connections)}):")
            
            incoming = [c for c in connections if c[3] == 'incoming']
            outgoing = [c for c in connections if c[3] == 'outgoing']
            
            if incoming:
                print("  Incoming (depends on this):")
                for name, node_type, rel_type, _ in incoming[:5]:
                    print(f"    ← {name} ({node_type}) via {rel_type}")
                    
            if outgoing:
                print("  Outgoing (this depends on):")
                for name, node_type, rel_type, _ in outgoing[:5]:
                    print(f"    → {name} ({node_type}) via {rel_type}")
                    
    def trace_call_path(self, from_component, to_component):
        """Try to find path between two components"""
        print(f"\n=== TRACING PATH: {from_component} → {to_component} ===\n")
        
        cursor = self.conn.cursor()
        
        # This is simplified - real implementation would use graph algorithms
        cursor.execute("""
        SELECT cn1.name, r.relationship_type, cn2.name
        FROM relationships r
        JOIN code_nodes cn1 ON r.source_id = cn1.id
        JOIN code_nodes cn2 ON r.target_id = cn2.id
        WHERE cn1.name LIKE ? OR cn2.name LIKE ?
        LIMIT 20
        """, (f'%{from_component}%', f'%{to_component}%'))
        
        paths = cursor.fetchall()
        if paths:
            print("Possible connections found:")
            for source, rel_type, target in paths[:10]:
                print(f"  {source} --{rel_type}--> {target}")
        else:
            print("No direct path found")
            
    def compare_with_traditional_search(self, search_term):
        """Compare graph search vs traditional grep search"""
        print(f"\n=== COMPARING SEARCH METHODS FOR '{search_term}' ===\n")
        
        # Graph search
        start_time = time.time()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT name, node_type, path, importance_score
        FROM code_nodes
        WHERE name LIKE ? OR summary LIKE ?
        ORDER BY importance_score DESC
        LIMIT 10
        """, (f'%{search_term}%', f'%{search_term}%'))
        
        graph_results = cursor.fetchall()
        graph_time = time.time() - start_time
        
        print(f"📊 Graph search ({graph_time:.3f}s):")
        for name, node_type, path, score in graph_results:
            print(f"  • {name} ({node_type}) - importance: {score:.3f}")
            
        # Traditional search (simulate with grep)
        print(f"\n🔍 Traditional search would use:")
        print(f"  grep -r '{search_term}' . --include='*.py'")
        print("  Then manually parse results...")
        print("\n✅ Graph advantages:")
        print("  • Pre-computed importance scores")
        print("  • Structured results with context")
        print("  • Relationship information available")
        print("  • No need to parse source files again")

# Demo usage
if __name__ == "__main__":
    analyzer = GraphAnalyzer("indexer_project.db")
    
    # 1. Analyze overall structure
    analyzer.analyze_code_structure()
    
    # 2. Find related components
    analyzer.find_related_components("CodeGraphIndexer")
    
    # 3. Find related to CLI
    analyzer.find_related_components("cli")
    
    # 4. Trace paths
    analyzer.trace_call_path("cli", "indexer")
    
    # 5. Compare search methods
    analyzer.compare_with_traditional_search("index")
    
    print("\n=== BENEFITS OF GRAPH-BASED APPROACH ===")
    print("1. 🚀 Instant understanding of code structure")
    print("2. 🔗 See relationships and dependencies clearly")
    print("3. 📊 Importance ranking helps focus on key components")
    print("4. 🎯 Precise component search with context")
    print("5. ⚡ Fast queries on pre-indexed data")
    print("6. 🧩 Better for understanding before coding")