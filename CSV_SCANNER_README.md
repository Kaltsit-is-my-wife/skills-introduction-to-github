# CSV Scanner and Keyword Search Utility

A Python utility for recursively scanning directories for CSV files and searching for keywords within them.

## Features

- **Recursive Directory Scanning**: Automatically discovers all CSV files in a directory tree
- **Fast File Path Caching**: Stores discovered file paths in memory for quick access
- **Keyword Search**: Search for keywords across all CSV files with optional case sensitivity
- **Detailed Results**: Returns file paths, row numbers, and specific columns where keywords are found
- **Multiple Encoding Support**: Handles various text encodings (UTF-8, Latin-1, etc.)
- **Command Line Interface**: Easy-to-use CLI with various options
- **Programmatic API**: Can be imported and used as a Python module

## Installation

No additional dependencies required! The utility uses only Python standard library modules:
- `os` - for file system operations
- `csv` - for CSV file parsing
- `argparse` - for command line interface
- `sys` - for system operations
- `typing` - for type hints

## Usage

### Command Line Interface

```bash
# Basic usage
python csv_scanner.py /path/to/directory keyword

# Case-sensitive search
python csv_scanner.py /path/to/directory "Exact Match" --case-sensitive

# Show statistics about discovered files
python csv_scanner.py /path/to/directory keyword --stats

# Limit display length for long rows
python csv_scanner.py /path/to/directory keyword --max-display 50
```

#### Examples

```bash
# Search for "Engineering" in test data
python csv_scanner.py test_data "Engineering" --stats

# Case-sensitive search for "Electronics"
python csv_scanner.py test_data "Electronics" --case-sensitive

# Search for email domain
python csv_scanner.py test_data "@example.com"
```

### Programmatic Usage

```python
from csv_scanner import CSVScanner, format_search_results

# Initialize scanner
scanner = CSVScanner('/path/to/directory')

# Get list of discovered CSV files
csv_files = scanner.get_csv_files()
print(f"Found {len(csv_files)} CSV files")

# Search for keyword
results = scanner.search_keyword('Engineering', case_sensitive=False)

# Format and display results
formatted = format_search_results(results)
print(formatted)

# Get statistics
stats = scanner.get_stats()
print(f"Total files: {stats['total_csv_files']}")
print(f"Directories: {stats['total_directories_scanned']}")

# Refresh scan (if files were added/removed)
scanner.refresh_scan()
```

## API Reference

### CSVScanner Class

#### Constructor
- `CSVScanner(root_directory: str)` - Initialize scanner with root directory

#### Methods
- `get_csv_files() -> List[str]` - Get list of discovered CSV file paths
- `search_keyword(keyword: str, case_sensitive: bool = False) -> List[Dict]` - Search for keyword
- `refresh_scan() -> None` - Re-scan directory for new files
- `get_stats() -> Dict[str, int]` - Get scanning statistics

#### Search Results Format
Each search result is a dictionary with:
- `file_path`: Full path to the CSV file
- `row_number`: Row number (1-indexed) where keyword was found
- `row_data`: List containing the actual row data
- `matching_columns`: List of column indices where keyword was found

### Utility Functions

- `format_search_results(results: List[Dict], max_row_display: int = 100) -> str` - Format results for display

## Error Handling

The utility includes robust error handling for:
- Non-existent directories
- Invalid file paths
- CSV parsing errors
- Unicode/encoding issues
- Permission errors

Warnings are printed to stderr for files that cannot be read, but the scan continues.

## Performance Notes

- File paths are cached in memory for fast repeated searches
- Large CSV files are processed row-by-row to minimize memory usage
- Multiple encoding attempts for files with encoding issues
- CSV dialect detection for better parsing accuracy

## Test Data

The repository includes sample CSV files in the `test_data/` directory:
- `employees.csv` - Employee information
- `subdir1/products.csv` - Product catalog
- `subdir2/customers.csv` - Customer data

## Examples

See `example_usage.py` for comprehensive usage examples demonstrating both CLI and programmatic usage.

## License

This utility is provided as part of the GitHub Skills Introduction course materials.