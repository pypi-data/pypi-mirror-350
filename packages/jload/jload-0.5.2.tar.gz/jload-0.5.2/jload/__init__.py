import json
import os
import fcntl
import time
from typing import Optional, Union, Dict, Any

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
                      JSON object is included in the returned list. Lines that are empty,
                      not valid JSON, or valid JSON but not an object, are skipped.
                    - Returns an empty list if the file is empty or contains no loadable dictionaries
                      after attempting both JSON and JSONL parsing.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file content cannot be interpreted as either
                    a JSON array/object or JSONL format leading to a list of dictionaries,
                    after trying both parsing methods.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File not found at '{file_path}'")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read the whole content first. This is necessary because a file
            # could be a single large JSON object that spans multiple lines,
            # or it could be JSONL.
            content = f.read()
    except Exception as e:
        raise ValueError(f"Error reading file '{file_path}': {e}")

    # Handle empty or whitespace-only file
    stripped_content = content.strip()
    if not stripped_content:
        return []

    # Attempt 1: Try to parse as a single JSON document (array of dicts or a single dict)
    try:
        data = json.loads(stripped_content)
        if isinstance(data, list):
            # If it's a list, check if all elements are dictionaries.
            # If not all are dicts, it's not a "list of dicts" as per this function's goal.
            # In such a case, we'll let it fall through to the JSONL parsing attempt,
            # as it's possible it's a malformed JSONL where the array brackets were unintended.
            if all(isinstance(item, dict) for item in data):
                return data
            # If not all items are dicts, don't return yet; try JSONL.
        elif isinstance(data, dict):
            return [data] # Single top-level object, wrap in a list
        # If it's valid JSON but not a list or a dict (e.g., a string, number, boolean),
        # it cannot be a list of dicts. Fall through to JSONL attempt.
    except json.JSONDecodeError:
        # Content is not a single valid JSON document. This is expected if it's JSONL.
        # Proceed to JSONL attempt.
        pass
    except Exception as e:
        # For other unexpected errors during the first parse attempt.
        # We might still want to try JSONL if this specific error occurs.
        # However, it's safer to report if the initial broad parse fails unexpectedly.
        # For simplicity now, we'll let it fall to JSONL, but this could be refined.
        # print(f"Initial JSON parse failed with non-JSONDecodeError: {e}. Trying JSONL.")
        pass


    # Attempt 2: Try to parse as JSONL (multiple JSON objects, one per line)
    # This attempt is made if:
    # 1. The whole content was not valid JSON (JSONDecodeError).
    # 2. The whole content was valid JSON but not a list of dicts or a single dict.
    lines = stripped_content.splitlines() # Use stripped_content to avoid issues with leading/trailing blank lines
    jsonl_data: list[dict] = []
    # successfully_parsed_any_jsonl_line = False # To track if JSONL parsing was productive

    for line_number, line_text in enumerate(lines, 1):
        line_text = line_text.strip()
        if not line_text:  # Skip empty lines within the content
            continue
        try:
            obj = json.loads(line_text)
            if isinstance(obj, dict): # Only add if the line parsed to a dictionary
                jsonl_data.append(obj)
                # successfully_parsed_any_jsonl_line = True # Mark that we found at least one
            # else: skip if line is valid JSON but not an object (e.g. a string, number)
        except json.JSONDecodeError:
            # This line is not valid JSON, skip it.
            # This is common in files that are primarily JSONL but might have comments or malformed lines.
            # print(f"Warning: Skipping invalid JSON on line {line_number} in '{file_path}'")
            continue
        except Exception as e:
            # For other unexpected errors on a specific line
            # print(f"Warning: Skipping line {line_number} in '{file_path}' due to unexpected error: {e}")
            continue # Skip line

    # Decision logic:
    # If jsonl_data has items, it means the JSONL parsing was successful for at least one line.
    # This should be preferred if the initial single-JSON parse didn't yield a list of dicts.
    if jsonl_data:
        return jsonl_data

    # If we reach here, neither attempt yielded a list of dictionaries.
    # This means:
    # - The initial parse as a single JSON document either failed or didn't result in a list of dicts/single dict.
    # - AND the subsequent parse as JSONL didn't find any lines that are valid JSON dictionaries.

    # To give a more precise error, we can re-check the first parse attempt's outcome if it didn't throw JSONDecodeError
    try:
        # This re-parse is to check if the file was valid JSON but of an unsupported type (e.g. a JSON string "hello")
        data_check = json.loads(stripped_content)
        # If json.loads succeeded but we didn't return earlier, it means it wasn't a list of dicts or a single dict.
        raise ValueError(
            f"Error: File '{file_path}' contains valid JSON, but not in the expected "
            "format of a JSON array of (or containing only) dictionaries, a single JSON object, "
            "or JSONL where lines are JSON objects. "
            f"The jload function specifically looks for a list of dictionaries. Found top-level type: {type(data_check).__name__}"
        )
    except json.JSONDecodeError:
        # This confirms the initial parse as a single JSON document failed, AND JSONL parsing yielded nothing.
        raise ValueError(
            f"Error: File '{file_path}' could not be decoded as a JSON array/object "
            "nor as JSONL consisting of dictionary objects. Please ensure the file contains valid JSON data "
            "in one of these formats."
        )
    except Exception as e: # Catch any other exception from the re-parse
        raise ValueError(f"An unexpected error occurred during final validation of '{file_path}': {e}")

