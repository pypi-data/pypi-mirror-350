# jload

A simple utility to load and save lists of dictionaries from/to JSON and JSONL files, with automatic format detection.

## Installation

```bash
pip install jload
```

## Usage

```python
from jload import jload, jsave

# File extension doesn't matter - format is auto-detected between json and jsonl
data = jload('path/to/any_file')

# List of dictionaries to save
data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]

# Save as JSONL
jsave(data, 'output.jsonl', format='jsonl')

# Auto-detect format based on file extension
jsave(data, 'output.jsonl')  # Will be saved as JSONL
jsave(data, 'output.json')   # Will be saved as JSON, with auto indent
```

## Features

- **Format Auto-detection**: 
  - When loading: Automatically detects if a file contains JSON or JSONL (JSON Lines) format
  - When saving: Determines format based on file extension (.jsonl/.ndjson for JSONL, anything else for JSON)
- **Flexible Parsing**: 
  - Handles JSON arrays of dictionaries
  - Handles single JSON objects (returns as a list with one dictionary)
  - Handles JSONL with one JSON object per line
- **Error Handling**: Provides meaningful error messages for invalid files or formats
- **Lightweight**: No dependencies beyond Python's standard library

## Function Details

### jload

```python
def jload(file_path: str) -> list[dict]:
    """
    Loads a list of dictionaries from a file, attempting to auto-detect
    if it's a single JSON array/object or JSONL (JSON Lines).
    The function prioritizes content analysis over file extension.

    Args:
        file_path (str): The path to the data file.

    Returns:
        list[dict]: A list of dictionaries loaded from the file.
                    - If the file content is a JSON array of objects, it's returned as is.
                    - If the file content is a single JSON object, it's returned as a list
                      containing that single object.
                    - If the file content appears to be JSONL, each line that is a valid
                      JSON object is included in the returned list.
                    - Returns an empty list if the file is empty.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file content cannot be interpreted as either
                    a JSON array/object or JSONL format.
    """
```

### jsave

```python
def jsave(data, file_path: str, format: str = 'auto', indent: int = 2) -> None:
    """
    Saves data to a file in either JSON or JSONL format.

    Args:
        data: The data to save.
            - For 'json' format: Can be any JSON-serializable data (dict, list, str, int, etc.)
            - For 'jsonl' format: Must be a list of dictionaries
        file_path (str): The path where the file will be saved.
        format (str, optional): The format to save in. Options:
            - 'auto': Determine format based on file extension (.jsonl/.ndjson for JSONL, anything else for JSON)
            - 'json': Save as a JSON document
            - 'jsonl': Save as JSONL (one JSON object per line)
            Defaults to 'auto'.
        indent (int, optional): Number of spaces for indentation in JSON format.
            Only applies to 'json' format, ignored for 'jsonl'. Defaults to 2.

    Raises:
        ValueError: If format is 'jsonl' but data is not a list of dictionaries,
                    or if an invalid format is specified.
        TypeError: If data is not JSON-serializable.
        IOError: If there's an error writing to the file.
    """
```

## Examples

### Example 1: Loading a JSON array of objects

**data.json**:
```json
[
  {"name": "Alice", "age": 30},
  {"name": "Bob", "age": 25}
]
```

**Python code**:
```python
from jload import jload

data = jload('data.json')
print(data)
# Output: [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
```

### Example 2: Loading a single JSON object

**data.json**:
```json
{"name": "Alice", "age": 30}
```

**Python code**:
```python
from jload import jload

data = jload('data.json')
print(data)
# Output: [{'name': 'Alice', 'age': 30}]
```

### Example 3: Loading a JSONL file

**data.jsonl**:
```
{"name": "Alice", "age": 30}
{"name": "Bob", "age": 25}
```

**Python code**:
```python
from jload import jload

data = jload('data.jsonl')
print(data)
# Output: [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
```

### Example 4: Saving data as JSON

```python
from jload import jsave

data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
jsave(data, 'output.json')
```

**output.json**:
```json
[
  {
    "name": "Alice",
    "age": 30
  },
  {
    "name": "Bob",
    "age": 25
  }
]
```

### Example 5: Saving data as JSONL

```python
from jload import jsave

data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
jsave(data, 'output.jsonl')
```

**output.jsonl**:
```
{"name":"Alice","age":30}
{"name":"Bob","age":25}
```

## Requirements

- Python 3.7+

## License

MIT License

## Contributing

Issues and pull requests are welcome at [https://github.com/Imbernoulli/jload/issues](https://github.com/Imbernoulli/jload/issues)