import os
import ast
import requests
from packaging.version import parse

def fetch_dependencies(project_dir, interactive, fix_missing):
    """Scans project files and generates requirements.txt"""
    dependencies = set()
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                dependencies.add(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            dependencies.add(node.module)
    
    resolved = resolve_versions(dependencies)
    if interactive:
        resolved = user_confirm_dependencies(resolved)
    if fix_missing:
        install_missing_dependencies(resolved)
    
    with open("requirements.txt", "w") as req_file:
        req_file.writelines([f"{dep}=={ver}\n" for dep, ver in resolved.items()])
    print("requirements.txt generated successfully!")

def resolve_versions(dependencies):
    """Fetches latest compatible versions from PyPI"""
    resolved = {}
    for dep in dependencies:
        try:
            response = requests.get(f"https://pypi.org/pypi/{dep}/json")
            if response.status_code == 200:
                version = response.json()["info"]["version"]
                resolved[dep] = version
        except Exception:
            print(f"Warning: Could not resolve version for {dep}")
    return resolved

def user_confirm_dependencies(dependencies):
    """Interactive mode for user confirmation"""
    confirmed = {}
    for dep, ver in dependencies.items():
        user_input = input(f"Use {dep}=={ver}? (Y/n): ").strip().lower()
        if user_input in ('', 'y'):
            confirmed[dep] = ver
    return confirmed

def install_missing_dependencies(dependencies):
    """Automatically installs missing dependencies"""
    for dep, ver in dependencies.items():
        os.system(f"pip install {dep}=={ver}")
        print(f"Installed {dep}=={ver}")