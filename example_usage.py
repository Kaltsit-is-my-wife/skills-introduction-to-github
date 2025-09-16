#!/usr/bin/env python3
"""
Example usage of the CSV Scanner utility

This script demonstrates how to use the CSVScanner class programmatically.
"""

from csv_scanner import CSVScanner, format_search_results
import os


def example_usage():
    """Demonstrate various uses of the CSV scanner."""
    
    # Define the test data directory
    test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    
    print("=== CSV Scanner Example Usage ===\n")
    
    # Initialize the scanner
    print(f"1. Initializing scanner for directory: {test_dir}")
    scanner = CSVScanner(test_dir)
    
    # Show discovered files
    csv_files = scanner.get_csv_files()
    print(f"   Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"   - {file}")
    print()
    
    # Show statistics
    stats = scanner.get_stats()
    print("2. Scanner Statistics:")
    print(f"   Total CSV files: {stats['total_csv_files']}")
    print(f"   Directories scanned: {stats['total_directories_scanned']}")
    print()
    
    # Example searches
    searches = [
        ("Engineering", False, "Search for 'Engineering' (case insensitive)"),
        ("email", False, "Search for 'email' (case insensitive)"),
        ("Electronics", True, "Search for 'Electronics' (case sensitive)"),
        ("@example.com", False, "Search for email domain '@example.com'"),
    ]
    
    for keyword, case_sensitive, description in searches:
        print(f"3. {description}")
        results = scanner.search_keyword(keyword, case_sensitive)
        
        if results:
            print(f"   Found {len(results)} matches:")
            # Show just the first few results for brevity
            for i, result in enumerate(results[:3]):
                file_name = os.path.basename(result['file_path'])
                print(f"   - {file_name}, row {result['row_number']}")
            if len(results) > 3:
                print(f"   ... and {len(results) - 3} more matches")
        else:
            print("   No matches found")
        print()
    
    # Detailed search example
    print("4. Detailed search results for 'Engineering':")
    results = scanner.search_keyword("Engineering", False)
    formatted_results = format_search_results(results)
    print(formatted_results)


if __name__ == "__main__":
    try:
        example_usage()
    except Exception as e:
        print(f"Error running example: {e}")