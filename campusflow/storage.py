"""JSON persistence (Issue 6). Only this module reads or writes the file."""

import json
import os

DEFAULT_PATH = os.path.join("data", "tickets.json")


def load_tickets(path=DEFAULT_PATH):
    """Return the list of tickets stored at path."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as err:
        raise ValueError("Malformed JSON structure.") from err

    if not isinstance(data, list):
        raise ValueError("JSON data must be a list.")
        
    return data


def save_tickets(tickets, path=DEFAULT_PATH):
    """Write tickets to path as JSON.

    Create the folder if it does not exist.
    A failed save must not leave the old file half-written or empty.
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
        
    tmp_path = path + ".tmp"
    
    try:
        # Step 1: Write to temporary file
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(tickets, f)
            
        # Step 2: Swap the temporary file over the real path
        os.replace(tmp_path, path)
        
    except Exception:
        # Step 3: Safety net clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
