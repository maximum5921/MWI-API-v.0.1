import os

LAST_INDEX_PATH = "last_index.txt"

def get_last_index(path=LAST_INDEX_PATH):
    """
    Reads the last processed index from a file.
    If the file does not exist, it returns 1 as the starting index.

    Args:
        path (str): The path to the file storing the last index.

    Returns:
        int: The last processed index.
    """
    if os.path.exists(path):
        with open(path, 'r') as f:
            return int(f.read().strip())
    return 1

def save_last_index(index, path=LAST_INDEX_PATH):
    """
    Saves the current index to a file.

    Args:
        index (int): The index to save.
        path (str): The path to the file where the index will be saved.
    """
    with open(path, 'w') as f:
        f.write(str(index))

def reset_index(path=LAST_INDEX_PATH):
    """
    Resets the last processed index in the file to 1.

    Args:
        path (str): The path to the file where the index is stored.
    """
    with open(path, 'w') as f:
        f.write('1')
