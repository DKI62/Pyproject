# main.py
import os
from utilts import get_last_operations

def main():
    """
    Основная функция.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(project_root, 'operations.json')
    last_operations = get_last_operations(file_path)
    for op in last_operations:
        print(op)

if __name__ == "__main__":
    main()
