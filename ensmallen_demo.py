#!/usr/bin/env python3
"""
Simplified demo of using Ensmallen for code graph analysis
"""

from ensmallen import Graph
import pandas as pd
import numpy as np

# Create a simple code graph example
print("=== Ensmallen Code Graph Demo ===\n")

# Define edges representing code relationships
edges_data = [
    # (source, destination, edge_type)
    ("main.py", "utils.py", "imports"),
    ("main.py", "models.py", "imports"),
    ("main.py", "Application", "contains"),
    ("Application", "Application.__init__", "contains"),
    ("Application", "Application.add_user", "contains"),
    ("Application", "Application.add_product", "contains"),
    ("Application.add_user", "UserModel", "uses"),
    ("Application.add_product", "ProductModel", "uses"),
    ("models.py", "UserModel", "contains"),
    ("models.py", "ProductModel", "contains"),
    ("UserModel", "UserModel.__init__", "contains"),
    ("UserModel", "UserModel.get_info", "contains"),
    ("ProductModel", "ProductModel.__init__", "contains"),
    ("ProductModel", "ProductModel.get_price_with_tax", "contains"),
    ("utils.py", "json", "imports"),
    ("utils.py", "datetime", "imports"),
    ("utils.py", "format_date", "contains"),
    ("utils.py", "parse_json", "contains"),
    ("utils.py", "calculate_discount", "contains"),
]

# Convert to DataFrame
edges_df = pd.DataFrame(edges_data, columns=["source", "destination", "edge_type"])
print("Edge list (first 5 rows):")
print(edges_df.head())
print(f"\nTotal edges: {len(edges_df)}")

# Create Ensmallen graph - using the correct API
print("\nCreating Ensmallen graph...")

# Method 1: From edge list
# Let's use a simpler approach
edges_list = edges_df[["source", "destination"]].values.tolist()

# Try different approaches to create the graph
try:
    # Approach 1: Direct from edge list
    graph = Graph.from_edge_list(
        edge_list=edges_list,
        directed=True,
        verbose=False
    )
except Exception as e1:
    print(f"Method 1 failed: {e1}")
    try:
        # Approach 2: Save to file and load
        edges_df[["source", "destination"]].to_csv("temp_edges.tsv", index=False, sep="\t", header=False)
        graph = Graph.from_csv(
            edge_path="temp_edges.tsv",
            directed=True,
            verbose=False
        )
    except Exception as e2:
        print(f"Method 2 failed: {e2}")
        # Fallback: create minimal graph
        graph = Graph.from_edge_list(
            edge_list=[("A", "B"), ("B", "C"), ("C", "A")],
            directed=True,
            verbose=False
        )

print(f"Graph created: {graph.get_number_of_nodes()} nodes, {graph.get_number_of_edges()} edges")

# Get node information
print("\nNode statistics:")
node_names = graph.get_node_names()
print(f"Total unique nodes: {len(node_names)}")
print("Sample nodes:", node_names[:5])

# Calculate node degrees
print("\nNode degree analysis:")
for i, node_name in enumerate(node_names[:10]):
    node_id = graph.get_node_id_from_node_name(node_name)
    in_degree = graph.get_node_degree_from_node_id(node_id, mode="in")
    out_degree = graph.get_node_degree_from_node_id(node_id, mode="out")
    print(f"- {node_name}: in={in_degree}, out={out_degree}, total={in_degree + out_degree}")

# Get connected components
print("\nConnected components:")
components = graph.get_connected_components()
print(f"Number of components: {components.max() + 1}")

# Node2Vec embeddings (if available)
try:
    from ensmallen import models
    
    print("\nGenerating Node2Vec embeddings...")
    node2vec = models.Node2Vec(
        walk_length=10,
        batch_size=32,
        window_size=4,
        return_weight=0.5,
        explore_weight=2.0,
        iterations=5,
        embedding_size=32
    )
    
    # Generate embeddings
    embeddings = node2vec.fit_transform(graph)
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Calculate similarity between some nodes
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Get embeddings for specific nodes
    main_idx = graph.get_node_id_from_node_name("main.py")
    utils_idx = graph.get_node_id_from_node_name("utils.py")
    models_idx = graph.get_node_id_from_node_name("models.py")
    
    # Calculate similarities
    main_emb = embeddings[main_idx].reshape(1, -1)
    utils_emb = embeddings[utils_idx].reshape(1, -1)
    models_emb = embeddings[models_idx].reshape(1, -1)
    
    print("\nCode file similarities (cosine):")
    print(f"main.py <-> utils.py: {cosine_similarity(main_emb, utils_emb)[0][0]:.3f}")
    print(f"main.py <-> models.py: {cosine_similarity(main_emb, models_emb)[0][0]:.3f}")
    print(f"utils.py <-> models.py: {cosine_similarity(utils_emb, models_emb)[0][0]:.3f}")
    
except Exception as e:
    print(f"\nNode2Vec skipped: {e}")

# Clean up
import os
if os.path.exists("temp_edges.csv"):
    os.remove("temp_edges.csv")
if os.path.exists("temp_edges.tsv"):
    os.remove("temp_edges.tsv")

print("\n=== Demo Complete ===")