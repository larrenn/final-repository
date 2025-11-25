import os
from pathlib import Path

def print_project_structure(startpath, max_depth=4):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level > max_depth:
            continue
            
        indent = ' ' * 2 * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith(('.py', '.c', '.h', '.resc', '.ini', '.yml', '.md')):
                print(f"{subindent}📄 {file}")

if __name__ == "__main__":
    project_path = r"C:\Users\Student\Desktop\final work\final-repository"
    print("🌳 СТРУКТУРА ПРОЕКТА:")
    print("=" * 50)
    print_project_structure(project_path)