def jsave_append(entry: Dict[str, Any], file_path: str, format: str = 'auto', indent: int = 2, 
                max_retries: int = 5, retry_delay: float = 0.1) -> None:
    """
    Appends a single dictionary entry to an existing JSON or JSONL file.
    
    Args:
        entry (Dict[str, Any]): The dictionary entry to append.
        file_path (str): The path to the file where the entry will be appended.
        format (str, optional): The format of the file. Options:
            - 'auto': Determine format based on file extension (.jsonl/.ndjson for JSONL, 
                      anything else for JSON)
            - 'json': Treat as a JSON array file
            - 'jsonl': Treat as a JSONL file (one JSON object per line)
            Defaults to 'auto'.
        indent (int, optional): Number of spaces for indentation in JSON format.
            Only applies to 'json' format, ignored for 'jsonl'. Defaults to 2.
        max_retries (int, optional): Maximum number of retries if file is locked. Defaults to 5.
        retry_delay (float, optional): Delay in seconds between retries. Defaults to 0.1.
            
    Raises:
        ValueError: If entry is not a dictionary, if format is invalid, or if the existing 
                   JSON file does not contain a JSON array.
        FileNotFoundError: If the file doesn't exist and needs to be created.
        IOError: If there's an error writing to the file or if max_retries is exceeded.
    """
    # Validate entry
    if not isinstance(entry, dict):
        raise ValueError("Entry must be a dictionary")
    
    # Determine format if 'auto'
    if format == 'auto':
        lower_path = file_path.lower()
        if lower_path.endswith('.jsonl') or lower_path.endswith('.ndjson'):
            format = 'jsonl'
        else:
            format = 'json'
    
    # Validate format
    if format not in ['json', 'jsonl']:
        raise ValueError(f"Invalid format: {format}. Must be 'json', 'jsonl', or 'auto'")
    
    # Handle JSONL format (simple append)
    if format == 'jsonl':
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                
                # Open file in append mode
                with open(file_path, 'a+', encoding='utf-8') as f:
                    # Acquire an exclusive lock
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    try:
                        # Write the new entry
                        f.write(json.dumps(entry) + '\n')
                    finally:
                        # Release the lock
                        fcntl.flock(f, fcntl.LOCK_UN)
                return
            except IOError as e:
                if "Resource temporarily unavailable" in str(e):
                    # File is locked by another process, retry
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise IOError(f"Failed to acquire file lock after {max_retries} attempts")
                    time.sleep(retry_delay)
                else:
                    # Other IO error
                    raise IOError(f"Error appending to file '{file_path}': {e}")
    
    # Handle JSON format (read, modify, write)
    else:  # format == 'json'
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Check if file exists
                file_exists = os.path.exists(file_path)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                
                if not file_exists:
                    # If file doesn't exist, create it with a single entry in an array
                    with open(file_path, 'w', encoding='utf-8') as f:
                        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        try:
                            json.dump([entry], f, indent=indent)
                        finally:
                            fcntl.flock(f, fcntl.LOCK_UN)
                    return
                
                # File exists, read current content
                with open(file_path, 'r+', encoding='utf-8') as f:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    try:
                        # Read existing content
                        try:
                            current_content = f.read().strip()
                            if not current_content:
                                data = []  # Empty file
                            else:
                                data = json.loads(current_content)
                        except json.JSONDecodeError:
                            raise ValueError(f"Existing file '{file_path}' does not contain valid JSON")
                        
                        # Ensure data is a list
                        if not isinstance(data, list):
                            raise ValueError(f"Existing file '{file_path}' must contain a JSON array for append operation")
                        
                        # Append the new entry
                        data.append(entry)
                        
                        # Write back to file
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f, indent=indent)
                    finally:
                        fcntl.flock(f, fcntl.LOCK_UN)
                return
            except IOError as e:
                if "Resource temporarily unavailable" in str(e):
                    # File is locked by another process, retry
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise IOError(f"Failed to acquire file lock after {max_retries} attempts")
                    time.sleep(retry_delay)
                else:
                    # Other IO error
                    raise IOError(f"Error appending to file '{file_path}': {e}")


