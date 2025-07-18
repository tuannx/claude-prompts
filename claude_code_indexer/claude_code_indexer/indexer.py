#!/usr/bin/env python3
"""
Code Graph Indexer using Ensmallen
"""

import ast
import os
import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import networkx as nx
import pandas as pd
from ensmallen import Graph
from .pattern_detector import PatternDetector
from .library_detector import LibraryDetector
from .infrastructure_detector import InfrastructureDetector
from .weight_calculator import WeightCalculator
from .db_optimizer import OptimizedDatabase, time_it
from .parallel_processor import ParallelFileProcessor, ProcessingStats
from .cache_manager import CacheManager, IncrementalIndexer
from .logger import log_info, log_warning, log_error
from .ignore_handler import IgnoreHandler
from .parsers import create_default_parser, ParseResult
from .storage_manager import get_storage_manager
from .security import validate_sql_identifier, SecurityError


class CodeGraphIndexer:
    """Main code indexing class using Ensmallen graph database"""
    
    def __init__(self, db_path: str = None, use_cache: bool = True, 
                 parallel_workers: int = None, enable_optimizations: bool = True,
                 project_path: Path = None):
        # Use centralized storage manager
        self.storage_manager = get_storage_manager()
        
        # Determine project path
        if project_path:
            self.project_path = Path(project_path)
        else:
            self.project_path = self.storage_manager.get_project_from_cwd()
        
        # Get database path from storage manager
        if db_path:
            # Allow override for backward compatibility
            self.db_path = db_path
        else:
            self.db_path = str(self.storage_manager.get_database_path(self.project_path))
        
        self.nodes = {}  # node_id -> node_info
        self.edges = []  # List of (source, target, edge_type)
        self.node_counter = 0
        self.pattern_detector = PatternDetector()
        self.library_detector = LibraryDetector()
        self.infrastructure_detector = InfrastructureDetector()
        self.weight_calculator = WeightCalculator()
        self.all_files_content = {}  # Store file contents for weight calculation
        
        # Multi-language parser system
        self.parser = create_default_parser()
        
        # Performance optimizations
        self.use_cache = use_cache
        self.enable_optimizations = enable_optimizations
        
        # Logging and debugging
        self.verbose = False
        self.parsing_errors = []
        
        if self.use_cache:
            self.cache_manager = CacheManager(project_path=self.project_path)
            self.incremental_indexer = IncrementalIndexer(self.cache_manager)
        
        if self.enable_optimizations:
            self.optimized_db = OptimizedDatabase(self.db_path)
        
        self.parallel_processor = ParallelFileProcessor(max_workers=parallel_workers)
        self.processing_stats = ProcessingStats()
        
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with schema and handle migrations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if database exists and needs migration
        self._migrate_database_schema(cursor)
        
        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_nodes (
            id INTEGER PRIMARY KEY,
            node_type TEXT,
            name TEXT,
            path TEXT,
            summary TEXT,
            importance_score REAL,
            relevance_tags TEXT,
            weight REAL,
            frequency_score REAL,
            usage_stats TEXT,
            language TEXT DEFAULT 'python',
            line_number INTEGER DEFAULT 0,
            column_number INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            source_id INTEGER,
            target_id INTEGER,
            relationship_type TEXT,
            weight REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES code_nodes(id),
            FOREIGN KEY (target_id) REFERENCES code_nodes(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS indexing_metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Patterns table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            pattern_type TEXT,
            confidence REAL,
            description TEXT,
            nodes TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Libraries table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS libraries (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            name TEXT,
            version TEXT,
            category TEXT,
            usage_count INTEGER,
            usage_contexts TEXT,
            import_statements TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Infrastructure table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS infrastructure (
            id INTEGER PRIMARY KEY,
            file_path TEXT,
            component_type TEXT,
            name TEXT,
            technology TEXT,
            configuration TEXT,
            usage_frequency INTEGER,
            connections TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _integrate_cached_result(self, cached_result):
        """Integrate cached processing result into current indexing session"""
        try:
            # Store file content for weight calculation
            with open(cached_result.file_path, 'r', encoding='utf-8') as f:
                self.all_files_content[cached_result.file_path] = f.read()
            
            # Integrate nodes
            for node_id, node_data in cached_result.nodes.items():
                new_id = self.node_counter
                self.nodes[new_id] = node_data.copy()
                self.nodes[new_id]['id'] = new_id
                self.node_counter += 1
            
            # Integrate edges (need to remap node IDs)
            node_id_mapping = {}
            start_id = self.node_counter - len(cached_result.nodes)
            for i, old_id in enumerate(cached_result.nodes.keys()):
                node_id_mapping[old_id] = start_id + i
            
            for edge in cached_result.edges:
                source, target, edge_type = edge
                if source in node_id_mapping and target in node_id_mapping:
                    self.edges.append((
                        node_id_mapping[source], 
                        node_id_mapping[target], 
                        edge_type
                    ))
        except Exception as e:
            log_warning(f"Failed to integrate cached result for {cached_result.file_path}: {e}")
    
    def _integrate_processing_result(self, result):
        """Integrate parallel processing result into current indexing session"""
        # Store file content
        try:
            with open(result.file_path, 'r', encoding='utf-8') as f:
                self.all_files_content[result.file_path] = f.read()
        except:
            pass
        
        # Integrate nodes
        node_id_mapping = {}
        for old_id, node_data in result.nodes.items():
            new_id = self.node_counter
            self.nodes[new_id] = node_data.copy()
            self.nodes[new_id]['id'] = new_id
            node_id_mapping[old_id] = new_id
            self.node_counter += 1
        
        # Integrate edges with remapped IDs
        for edge in result.edges:
            source, target, edge_type = edge
            if source in node_id_mapping and target in node_id_mapping:
                self.edges.append((
                    node_id_mapping[source], 
                    node_id_mapping[target], 
                    edge_type
                ))
    
    def parse_code_file(self, file_path: str) -> Dict:
        """Parse a code file using the appropriate language parser"""
        if self.verbose:
            log_info(f"Parsing {file_path}...")
            
        # Use the new multi-language parser
        parse_result = self.parser.parse_file(file_path)
        
        if not parse_result.success:
            error_msg = f"Failed to parse {file_path}: {parse_result.error_message}"
            log_warning(error_msg)
            self.parsing_errors.append(error_msg)
            return {}
            
        if self.verbose and parse_result.error_message:
            # Partial success with warnings
            self.parsing_errors.append(f"Warnings in {file_path}: {parse_result.error_message}")
        
        # Convert parser nodes to indexer format
        # Keep a mapping from parser node IDs to indexer node IDs
        parser_to_indexer_id = {}
        
        for parser_node_id, parser_node in parse_result.nodes.items():
            # Map parser node to indexer node format
            indexer_node = {
                'id': self.node_counter,
                'node_type': parser_node.node_type,
                'name': parser_node.name,
                'path': parser_node.path,
                'summary': parser_node.summary,
                'importance_score': 0.0,
                'relevance_tags': [],
                'language': parser_node.language,
                'line_number': parser_node.line_number,
                'column_number': parser_node.column_number
            }
            
            # Add language-specific attributes
            if parser_node.attributes:
                indexer_node.update(parser_node.attributes)
            
            # Store the mapping
            parser_to_indexer_id[parser_node_id] = self.node_counter
            
            self.nodes[self.node_counter] = indexer_node
            self.node_counter += 1
        
        # Convert parser relationships to indexer format using the mapping
        for relationship in parse_result.relationships:
            source_id = parser_to_indexer_id.get(relationship.source_id)
            target_id = parser_to_indexer_id.get(relationship.target_id)
            
            if source_id is not None and target_id is not None:
                self.edges.append((source_id, target_id, relationship.relationship_type))
        
        return self.nodes
    
    def parse_python_file(self, file_path: str) -> Dict:
        """Parse a Python file and extract code entities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252', 'utf-8-sig']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                log_warning(f"Could not decode {file_path}, skipping")
                return {}
        
        # Store content for weight calculation
        self.all_files_content[file_path] = content
        
        # Check for null bytes (binary files)
        if '\x00' in content:
            log_warning(f"Binary file detected {file_path}, skipping")
            return {}
        
        try:
            tree = ast.parse(content)
        except (SyntaxError, ValueError) as e:
            log_warning(f"Cannot parse {file_path}: {e}")
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
            
            elif isinstance(node, ast.FunctionDef):
                func_node_id = self._create_node(
                    node_type='function',
                    name=node.name,
                    path=file_path,
                    summary=f"Function: {node.name}"
                )
                self.edges.append((file_node_id, func_node_id, 'contains'))
        
        # Detect patterns
        patterns = self.pattern_detector.detect_patterns(tree, file_path)
        self._store_patterns(patterns, file_path)
        
        # Detect libraries
        libraries = self.library_detector.detect_libraries(tree, file_path, content)
        self._store_libraries(libraries, file_path)
        
        # Detect infrastructure
        infrastructure = self.infrastructure_detector.detect_infrastructure(tree, file_path, content)
        self._store_infrastructure(infrastructure, file_path)
        
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
    
    def build_graph(self) -> nx.DiGraph:
        """Build NetworkX graph from nodes and edges"""
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
    
    def build_ensmallen_graph(self) -> Optional[Graph]:
        """Build Ensmallen graph for advanced analysis"""
        if not self.edges:
            return None
        
        # Prepare edge data
        edges_data = []
        for source, target, edge_type in self.edges:
            edges_data.append([f"node_{source}", f"node_{target}"])
        
        # Save to temporary file
        edges_df = pd.DataFrame(edges_data, columns=["source", "destination"])
        
        # Always use home directory for temp files to avoid permission issues
        # This is especially important for MCP servers and read-only environments
        try:
            temp_dir = Path.home() / '.claude_code_indexer' / 'temp'
            temp_dir.mkdir(exist_ok=True, parents=True)
            temp_file = str(temp_dir / f"temp_edges_{os.getpid()}_{int(time.time() * 1000)}.tsv")
        except (OSError, PermissionError):
            # Final fallback: use system temp directory
            import tempfile
            temp_file = tempfile.mktemp(suffix='.tsv', prefix='temp_edges_')
            
        # Add debug logging to understand the actual file path being used
        log_info(f"Creating temp file: {temp_file}")
        edges_df.to_csv(temp_file, index=False, sep="\t", header=False)
        
        try:
            # Create ensmallen graph
            graph = Graph.from_csv(
                edge_path=temp_file,
                directed=True,
                verbose=False
            )
            return graph
        except Exception as e:
            log_warning(f"Could not create Ensmallen graph: {e}")
            return None
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
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
                # Normalize scores for better distribution
                node_type = self.nodes[node_id]['node_type']
                
                # Base score from centrality measures
                base_score = (
                    0.4 * in_score +  # How many depend on this
                    0.2 * out_score + # Complexity
                    0.4 * pr_score    # Overall importance
                )
                
                # Boost scores based on node type
                type_boost = {
                    'class': 0.3,
                    'function': 0.1,
                    'method': 0.05,
                    'file': 0.0,
                    'import': 0.0
                }.get(node_type, 0.0)
                
                # Boost for nodes with many connections
                connection_boost = 0.0
                if graph.in_degree(node_id) > 5:
                    connection_boost = 0.2
                elif graph.in_degree(node_id) > 2:
                    connection_boost = 0.1
                
                # Calculate final score with boosts
                importance_score = base_score + type_boost + connection_boost
                
                # Normalize to 0-1 range with better distribution
                self.nodes[node_id]['importance_score'] = min(importance_score * 2, 1.0)
                
                # Add relevance tags
                tags = []
                if self.nodes[node_id]['node_type'] == 'class':
                    tags.append('structural')
                if graph.in_degree(node_id) > 3:
                    tags.append('highly-used')
                if graph.out_degree(node_id) > 3:
                    tags.append('complex')
                node_name = self.nodes[node_id].get('name', '')
                if node_name and 'test' in node_name.lower():
                    tags.append('test')
                if self.nodes[node_id]['node_type'] == 'file':
                    tags.append('module')
                
                self.nodes[node_id]['relevance_tags'] = tags
            else:
                self.nodes[node_id]['importance_score'] = 0.0
                self.nodes[node_id]['relevance_tags'] = []
    
    def save_to_db(self):
        """Save nodes and relationships to SQLite database with error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
        except sqlite3.Error as e:
            log_error(f"Error connecting to database: {e}")
            return False
        
        try:
            # Clear existing data safely - use parameterized queries
            tables_to_clear = ["relationships", "code_nodes", "patterns", "libraries", "infrastructure"]
            for table in tables_to_clear:
                try:
                    # Use explicit table names to avoid SQL injection
                    if table == "relationships":
                        cursor.execute("DELETE FROM relationships")
                    elif table == "code_nodes":
                        cursor.execute("DELETE FROM code_nodes")
                    elif table == "patterns":
                        cursor.execute("DELETE FROM patterns")
                    elif table == "libraries":
                        cursor.execute("DELETE FROM libraries")
                    elif table == "infrastructure":
                        cursor.execute("DELETE FROM infrastructure")
                except sqlite3.Error as e:
                    log_warning(f"Could not clear table {table}: {e}")
            
            # Insert nodes with error handling
            for node_id, node_info in self.nodes.items():
                try:
                    cursor.execute('''
                    INSERT INTO code_nodes (id, node_type, name, path, summary, importance_score, relevance_tags, weight, frequency_score, usage_stats, language, line_number, column_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        node_info['id'],
                        node_info['node_type'],
                        node_info['name'],
                        node_info['path'],
                        node_info['summary'],
                        node_info['importance_score'],
                        json.dumps(node_info['relevance_tags']),
                        node_info.get('weight', 0.0),
                        node_info.get('frequency_score', 0.0),
                        json.dumps(node_info.get('usage_stats', {})),
                        node_info.get('language', 'python'),
                        node_info.get('line_number', 0),
                        node_info.get('column_number', 0)
                    ))
                except sqlite3.Error as e:
                    log_warning(f"Could not insert node {node_id}: {e}")
                    # Try fallback insertion without new columns
                    try:
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
                    except sqlite3.Error as fallback_error:
                        log_error(f"Could not insert node {node_id} even with fallback: {fallback_error}")
        
            # Insert edges with error handling
            for source, target, edge_type in self.edges:
                try:
                    cursor.execute('''
                    INSERT INTO relationships (source_id, target_id, relationship_type, weight)
                    VALUES (?, ?, ?, ?)
                    ''', (source, target, edge_type, 1.0))
                except sqlite3.Error as e:
                    log_warning(f"Could not insert edge {source}->{target}: {e}")
            
            # Update metadata with error handling
            metadata_updates = [
                ('last_indexed', 'datetime("now")'),
                ('total_nodes', str(len(self.nodes))),
                ('total_edges', str(len(self.edges))),
                ('schema_version', '1.1.0')
            ]
            
            for key, value in metadata_updates:
                try:
                    if key == 'last_indexed':
                        cursor.execute('''
                        INSERT OR REPLACE INTO indexing_metadata (key, value)
                        VALUES (?, datetime('now'))
                        ''', (key,))
                    else:
                        cursor.execute('''
                        INSERT OR REPLACE INTO indexing_metadata (key, value)
                        VALUES (?, ?)
                        ''', (key, value))
                except sqlite3.Error as e:
                    log_warning(f"Could not update metadata {key}: {e}")
            
            conn.commit()
            log_info("✅ Data saved successfully")
            return True
            
        except sqlite3.Error as e:
            log_error(f"Database error during save: {e}")
            return False
        except Exception as e:
            log_error(f"Unexpected error during save: {e}")
            return False
        finally:
            try:
                conn.close()
            except:
                pass
    
    @time_it
    def index_directory(self, directory: str, patterns: List[str] = None, 
                       force_reindex: bool = False, custom_ignore: List[str] = None):
        """Index all supported code files in a directory with performance optimizations
        
        Args:
            directory: Directory to index
            patterns: File patterns to include (default: auto-detect from supported languages)
            force_reindex: Force re-indexing all files
            custom_ignore: Additional ignore patterns beyond .gitignore
        """
        if patterns is None:
            # Auto-generate patterns from supported extensions
            extensions = self.parser.get_supported_extensions()
            patterns = [f"*{ext}" for ext in extensions]
        
        start_time = time.time()
        
        # Initialize ignore handler
        ignore_handler = IgnoreHandler(directory, custom_ignore)
        
        # Collect all supported code files
        all_files = []
        for pattern in patterns:
            for file_path in Path(directory).rglob(pattern):
                if file_path.is_file():
                    file_str = str(file_path)
                    # Only include files that can be parsed
                    if self.parser.can_parse(file_str):
                        all_files.append(file_str)
        
        # Filter out ignored files
        all_files = ignore_handler.filter_files(all_files)
        
        if not all_files:
            log_info(f"No supported code files found matching patterns {patterns} in {directory} (after applying ignore rules)")
            return
        
        # Get language statistics
        language_stats = {}
        for file_path in all_files:
            parse_result = self.parser.parse_file(file_path)
            if parse_result.success:
                lang = parse_result.language
                if lang not in language_stats:
                    language_stats[lang] = 0
                language_stats[lang] += 1
        
        log_info(f"🔍 Found {len(all_files)} code files")
        for lang, count in language_stats.items():
            log_info(f"   📝 {lang}: {count} files")
        
        # Use incremental indexing if cache is enabled
        files_to_process = all_files
        cached_results = []
        
        if self.use_cache and not force_reindex:
            log_info("📋 Checking cache for unchanged files...")
            cached_files, files_to_process = self.incremental_indexer.get_files_to_process(all_files)
            
            if cached_files:
                log_info(f"💾 Loading {len(cached_files)} files from cache")
                cached_results = self.incremental_indexer.load_cached_results(cached_files)
                
                # Integrate cached results
                for cached_result in cached_results:
                    self._integrate_cached_result(cached_result)
            
            log_info(f"🔄 Processing {len(files_to_process)} new/modified files")
        
        # Process files with parallel processing or sequentially
        if files_to_process:
            if len(files_to_process) > 3 and hasattr(self, 'parallel_processor'):
                # Use parallel processing for multiple files
                processing_results = self.parallel_processor.process_files_parallel(files_to_process)
                self.processing_stats.update(processing_results)
                
                # Integrate parallel results and cache them
                for result in processing_results:
                    if result.success:
                        self._integrate_processing_result(result)
                        
                        # Cache the result if caching is enabled
                        if self.use_cache:
                            self.cache_manager.cache_file_result(
                                result.file_path, result.nodes, result.edges,
                                result.patterns, result.libraries, result.infrastructure
                            )
            else:
                # Sequential processing for small number of files
                for file_path in files_to_process:
                    parsed_nodes = self.parse_code_file(file_path)
                    # The parse_code_file method already adds nodes to self.nodes
                    # but we should also cache the result
                    if self.use_cache and parsed_nodes:
                        # Extract relevant data for caching
                        file_nodes = {id: node for id, node in self.nodes.items() 
                                     if node.get('path') == file_path}
                        file_edges = [(s, t, type) for s, t, type in self.edges 
                                     if s in file_nodes or t in file_nodes]
                        
                        # Cache the parsed result
                        self.cache_manager.cache_file_result(
                            file_path, file_nodes, file_edges,
                            {}, {}, {}  # patterns, libraries, infrastructure
                        )
        
        total_indexed = len(all_files)
        
        if total_indexed == 0:
            log_info("No files to index")
            return
        
        log_info("🔗 Building graph...")
        graph = self.build_graph()
        
        log_info("⚖️  Calculating importance scores...")
        self.calculate_importance_scores(graph)
        
        log_info("📊 Calculating weights based on usage frequency...")
        weighted_nodes, weighted_edges = self.weight_calculator.calculate_weights(
            self.nodes, self.edges, self.all_files_content
        )
        
        # Update nodes with weight information
        for node_id, weighted_node in weighted_nodes.items():
            self.nodes[node_id].update(weighted_node)
        
        log_info("💾 Saving to database...")
        if not self.save_to_db():
            log_error("❌ Failed to save data to database")
            return False
        
        # Print performance stats
        processing_time = time.time() - start_time
        
        log_info(f"\n✅ Indexing Complete!")
        log_info(f"   📁 Total files: {total_indexed}")
        log_info(f"   💾 From cache: {len(cached_results)}")
        log_info(f"   🔄 Processed: {len(files_to_process)}")
        log_info(f"   🔗 Nodes: {len(self.nodes)}")
        log_info(f"   ↔️  Edges: {len(self.edges)}")
        log_info(f"   ⏱️  Time: {processing_time:.2f}s")
        log_info(f"   🚀 Speed: {total_indexed/processing_time:.1f} files/sec")
        log_info(f"   💾 Database: {self.db_path}")
        
        # Update project stats in storage manager
        stats = {
            'nodes': len(self.nodes),
            'edges': len(self.edges),
            'files': total_indexed,
            'cached': len(cached_results),
            'processed': len(files_to_process),
            'time': processing_time
        }
        self.storage_manager.update_project_stats(self.project_path, stats)
        
        # Print processing stats if available
        if hasattr(self.processing_stats, 'print_stats') and files_to_process:
            self.processing_stats.print_stats()
        
        # Print cache stats if enabled
        if self.use_cache:
            self.cache_manager.print_cache_stats()
        
        # Try to build Ensmallen graph for advanced features
        ensmallen_graph = self.build_ensmallen_graph()
        if ensmallen_graph:
            log_info(f"✓ Ensmallen graph ready for advanced analysis")
    
    def query_important_nodes(self, min_score: float = 0.1, limit: int = 20, node_type: Optional[str] = None) -> List[Dict]:
        """Query nodes with high importance scores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM code_nodes WHERE importance_score >= ?"
        params = [min_score]
        
        if node_type:
            query += " AND node_type = ?"
            params.append(node_type)
            
        query += " ORDER BY importance_score DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            node_dict = dict(zip(columns, row))
            node_dict['relevance_tags'] = json.loads(node_dict['relevance_tags'])
            results.append(node_dict)
        
        conn.close()
        return results
    
    def get_stats(self) -> Dict:
        """Get indexing statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Get metadata
        cursor.execute('SELECT key, value FROM indexing_metadata')
        for key, value in cursor.fetchall():
            stats[key] = value
        
        # Get node type counts
        cursor.execute('SELECT node_type, COUNT(*) FROM code_nodes GROUP BY node_type')
        stats['node_types'] = dict(cursor.fetchall())
        
        # Get relationship type counts
        cursor.execute('SELECT relationship_type, COUNT(*) FROM relationships GROUP BY relationship_type')
        stats['relationship_types'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def _store_patterns(self, patterns: List, file_path: str):
        """Store detected patterns in database"""
        if not patterns:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for pattern in patterns:
            cursor.execute('''
            INSERT INTO patterns (file_path, pattern_type, confidence, description, nodes, location)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                file_path,
                pattern.pattern_type,
                pattern.confidence,
                pattern.description,
                json.dumps(pattern.nodes),
                pattern.location
            ))
        
        conn.commit()
        conn.close()
    
    def _store_libraries(self, libraries: Dict, file_path: str):
        """Store detected libraries in database"""
        if not libraries:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for lib_name, lib_usage in libraries.items():
            cursor.execute('''
            INSERT INTO libraries (file_path, name, version, category, usage_count, usage_contexts, import_statements)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_path,
                lib_usage.name,
                lib_usage.version,
                lib_usage.category,
                lib_usage.usage_count,
                json.dumps(lib_usage.usage_contexts),
                json.dumps(lib_usage.import_statements)
            ))
        
        conn.commit()
        conn.close()
    
    def _store_infrastructure(self, infrastructure: Dict, file_path: str):
        """Store detected infrastructure in database"""
        if not infrastructure:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for category, components in infrastructure.items():
            for component in components:
                cursor.execute('''
                INSERT INTO infrastructure (file_path, component_type, name, technology, configuration, usage_frequency, connections)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    file_path,
                    component.component_type,
                    component.name,
                    component.technology,
                    json.dumps(component.configuration),
                    component.usage_frequency,
                    json.dumps(component.connections)
                ))
        
        conn.commit()
        conn.close()
    
    def _migrate_database_schema(self, cursor):
        """Migrate existing database schema to support new columns"""
        try:
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='code_nodes'")
            if not cursor.fetchone():
                return  # New database, no migration needed
            
            # Check existing columns
            cursor.execute("PRAGMA table_info(code_nodes)")
            existing_columns = [column[1] for column in cursor.fetchall()]
            
            # Add missing columns for v1.1.0 and v1.6.0
            new_columns = {
                'weight': 'REAL DEFAULT 0.0',
                'frequency_score': 'REAL DEFAULT 0.0', 
                'usage_stats': 'TEXT DEFAULT "{}"',
                'language': 'TEXT DEFAULT "python"',
                'line_number': 'INTEGER DEFAULT 0',
                'column_number': 'INTEGER DEFAULT 0'
            }
            
            for column_name, column_def in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        # Validate column name to prevent SQL injection
                        safe_column_name = validate_sql_identifier(column_name)
                        # Use DDL with safe column name
                        cursor.execute(f"ALTER TABLE code_nodes ADD COLUMN {safe_column_name} {column_def}")
                        log_info(f"✓ Added column '{safe_column_name}' to code_nodes table")
                    except SecurityError as e:
                        log_warning(f"Invalid column name '{column_name}': {e}")
                    except sqlite3.Error as e:
                        log_warning(f"Could not add column '{column_name}': {e}")
            
            # Migrate other tables if needed
            self._migrate_new_tables(cursor)
            
        except sqlite3.Error as e:
            log_warning(f"Database migration failed: {e}")
    
    def _migrate_new_tables(self, cursor):
        """Create new tables introduced in v1.1.0"""
        new_tables = {
            'patterns': '''
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    pattern_type TEXT,
                    confidence REAL,
                    description TEXT,
                    nodes TEXT,
                    location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'libraries': '''
                CREATE TABLE IF NOT EXISTS libraries (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    name TEXT,
                    version TEXT,
                    category TEXT,
                    usage_count INTEGER,
                    usage_contexts TEXT,
                    import_statements TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'infrastructure': '''
                CREATE TABLE IF NOT EXISTS infrastructure (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT,
                    component_type TEXT,
                    name TEXT,
                    technology TEXT,
                    configuration TEXT,
                    usage_frequency INTEGER,
                    connections TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        for table_name, create_sql in new_tables.items():
            try:
                # Validate table name to prevent SQL injection
                safe_table_name = validate_sql_identifier(table_name)
                # Use parameterized query for table existence check
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (safe_table_name,))
                if not cursor.fetchone():
                    cursor.execute(create_sql)
                    log_info(f"✓ Created new table '{safe_table_name}'")
            except SecurityError as e:
                log_warning(f"Invalid table name '{table_name}': {e}")
            except sqlite3.Error as e:
                log_warning(f"Could not create table '{table_name}': {e}")
    
    def _safe_database_operation(self, operation_func, *args, **kwargs):
        """Execute database operation with error handling"""
        try:
            return operation_func(*args, **kwargs)
        except sqlite3.Error as e:
            log_error(f"Database error: {e}")
            return None
        except Exception as e:
            log_error(f"Unexpected error: {e}")
            return None