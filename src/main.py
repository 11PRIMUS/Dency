import os
import ast
import requests
import pkgutil

STANDARD_LIBS = set(module.name for module in pkgutil.iter_modules() if module.module_finder is None)

def extract_imports_from_file(file_path):
    """Extract imported modules from a Python file."""
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
        except SyntaxError:
            return set()
        
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        
        return imports

def scan_project_for_imports(directory):
    """Scan all Python files in a directory and extract unique third-party imports."""
    all_imports = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_imports.update(extract_imports_from_file(file_path))

    return all_imports - STANDARD_LIBS

def get_latest_version(package_name):
    """Fetch the latest version of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()["info"]["version"]
    except requests.RequestException:
        pass
    return None
