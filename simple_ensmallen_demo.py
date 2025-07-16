#!/usr/bin/env python3
"""
Working demo of Ensmallen for code indexing
"""

from ensmallen import Graph
import pandas as pd
import numpy as np

print("=== Working Ensmallen Demo ===\n")

# Simple edge list for demonstration
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
    ["UserModel", "get_info"],
    ["ProductModel", "get_price"]
]

# Save to file (ensmallen prefers file input)
edges_df = pd.DataFrame(edges_data, columns=["source", "destination"])
edges_df.to_csv("code_edges.tsv", index=False, sep="\t", header=False)

print("Created edge file with code relationships")
print(f"Total edges: {len(edges_data)}")

# Create graph from file
try:
    graph = Graph.from_csv(
        edge_path="code_edges.tsv",
        directed=True,
        verbose=False
    )
    
    print(f"\nGraph successfully created!")
    print(f"Nodes: {graph.get_number_of_nodes()}")
    print(f"Edges: {graph.get_number_of_edges()}")
    
    # Get basic graph info
    node_names = graph.get_node_names()
    print(f"\nNode names (first 10): {node_names[:10]}")
    
    # Check connectivity
    print(f"Is connected: {graph.is_connected()}")
    print(f"Is directed: {graph.is_directed()}")
    
    # Node degree analysis (using correct API)
    print("\nNode degree analysis:")
    for i, node_name in enumerate(node_names[:8]):
        node_id = graph.get_node_id_from_node_name(node_name)
        
        # Get in-degree and out-degree separately
        in_degree = graph.get_node_in_degree_from_node_id(node_id)
        out_degree = graph.get_node_out_degree_from_node_id(node_id)
        total_degree = in_degree + out_degree
        
        print(f"- {node_name}: in={in_degree}, out={out_degree}, total={total_degree}")
    
    # Try to generate embeddings
    print("\nAttempting to generate embeddings...")
    try:
        from ensmallen import models
        
        # Use Node2Vec for embeddings
        model = models.Node2Vec(
            walk_length=5,
            batch_size=16,
            window_size=3,
            return_weight=1.0,
            explore_weight=1.0,
            iterations=3,
            embedding_size=16
        )
        
        # Fit and get embeddings
        embeddings = model.fit_transform(graph)
        print(f"Generated embeddings: {embeddings.shape}")
        
        # Calculate some similarities
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Get embeddings for key nodes
        try:
            main_idx = graph.get_node_id_from_node_name("main.py")
            utils_idx = graph.get_node_id_from_node_name("utils.py")
            models_idx = graph.get_node_id_from_node_name("models.py")
            
            main_emb = embeddings[main_idx].reshape(1, -1)
            utils_emb = embeddings[utils_idx].reshape(1, -1)
            models_emb = embeddings[models_idx].reshape(1, -1)
            
            print("\nCode similarity analysis:")
            print(f"main.py <-> utils.py: {cosine_similarity(main_emb, utils_emb)[0][0]:.3f}")
            print(f"main.py <-> models.py: {cosine_similarity(main_emb, models_emb)[0][0]:.3f}")
            print(f"utils.py <-> models.py: {cosine_similarity(utils_emb, models_emb)[0][0]:.3f}")
            
        except Exception as e:
            print(f"Similarity calculation failed: {e}")
            
    except Exception as e:
        print(f"Embeddings failed: {e}")
    
    # Graph traversal example
    print("\nGraph traversal example:")
    main_id = graph.get_node_id_from_node_name("main.py")
    print(f"Starting from main.py (id: {main_id})")
    
    # Get neighbors
    try:
        neighbors = graph.get_neighbour_node_ids_from_node_id(main_id)
        print(f"Direct neighbors of main.py: {[graph.get_node_name_from_node_id(n) for n in neighbors]}")
    except Exception as e:
        print(f"Neighbor analysis failed: {e}")

except Exception as e:
    print(f"Graph creation failed: {e}")

# Practical applications summary
print("\n=== Practical Applications ===")
print("1. Code Navigation: Find related modules and dependencies")
print("2. Refactoring: Identify tightly coupled components")
print("3. Impact Analysis: Trace changes through the codebase")
print("4. Architecture Understanding: Visualize code structure")
print("5. Similarity Search: Find similar code patterns")
print("6. Anomaly Detection: Identify unusual code structures")

# Clean up
import os
if os.path.exists("code_edges.tsv"):
    os.remove("code_edges.tsv")

print("\n=== Demo Complete ===")