def jsave(data, file_path: str, format: str = 'auto', indent: int = 2, append: bool = False) -> None:
    """
    Saves data to a file in either JSON or JSONL format.

    Args:
        data: The data to save.
            - For 'json' format: Can be any JSON-serializable data (dict, list, str, int, etc.)
            - For 'jsonl' format: Must be a list of dictionaries if append=False
                                 Must be a dictionary if append=True
        file_path (str): The path where the file will be saved.
        format (str, optional): The format to save in. Options:
            - 'auto': Determine format based on file extension (.jsonl/.ndjson for JSONL, anything else for JSON)
            - 'json': Save as a JSON document
            - 'jsonl': Save as JSONL (one JSON object per line)
            Defaults to 'auto'.
        indent (int, optional): Number of spaces for indentation in JSON format.
            Only applies to 'json' format, ignored for 'jsonl'. Defaults to 2.
        append (bool, optional): If True, appends data to the existing file instead of overwriting.
            - For 'json' format: data must be a dictionary, which will be appended to the existing JSON array
            - For 'jsonl' format: data must be a dictionary, which will be appended as a new line
            Defaults to False.

    Raises:
        ValueError: If data is not in the correct format for the specified file format,
                    or if an invalid format is specified.
        TypeError: If data is not JSON-serializable.
        IOError: If there's an error writing to the file.
    """
    # If append mode is requested, delegate to jsave_append for a single dictionary
    if append:
        if not isinstance(data, dict):
            raise ValueError("When append=True, data must be a dictionary")
        return jsave_append(data, file_path, format, indent)
    
    # Regular save operation (overwrite mode)
    # Determine format if 'auto'
    if format == 'auto':
        # Check file extension
        lower_path = file_path.lower()
        if lower_path.endswith('.jsonl') or lower_path.endswith('.ndjson'):
            format = 'jsonl'
        else:
            format = 'json'
    
    # Validate format
    if format not in ['json', 'jsonl']:
        raise ValueError(f"Invalid format: {format}. Must be 'json', 'jsonl', or 'auto'")
    
    # Validate data format for JSONL
    if format == 'jsonl':
        if not isinstance(data, list):
            raise ValueError("For JSONL format, data must be a list")
        
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("For JSONL format, all items in data must be dictionaries")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            if format == 'json':
                # Save as a JSON document with specified indentation
                json.dump(data, f, indent=indent)
            else:  # format == 'jsonl'
                # Save as JSONL (one object per line, no indentation)
                for item in data:
                    f.write(json.dumps(item) + '\n')
    except ValueError as e:
        # 处理循环引用等序列化错误
        if "Circular reference detected" in str(e):
            raise TypeError(f"Data is not JSON-serializable: {e}")
        else:
            # 其他ValueError可能是格式问题，保持原样
            raise
    except TypeError as e:
        raise TypeError(f"Data is not JSON-serializable: {e}")
    except Exception as e:
        raise IOError(f"Error writing to file '{file_path}': {e}")


# To make imports work
__all__ = ['jload', 'jsave', 'jsave_append']