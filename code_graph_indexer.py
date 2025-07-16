#!/usr/bin/env python3
"""
Code Graph Indexer using Ensmallen
This demonstrates indexing source code as a graph database
"""

import ast
import os
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
import networkx as nx
import numpy as np
import pandas as pd


class CodeGraphIndexer:
    def __init__(self, db_path: str = "code_index.db"):
        self.db_path = db_path
        self.nodes = {}  # node_id -> node_info
        self.edges = []  # List of (source, target, edge_type)
        self.node_counter = 0
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_nodes (
            id INTEGER PRIMARY KEY,
            node_type TEXT,
            name TEXT,
            path TEXT,
            summary TEXT,
            importance_score REAL,
            relevance_tags TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            source_id INTEGER,
            target_id INTEGER,
            relationship_type TEXT,
            weight REAL,
            FOREIGN KEY (source_id) REFERENCES code_nodes(id),
            FOREIGN KEY (target_id) REFERENCES code_nodes(id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def parse_python_file(self, file_path: str) -> Dict:
        """Parse a Python file and extract code entities"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return {}
        
        # Create file node
        file_node_id = self._create_node(
            node_type='file',
            name=os.path.basename(file_path),
            path=file_path,
            summary=f"Python file: {os.path.basename(file_path)}"
        )
        
        # Extract imports, classes, and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_node_id = self._create_node(
                        node_type='import',
                        name=alias.name,
                        path=file_path,
                        summary=f"Import: {alias.name}"
                    )
                    self.edges.append((file_node_id, import_node_id, 'imports'))
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_node_id = self._create_node(
                        node_type='import',
                        name=node.module,
                        path=file_path,
                        summary=f"Import from: {node.module}"
                    )
                    self.edges.append((file_node_id, import_node_id, 'imports'))
            
            elif isinstance(node, ast.ClassDef):
                class_node_id = self._create_node(
                    node_type='class',
                    name=node.name,
                    path=file_path,
                    summary=f"Class: {node.name}"
                )
                self.edges.append((file_node_id, class_node_id, 'contains'))
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_node_id = self._create_node(
                            node_type='method',
                            name=f"{node.name}.{item.name}",
                            path=file_path,
                            summary=f"Method: {node.name}.{item.name}"
                        )
                        self.edges.append((class_node_id, method_node_id, 'contains'))
            
            elif isinstance(node, ast.FunctionDef) and not self._is_method(node):
                func_node_id = self._create_node(
                    node_type='function',
                    name=node.name,
                    path=file_path,
                    summary=f"Function: {node.name}"
                )
                self.edges.append((file_node_id, func_node_id, 'contains'))
        
        return self.nodes
    
    def _create_node(self, node_type: str, name: str, path: str, summary: str) -> int:
        """Create a node and return its ID"""
        node_id = self.node_counter
        self.nodes[node_id] = {
            'id': node_id,
            'node_type': node_type,
            'name': name,
            'path': path,
            'summary': summary,
            'importance_score': 0.0,
            'relevance_tags': []
        }
        self.node_counter += 1
        return node_id
    
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if a function is a method (inside a class)"""
        # This is a simplified check - in real implementation you'd need
        # to track the parent context while walking the AST
        return False  # For now, treat all functions as standalone
    
    def build_graph(self) -> nx.DiGraph:
        """Build NetworkX graph from nodes and edges"""
        # Create NetworkX graph
        nx_graph = nx.DiGraph()
        
        # Add nodes
        for node_id, node_info in self.nodes.items():
            nx_graph.add_node(
                node_id,
                node_type=node_info['node_type'],
                name=node_info['name']
            )
        
        # Add edges
        for source, target, edge_type in self.edges:
            nx_graph.add_edge(source, target, edge_type=edge_type)
        
        return nx_graph
    
    def calculate_importance_scores(self, graph: nx.DiGraph):
        """Calculate importance scores for nodes using graph metrics"""
        # Calculate various centrality measures
        in_degree_centrality = nx.in_degree_centrality(graph)
        out_degree_centrality = nx.out_degree_centrality(graph)
        
        # Calculate PageRank for importance
        try:
            pagerank = nx.pagerank(graph, alpha=0.85)
        except:
            pagerank = {node: 0.0 for node in graph.nodes()}
        
        # Update node importance scores
        for node_id in self.nodes:
            if node_id in graph:
                # Combine different metrics
                in_score = in_degree_centrality.get(node_id, 0.0)
                out_score = out_degree_centrality.get(node_id, 0.0)
                pr_score = pagerank.get(node_id, 0.0)
                
                # Weighted importance score
                importance_score = (
                    0.4 * in_score +  # How many depend on this
                    0.2 * out_score + # Complexity
                    0.4 * pr_score    # Overall importance
                )
                
                self.nodes[node_id]['importance_score'] = min(importance_score, 1.0)
                
                # Add relevance tags
                tags = []
                if self.nodes[node_id]['node_type'] == 'class':
                    tags.append('structural')
                if graph.in_degree(node_id) > 3:
                    tags.append('highly-used')
                if graph.out_degree(node_id) > 3:
                    tags.append('complex')
                if 'test' in self.nodes[node_id]['name'].lower():
                    tags.append('test')
                if self.nodes[node_id]['node_type'] == 'file':
                    tags.append('module')
                
                self.nodes[node_id]['relevance_tags'] = tags
            else:
                self.nodes[node_id]['importance_score'] = 0.0
                self.nodes[node_id]['relevance_tags'] = []
    
    def save_to_db(self):
        """Save nodes and relationships to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM relationships")
        cursor.execute("DELETE FROM code_nodes")
        
        # Insert nodes
        for node_id, node_info in self.nodes.items():
            cursor.execute('''
            INSERT INTO code_nodes (id, node_type, name, path, summary, importance_score, relevance_tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                node_info['id'],
                node_info['node_type'],
                node_info['name'],
                node_info['path'],
                node_info['summary'],
                node_info['importance_score'],
                json.dumps(node_info['relevance_tags'])
            ))
        
        # Insert edges
        for source, target, edge_type in self.edges:
            cursor.execute('''
            INSERT INTO relationships (source_id, target_id, relationship_type, weight)
            VALUES (?, ?, ?, ?)
            ''', (source, target, edge_type, 1.0))
        
        conn.commit()
        conn.close()
    
    def index_directory(self, directory: str):
        """Index all Python files in a directory"""
        for file_path in Path(directory).rglob("*.py"):
            print(f"Indexing: {file_path}")
            self.parse_python_file(str(file_path))
        
        # Build graph and calculate importance
        print("Building graph...")
        graph = self.build_graph()
        
        print("Calculating importance scores...")
        self.calculate_importance_scores(graph)
        
        print("Saving to database...")
        self.save_to_db()
        
        print(f"\nIndexed {len(self.nodes)} nodes and {len(self.edges)} relationships")
    
    def query_important_nodes(self, min_score: float = 0.5) -> List[Dict]:
        """Query nodes with high importance scores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM code_nodes 
        WHERE importance_score >= ? 
        ORDER BY importance_score DESC
        ''', (min_score,))
        
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            node_dict = dict(zip(columns, row))
            node_dict['relevance_tags'] = json.loads(node_dict['relevance_tags'])
            results.append(node_dict)
        
        conn.close()
        return results


def demonstrate_ensmallen_integration():
    """Demonstrate how to use ensmallen for graph embeddings"""
    print("\n=== Ensmallen Integration Demo ===")
    
    # Import ensmallen
    from ensmallen import Graph as EnsmallenGraph
    from ensmallen import models
    
    # Load our graph data
    indexer = CodeGraphIndexer()
    indexer.index_directory("sample_code")
    
    # Prepare edge list for ensmallen
    edge_list = []
    for source, target, edge_type in indexer.edges:
        # Ensmallen expects string node names
        edge_list.append([
            f"node_{source}",
            f"node_{target}"
        ])
    
    if edge_list:
        # Create ensmallen graph
        print("\nCreating ensmallen graph...")
        ensmallen_graph = EnsmallenGraph.from_pandas(
            pd.DataFrame(edge_list, columns=["source", "destination"]),
            directed=True,
            verbose=False
        )
        
        print(f"Ensmallen graph: {ensmallen_graph.get_number_of_nodes()} nodes, {ensmallen_graph.get_number_of_edges()} edges")
        
        # Generate node embeddings using Node2Vec
        print("\nGenerating node embeddings with Node2Vec...")
        node2vec = models.Node2Vec(
            walk_length=10,
            batch_size=32,
            window_size=4,
            return_weight=0.5,
            explore_weight=2.0,
            iterations=10
        )
        
        # Fit the model
        embeddings = node2vec.fit_transform(ensmallen_graph)
        print(f"Generated embeddings shape: {embeddings.shape}")
        
        # You can use these embeddings for:
        # - Code similarity search
        # - Clustering related code components
        # - Anomaly detection in code structure
        # - Code recommendation systems
    
    print("\n=== Demo Complete ===")


# Example usage
if __name__ == "__main__":
    # First run the basic indexing
    indexer = CodeGraphIndexer()
    
    # Create sample Python files for testing
    sample_dir = "sample_code"
    os.makedirs(sample_dir, exist_ok=True)
    
    # Sample file 1: main.py
    with open(os.path.join(sample_dir, "main.py"), "w") as f:
        f.write('''
import utils
from models import UserModel, ProductModel

class Application:
    def __init__(self):
        self.users = []
        self.products = []
    
    def add_user(self, user: UserModel):
        self.users.append(user)
    
    def add_product(self, product: ProductModel):
        self.products.append(product)

def main():
    app = Application()
    print("Application started")

if __name__ == "__main__":
    main()
''')
    
    # Sample file 2: models.py
    with open(os.path.join(sample_dir, "models.py"), "w") as f:
        f.write('''
class UserModel:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def get_info(self):
        return f"{self.name} ({self.email})"

class ProductModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def get_price_with_tax(self, tax_rate=0.1):
        return self.price * (1 + tax_rate)
''')
    
    # Sample file 3: utils.py
    with open(os.path.join(sample_dir, "utils.py"), "w") as f:
        f.write('''
import json
import datetime

def format_date(date):
    return date.strftime("%Y-%m-%d")

def parse_json(json_str):
    return json.loads(json_str)

def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)
''')
    
    # Index the sample directory
    indexer.index_directory(sample_dir)
    
    # Query important nodes
    print("\nImportant nodes (score >= 0.1):")
    important_nodes = indexer.query_important_nodes(min_score=0.1)
    for node in important_nodes:
        print(f"- {node['name']} ({node['node_type']}) - Score: {node['importance_score']:.3f} - Tags: {node['relevance_tags']}")
    
    # Demonstrate ensmallen integration
    try:
        demonstrate_ensmallen_integration()
    except Exception as e:
        print(f"\nEnsmallen demo skipped due to: {e}")