#!/usr/bin/env python3
"""
Complete working demo of Ensmallen for code graph indexing
"""

from ensmallen import Graph
import pandas as pd
import numpy as np

print("=== Complete Ensmallen Code Graph Demo ===\n")

# Realistic code relationship data
edges_data = [
    ["main.py", "utils.py"],
    ["main.py", "models.py"], 
    ["main.py", "Application"],
    ["Application", "UserModel"],
    ["Application", "ProductModel"],
    ["models.py", "UserModel"],
    ["models.py", "ProductModel"],
    ["utils.py", "format_date"],
    ["utils.py", "parse_json"],
    ["utils.py", "calculate_discount"],
    ["UserModel", "get_info"],
    ["UserModel", "__init__"],
    ["ProductModel", "get_price_with_tax"],
    ["ProductModel", "__init__"],
    ["Application", "add_user"],
    ["Application", "add_product"],
    ["add_user", "UserModel"],
    ["add_product", "ProductModel"],
]

# Create graph
edges_df = pd.DataFrame(edges_data, columns=["source", "destination"])
edges_df.to_csv("code_graph.tsv", index=False, sep="\t", header=False)

print(f"Code graph edges: {len(edges_data)}")
print("Sample edges:")
for i, (src, dst) in enumerate(edges_data[:5]):
    print(f"  {src} -> {dst}")

