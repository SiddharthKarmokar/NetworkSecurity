import os

def print_structure(dir_path, prefix=''):
    ignore = {'__pycache__', '.git', 'venv', '.mypy_cache', '.idea', '.vscode', '.DS_Store'}
    entries = [e for e in os.listdir(dir_path) if e not in ignore]
    entries.sort()

    for i, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        connector = '|-- ' if i < len(entries) - 1 else '`-- '
        print(prefix + connector + entry)
        if os.path.isdir(path):
            new_prefix = prefix + ('|   ' if i < len(entries) - 1 else '    ')
            print_structure(path, new_prefix)

print_structure('.')
