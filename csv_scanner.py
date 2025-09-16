#!/usr/bin/env python3
"""
CSV Scanner and Keyword Search Utility

This script provides functionality to:
1. Recursively scan directories for CSV files
2. Store file paths for quick access
3. Search for keywords across all found CSV files
4. Return file paths and matching rows

Usage:
    python csv_scanner.py /path/to/directory keyword
    
Or use as a module:
    from csv_scanner import CSVScanner
    scanner = CSVScanner('/path/to/directory')
    results = scanner.search_keyword('keyword')
"""

import os
import csv
import argparse
import sys
from typing import List, Dict, Tuple, Optional


class CSVScanner:
    """A utility class for scanning directories and searching CSV files."""
    
    def __init__(self, root_directory: str):
        """
        Initialize the CSV scanner with a root directory.
        
        Args:
            root_directory (str): The root directory to scan for CSV files
        """
        self.root_directory = os.path.abspath(root_directory)
        self.csv_files: List[str] = []
        self._scan_directory()
    
    def _scan_directory(self) -> None:
        """
        Recursively scan the directory and collect all CSV file paths.
        """
        if not os.path.exists(self.root_directory):
            raise ValueError(f"Directory does not exist: {self.root_directory}")
        
        if not os.path.isdir(self.root_directory):
            raise ValueError(f"Path is not a directory: {self.root_directory}")
        
        self.csv_files = []
        for root, dirs, files in os.walk(self.root_directory):
            for file in files:
                if file.lower().endswith('.csv'):
                    full_path = os.path.join(root, file)
                    self.csv_files.append(full_path)
    
    def get_csv_files(self) -> List[str]:
        """
        Get the list of all discovered CSV files.
        
        Returns:
            List[str]: List of full paths to CSV files
        """
        return self.csv_files.copy()
    
    def search_keyword(self, keyword: str, case_sensitive: bool = False) -> List[Dict]:
        """
        Search for a keyword across all CSV files.
        
        Args:
            keyword (str): The keyword to search for
            case_sensitive (bool): Whether the search should be case sensitive
            
        Returns:
            List[Dict]: List of dictionaries containing:
                - file_path: Path to the file containing the keyword
                - row_number: Row number (1-indexed) where keyword was found
                - row_data: The actual row data as a list
                - matching_columns: List of column indices where keyword was found
        """
        if not keyword:
            raise ValueError("Keyword cannot be empty")
        
        results = []
        search_keyword = keyword if case_sensitive else keyword.lower()
        
        for file_path in self.csv_files:
            try:
                results.extend(self._search_file(file_path, search_keyword, case_sensitive))
            except Exception as e:
                print(f"Warning: Error reading file {file_path}: {e}", file=sys.stderr)
                continue
        
        return results
    
    def _search_file(self, file_path: str, keyword: str, case_sensitive: bool) -> List[Dict]:
        """
        Search for keyword in a specific CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            keyword (str): Keyword to search for (already processed for case)
            case_sensitive (bool): Whether search is case sensitive
            
        Returns:
            List[Dict]: List of matching rows with metadata
        """
        matches = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                # Try to detect the CSV dialect
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                
                try:
                    dialect = sniffer.sniff(sample)
                except csv.Error:
                    # Fall back to default dialect
                    dialect = csv.excel
                
                reader = csv.reader(csvfile, dialect)
                
                for row_number, row in enumerate(reader, 1):
                    matching_columns = []
                    
                    for col_index, cell in enumerate(row):
                        cell_content = str(cell) if case_sensitive else str(cell).lower()
                        if keyword in cell_content:
                            matching_columns.append(col_index)
                    
                    if matching_columns:
                        matches.append({
                            'file_path': file_path,
                            'row_number': row_number,
                            'row_data': row,
                            'matching_columns': matching_columns
                        })
        
        except UnicodeDecodeError:
            # Try with different encodings
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(file_path, 'r', encoding=encoding, newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        for row_number, row in enumerate(reader, 1):
                            matching_columns = []
                            for col_index, cell in enumerate(row):
                                cell_content = str(cell) if case_sensitive else str(cell).lower()
                                if keyword in cell_content:
                                    matching_columns.append(col_index)
                            
                            if matching_columns:
                                matches.append({
                                    'file_path': file_path,
                                    'row_number': row_number,
                                    'row_data': row,
                                    'matching_columns': matching_columns
                                })
                    break
                except UnicodeDecodeError:
                    continue
        
        return matches
    
    def refresh_scan(self) -> None:
        """
        Re-scan the directory to pick up any new CSV files.
        """
        self._scan_directory()
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the scanned directory.
        
        Returns:
            Dict[str, int]: Dictionary with statistics
        """
        return {
            'total_csv_files': len(self.csv_files),
            'total_directories_scanned': len(set(os.path.dirname(f) for f in self.csv_files))
        }


def format_search_results(results: List[Dict], max_row_display: int = 100) -> str:
    """
    Format search results for display.
    
    Args:
        results (List[Dict]): Search results from CSVScanner.search_keyword()
        max_row_display (int): Maximum characters to display per row
        
    Returns:
        str: Formatted results string
    """
    if not results:
        return "No matches found."
    
    output = []
    output.append(f"Found {len(results)} matching rows in {len(set(r['file_path'] for r in results))} files:\n")
    
    current_file = None
    for result in results:
        if result['file_path'] != current_file:
            current_file = result['file_path']
            output.append(f"\nFile: {current_file}")
        
        row_str = str(result['row_data'])
        if len(row_str) > max_row_display:
            row_str = row_str[:max_row_display] + "..."
        
        output.append(f"  Row {result['row_number']}: {row_str}")
        output.append(f"    Matching columns: {result['matching_columns']}")
    
    return "\n".join(output)


def main():
    """Command line interface for the CSV scanner."""
    parser = argparse.ArgumentParser(
        description="Recursively scan directories for CSV files and search for keywords",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv_scanner.py /path/to/data keyword
  python csv_scanner.py /home/user/documents "John Doe" --case-sensitive
  python csv_scanner.py . email --stats
        """
    )
    
    parser.add_argument('directory', help='Root directory to scan for CSV files')
    parser.add_argument('keyword', help='Keyword to search for in CSV files')
    parser.add_argument('--case-sensitive', action='store_true',
                        help='Perform case-sensitive search')
    parser.add_argument('--stats', action='store_true',
                        help='Show statistics about scanned files')
    parser.add_argument('--max-display', type=int, default=100,
                        help='Maximum characters to display per row (default: 100)')
    
    args = parser.parse_args()
    
    try:
        # Initialize scanner
        scanner = CSVScanner(args.directory)
        
        # Show stats if requested
        if args.stats:
            stats = scanner.get_stats()
            print(f"Statistics:")
            print(f"  Total CSV files found: {stats['total_csv_files']}")
            print(f"  Directories scanned: {stats['total_directories_scanned']}")
            print()
        
        # Perform search
        print(f"Searching for '{args.keyword}' in {len(scanner.get_csv_files())} CSV files...")
        results = scanner.search_keyword(args.keyword, args.case_sensitive)
        
        # Display results
        print(format_search_results(results, args.max_display))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()