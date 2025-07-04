import os

EXCLUDED_DIRS = {'node_modules', 'venv', '__pycache__', 'alembic'}

def generate_file_structure(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for current_path, dirs, files in os.walk(root_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            depth = current_path.replace(root_dir, '').count(os.sep)
            indent = '    ' * depth
            folder_name = os.path.basename(current_path) or os.path.basename(root_dir)
            f.write(f'{indent}[{folder_name}]\n')
            
            for file in files:
                f.write(f'{indent}    {file}\n')

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_directory, 'file_structure.txt')
    generate_file_structure(current_directory, output_path)
    print(f'File structure saved to {output_path}')