try:
    # Create ensmallen graph
    graph = Graph.from_csv(
        edge_path="code_graph.tsv",
        directed=True,
        verbose=False
    )
    
    print(f"\n✓ Graph created successfully!")
    print(f"  Nodes: {graph.get_number_of_nodes()}")
    print(f"  Edges: {graph.get_number_of_edges()}")
    print(f"  Directed: {graph.is_directed()}")
    
    # Node analysis
    node_names = graph.get_node_names()
    print(f"\nCode entities found: {len(node_names)}")
    print("Entities:", ", ".join(node_names[:8]) + "...")
    
    # Calculate node importance using degree centrality
    print("\n=== Node Importance Analysis ===")
    node_scores = []
    
    for node_name in node_names:
        node_id = graph.get_node_id_from_node_name(node_name)
        degree = graph.get_node_degree_from_node_id(node_id)
        node_scores.append((node_name, degree))
    
    # Sort by importance (degree)
    node_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("Most important code entities (by connections):")
    for name, score in node_scores[:8]:
        print(f"  {name}: {score} connections")
    
    # Generate embeddings for similarity analysis
    print("\n=== Code Similarity Analysis ===")
    try:
        from ensmallen import models
        
        # Node2Vec model for code embeddings
        node2vec = models.Node2Vec(
            walk_length=8,
            batch_size=32,
            window_size=4,
            return_weight=1.0,
            explore_weight=2.0,
            iterations=5,
            embedding_size=32
        )
        
        # Generate embeddings
        embeddings = node2vec.fit_transform(graph)
        print(f"✓ Generated embeddings: {embeddings.shape}")
        
        # Similarity analysis
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Compare key code components
        comparisons = [
            ("main.py", "models.py"),
            ("main.py", "utils.py"),
            ("UserModel", "ProductModel"),
            ("Application", "main.py"),
            ("utils.py", "models.py")
        ]
        
        print("\nCode similarity scores (cosine similarity):")
        for entity1, entity2 in comparisons:
            try:
                id1 = graph.get_node_id_from_node_name(entity1)
                id2 = graph.get_node_id_from_node_name(entity2)
                
                emb1 = embeddings[id1].reshape(1, -1)
                emb2 = embeddings[id2].reshape(1, -1)
                
                similarity = cosine_similarity(emb1, emb2)[0][0]
                print(f"  {entity1} <-> {entity2}: {similarity:.3f}")
                
            except Exception as e:
                print(f"  {entity1} <-> {entity2}: N/A (not found)")
    
    except Exception as e:
        print(f"Embeddings not available: {e}")
    
    # Graph analysis for code understanding
    print("\n=== Code Structure Analysis ===")
    
    # Find central nodes (hub detection)
    degree_centrality = graph.get_degree_centrality()
    central_nodes = [(node_names[i], degree_centrality[i]) for i in range(len(node_names))]
    central_nodes.sort(key=lambda x: x[1], reverse=True)
    
    print("Most central code entities (hubs):")
    for name, centrality in central_nodes[:5]:
        print(f"  {name}: {centrality:.3f}")
    
    # Neighbor analysis for dependency tracking
    print("\nDependency analysis (neighbors):")
    key_entities = ["main.py", "Application", "UserModel"]
    
    for entity in key_entities:
        if entity in node_names:
            entity_id = graph.get_node_id_from_node_name(entity)
            
            # Get all neighbors (both incoming and outgoing)
            try:
                # This might need to be adjusted based on available methods
                neighbors = []
                for other_name in node_names:
                    other_id = graph.get_node_id_from_node_name(other_name)
                    if graph.has_edge_from_node_ids(entity_id, other_id):
                        neighbors.append(f"{other_name} (depends on)")
                    elif graph.has_edge_from_node_ids(other_id, entity_id):
                        neighbors.append(f"{other_name} (uses)")
                
                print(f"  {entity}: {len(neighbors)} relationships")
                if neighbors:
                    print(f"    {', '.join(neighbors[:3])}{'...' if len(neighbors) > 3 else ''}")
                        
            except Exception as e:
                print(f"  {entity}: analysis failed")
    
    # Practical applications
    print("\n=== Practical Use Cases ===")
    print("1. 🔍 Find modules that depend on a specific class")
    print("2. 🔧 Identify refactoring candidates (highly connected nodes)")
    print("3. 📊 Measure code complexity through graph metrics")
    print("4. 🎯 Detect similar code patterns via embeddings")
    print("5. 🚨 Find orphaned or weakly connected components")
    print("6. 📈 Track architecture evolution over time")
    
    # SQLite integration example
    print("\n=== SQLite Integration ===")
    import sqlite3
    
    # Create database with graph metrics
    conn = sqlite3.connect("code_metrics.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_entities (
        name TEXT PRIMARY KEY,
        node_type TEXT,
        degree INTEGER,
        centrality REAL,
        embedding TEXT
    )
    ''')
    
    # Insert data
    for i, name in enumerate(node_names):
        node_id = graph.get_node_id_from_node_name(name)
        degree = graph.get_node_degree_from_node_id(node_id)
        centrality = degree_centrality[i]
        
        # Determine node type based on name patterns
        if name.endswith('.py'):
            node_type = 'file'
        elif name[0].isupper() and not '.' in name:
            node_type = 'class'
        elif '__' in name:
            node_type = 'method'
        else:
            node_type = 'function'
        
        # Store embedding as JSON if available
        embedding_json = None
        if 'embeddings' in locals():
            embedding_json = str(embeddings[node_id].tolist())
        
        cursor.execute('''
        INSERT OR REPLACE INTO code_entities 
        (name, node_type, degree, centrality, embedding)
        VALUES (?, ?, ?, ?, ?)
        ''', (str(name), str(node_type), int(degree), float(centrality), str(embedding_json) if embedding_json else None))
    
    conn.commit()
    
    # Query example
    cursor.execute('''
    SELECT name, node_type, degree, centrality 
    FROM code_entities 
    ORDER BY centrality DESC 
    LIMIT 5
    ''')
    
    print("Top entities stored in SQLite:")
    for row in cursor.fetchall():
        name, node_type, degree, centrality = row
        print(f"  {name} ({node_type}): degree={degree}, centrality={centrality:.3f}")
    
    conn.close()
    print("✓ Data saved to code_metrics.db")

except Exception as e:
    print(f"❌ Demo failed: {e}")
    import traceback
    traceback.print_exc()

# Clean up
import os
if os.path.exists("code_graph.tsv"):
    os.remove("code_graph.tsv")

print("\n=== Demo Complete ===")
print("This demonstrates how to:")
print("• Parse code into graph structure")
print("• Use ensmallen for graph analysis")
print("• Generate code embeddings")
print("• Store results in SQLite database")
print("• Apply graph metrics to understand code architecture")