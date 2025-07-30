import json
import os

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


def jsave(data: list[dict], file_path: str, format: str = 'auto', indent: int = 2) -> None:
    """
    Saves a list of dictionaries to a file in either JSON or JSONL format.

    Args:
        data (list[dict]): The list of dictionaries to save.
        file_path (str): The path where the file will be saved.
        format (str, optional): The format to save in. Options:
            - 'auto': Determine format based on file extension (.jsonl/.ndjson for JSONL, anything else for JSON)
            - 'json': Save as a JSON array
            - 'jsonl': Save as JSONL (one JSON object per line)
            Defaults to 'auto'.
        indent (int, optional): Number of spaces for indentation in JSON format.
            Only applies to 'json' format, ignored for 'jsonl'. Defaults to 2.

    Raises:
        ValueError: If data is not a list of dictionaries or if an invalid format is specified.
        IOError: If there's an error writing to the file.
    """
    # Validate input data
    if not isinstance(data, list):
        raise ValueError("Data must be a list")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("All items in data must be dictionaries")
    
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
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            if format == 'json':
                # Save as a JSON array with specified indentation
                json.dump(data, f, indent=indent)
            else:  # format == 'jsonl'
                # Save as JSONL (one object per line, no indentation)
                for item in data:
                    f.write(json.dumps(item) + '\n')
    except Exception as e:
        raise IOError(f"Error writing to file '{file_path}': {e}")


# To make `from jload import jload, jsave` work directly
__all__ = ['jload', 'jsave']