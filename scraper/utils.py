import os

LAST_INDEX_PATH = "last_index.txt"

def get_last_index(path=LAST_INDEX_PATH):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return int(f.read().strip())
    return 1

def save_last_index(index, path=LAST_INDEX_PATH):
    with open(path, 'w') as f:
        f.write(str(index))

def reset_index(path=LAST_INDEX_PATH):
    with open(path, 'w') as f:
        f.write('1')
