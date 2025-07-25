#!/usr/bin/env python3
"""
Performance benchmark comparing cci search vs grep
Tests search speed and accuracy on realistic codebases
"""

import time
import subprocess
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
import tempfile
import shutil

class PerformanceBenchmark:
    def __init__(self, test_dir: str):
        self.test_dir = Path(test_dir)
        self.results = {}
        
    def create_test_codebase(self) -> Path:
        """Create a realistic test codebase"""
        test_path = self.test_dir / "benchmark_codebase"
        test_path.mkdir(exist_ok=True, parents=True)
        
        # Create various file types with search targets
        files = {
            "src/main.js": """
function calculateTotal(items) {
    return items.reduce((total, item) => total + item.price, 0);
}

class ShoppingCart {
    constructor() {
        this.items = [];
        this.total = 0;
    }
    
    addItem(item) {
        this.items.push(item);
        this.total = calculateTotal(this.items);
    }
    
    removeItem(id) {
        this.items = this.items.filter(item => item.id !== id);
        this.total = calculateTotal(this.items);
    }
}

export { ShoppingCart, calculateTotal };
""",
            "src/utils.js": """
import { calculateTotal } from './main.js';

export function formatPrice(price) {
    return `$${price.toFixed(2)}`;
}

export function validateItem(item) {
    return item && item.price > 0 && item.name;
}

export function getTotalWithTax(items, taxRate = 0.08) {
    const subtotal = calculateTotal(items);
    return subtotal * (1 + taxRate);
}
""",
            "src/api.py": """
from typing import List, Dict
import json

def calculate_total(items: List[Dict]) -> float:
    '''Calculate total price from items'''
    return sum(item.get('price', 0) for item in items)

class CartAPI:
    def __init__(self):
        self.carts = {}
    
    def create_cart(self, user_id: str) -> str:
        cart_id = f"cart_{len(self.carts)}"
        self.carts[cart_id] = {
            'user_id': user_id,
            'items': [],
            'total': 0
        }
        return cart_id
    
    def add_item(self, cart_id: str, item: Dict):
        if cart_id in self.carts:
            self.carts[cart_id]['items'].append(item)
            self.carts[cart_id]['total'] = calculate_total(
                self.carts[cart_id]['items']
            )
""",
            "tests/test_main.js": """
import { ShoppingCart, calculateTotal } from '../src/main.js';

describe('ShoppingCart', () => {
    test('calculateTotal should sum item prices', () => {
        const items = [
            { id: 1, name: 'Apple', price: 1.50 },
            { id: 2, name: 'Banana', price: 0.75 }
        ];
        expect(calculateTotal(items)).toBe(2.25);
    });
    
    test('should add items to cart', () => {
        const cart = new ShoppingCart();
        cart.addItem({ id: 1, name: 'Apple', price: 1.50 });
        expect(cart.total).toBe(1.50);
    });
});
""",
            "config/database.js": """
const config = {
    development: {
        host: 'localhost',
        port: 5432,
        database: 'shop_dev',
        calculateConnectionString() {
            return `postgresql://${this.host}:${this.port}/${this.database}`;
        }
    },
    production: {
        host: process.env.DB_HOST,
        port: process.env.DB_PORT,
        database: process.env.DB_NAME,
        calculateConnectionString() {
            return `postgresql://${this.host}:${this.port}/${this.database}`;
        }
    }
};

module.exports = config;
""",
            "README.md": """
# Shopping Cart Project

This project implements a shopping cart with price calculation features.

## Key Functions

- `calculateTotal()` - Calculates total price of items
- `ShoppingCart` - Main cart class
- `formatPrice()` - Formats prices for display

## Usage

```javascript
import { ShoppingCart, calculateTotal } from './src/main.js';

const cart = new ShoppingCart();
cart.addItem({ id: 1, name: 'Item', price: 10.00 });
```
""",
            "package.json": """
{
  "name": "shopping-cart",
  "version": "1.0.0",
  "description": "Shopping cart with calculateTotal functionality",
  "main": "src/main.js",
  "scripts": {
    "test": "jest",
    "build": "webpack"
  },
  "dependencies": {
    "lodash": "^4.17.21"
  }
}
"""
        }
        
        # Create files
        for file_path, content in files.items():
            full_path = test_path / file_path
            full_path.parent.mkdir(exist_ok=True, parents=True)
            full_path.write_text(content)
        
        return test_path
    
    def run_cci_search(self, codebase_path: Path, term: str) -> Tuple[float, List[str]]:
        """Run cci search and measure performance"""
        # First ensure the codebase is indexed
        index_result = subprocess.run(['cci', 'index', str(codebase_path)], 
                                     capture_output=True, text=True, cwd=codebase_path)
        
        # Run search and measure time
        start_time = time.perf_counter()
        result = subprocess.run(['cci', 'search', term, '--project', str(codebase_path)], 
                               capture_output=True, text=True, cwd=codebase_path)
        end_time = time.perf_counter()
        
        # Debug: print search result for troubleshooting
        if not result.stdout.strip() or "Search results" not in result.stdout:
            print(f"   ⚠️  cci search debug for '{term}':")
            print(f"   Index stderr: {index_result.stderr.strip()[:200]}")
            print(f"   Search stdout: {result.stdout.strip()[:200]}")
            print(f"   Search stderr: {result.stderr.strip()[:200]}")
        
        # Parse results - count lines with actual results (not headers)
        results = []
        lines = result.stdout.split('\n')
        for line in lines:
            if '│' in line and not line.startswith('┃') and not line.startswith('┡'):
                # Extract the path from the table row
                parts = line.split('│')
                if len(parts) >= 4:
                    path = parts[3].strip()
                    if path and not path.startswith('─'):
                        results.append(path)
        
        return end_time - start_time, results
    
    def run_grep_search(self, codebase_path: Path, term: str) -> Tuple[float, List[str]]:
        """Run grep search and measure performance"""
        start_time = time.perf_counter()
        result = subprocess.run(['grep', '-r', '-n', term, '.'], 
                               capture_output=True, text=True, cwd=codebase_path)
        end_time = time.perf_counter()
        
        # Parse grep results
        results = []
        if result.stdout:
            for line in result.stdout.split('\n'):
                if line.strip() and ':' in line:
                    file_path = line.split(':')[0]
                    results.append(file_path)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for item in results:
            if item not in seen:
                seen.add(item)
                unique_results.append(item)
        
        return end_time - start_time, unique_results
    
    def run_ripgrep_search(self, codebase_path: Path, term: str) -> Tuple[float, List[str]]:
        """Run ripgrep search and measure performance (if available)"""
        try:
            start_time = time.perf_counter()
            result = subprocess.run(['rg', '-n', term], 
                                   capture_output=True, text=True, cwd=codebase_path)
            end_time = time.perf_counter()
            
            # Parse ripgrep results
            results = []
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip() and ':' in line:
                        file_path = line.split(':')[0]
                        results.append(file_path)
            
            # Remove duplicates
            seen = set()
            unique_results = []
            for item in results:
                if item not in seen:
                    seen.add(item)
                    unique_results.append(item)
            
            return end_time - start_time, unique_results
        except FileNotFoundError:
            return None, []
    
    def benchmark_search_terms(self, codebase_path: Path) -> Dict:
        """Benchmark various search terms"""
        # Note: cci search looks for node names, not content
        search_terms = [
            'calculateTotal',  # Function name - should be fast in cci
            'ShoppingCart',    # Class name - should be fast in cci  
            'formatPrice',     # Another function name
            'CartAPI',         # Python class name
            'main.js',         # File name
            'nonexistent'      # No matches
        ]
        
        results = {}
        
        for term in search_terms:
            print(f"🔍 Benchmarking search term: '{term}'")
            
            # Test cci search
            cci_time, cci_results = self.run_cci_search(codebase_path, term)
            
            # Test grep search  
            grep_time, grep_results = self.run_grep_search(codebase_path, term)
            
            # Test ripgrep if available
            rg_time, rg_results = self.run_ripgrep_search(codebase_path, term)
            
            results[term] = {
                'cci': {
                    'time': cci_time,
                    'results_count': len(cci_results),
                    'results': cci_results[:5]  # First 5 results for comparison
                },
                'grep': {
                    'time': grep_time, 
                    'results_count': len(grep_results),
                    'results': grep_results[:5]
                }
            }
            
            if rg_time is not None:
                results[term]['ripgrep'] = {
                    'time': rg_time,
                    'results_count': len(rg_results), 
                    'results': rg_results[:5]
                }
        
        return results
    
    def print_results(self, results: Dict):
        """Print benchmark results in a nice format"""
        print("\n" + "="*80)
        print("🚀 PERFORMANCE BENCHMARK RESULTS")
        print("="*80)
        
        for term, data in results.items():
            print(f"\n🔍 Search term: '{term}'")
            print("-" * 50)
            
            # Print timing comparison
            cci_time = data['cci']['time'] * 1000  # Convert to ms
            grep_time = data['grep']['time'] * 1000
            
            print(f"⏱️  Timing:")
            print(f"   cci search:  {cci_time:.2f}ms ({data['cci']['results_count']} results)")
            print(f"   grep:        {grep_time:.2f}ms ({data['grep']['results_count']} results)")
            
            if 'ripgrep' in data:
                rg_time = data['ripgrep']['time'] * 1000
                print(f"   ripgrep:     {rg_time:.2f}ms ({data['ripgrep']['results_count']} results)")
            
            # Speed comparison
            if grep_time > 0:
                speedup = grep_time / cci_time if cci_time > 0 else float('inf')
                if speedup > 1:
                    print(f"   🚀 cci is {speedup:.1f}x faster than grep")
                else:
                    print(f"   ⚠️  grep is {1/speedup:.1f}x faster than cci")
            
            # Result accuracy comparison
            if data['cci']['results_count'] != data['grep']['results_count']:
                print(f"   📊 Result count differs: cci={data['cci']['results_count']}, grep={data['grep']['results_count']}")
        
        # Overall summary
        print(f"\n" + "="*80)
        print("📊 SUMMARY")
        print("="*80)
        
        total_cci_time = sum(data['cci']['time'] for data in results.values()) * 1000
        total_grep_time = sum(data['grep']['time'] for data in results.values()) * 1000
        
        print(f"Total time across all searches:")
        print(f"   cci:   {total_cci_time:.2f}ms")
        print(f"   grep:  {total_grep_time:.2f}ms")
        
        if total_grep_time > 0:
            overall_speedup = total_grep_time / total_cci_time if total_cci_time > 0 else float('inf')
            if overall_speedup > 1:
                print(f"   🚀 Overall: cci is {overall_speedup:.1f}x faster")
            else:
                print(f"   ⚠️  Overall: grep is {1/overall_speedup:.1f}x faster")

def main():
    print("🚀 Starting Performance Benchmark: cci search vs grep")
    
    benchmark = PerformanceBenchmark("benchmark_temp")
    
    try:
        # Create test codebase
        print("📁 Creating test codebase...")
        codebase_path = benchmark.create_test_codebase()
        print(f"   Created at: {codebase_path}")
        
        # Run benchmarks
        print("⏱️  Running benchmarks...")
        results = benchmark.benchmark_search_terms(codebase_path)
        
        # Print results
        benchmark.print_results(results)
        
        # Save results to file
        results_file = Path("performance_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Detailed results saved to: {results_file}")
        
    finally:
        # Cleanup
        if benchmark.test_dir.exists():
            shutil.rmtree(benchmark.test_dir)
        print("🧹 Cleanup completed")

if __name__ == "__main__":
    main()