import os
import ast
import sys
import requests
import argparse
import pkgutil
import click

STANDARD_LIBS = set(module.name for module in pkgutil.iter_modules() if module.module_finder is None) #standard lib


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
            elif isinstance(node, ast.ImportFrom):
                if node.module:
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
    
    return all_imports - STANDARD_LIBS  # Remove standard libraries


def get_latest_version(package_name):
    """Fetch pack"""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["info"]["version"]
    except requests.RequestException:
        pass
    return None


def generate_requirements_file(dependencies, output_file):
    """Generate a requirements.txt file from the dependencies list."""
    with open(output_file, "w", encoding="utf-8") as file:
        for package in dependencies:
            version = get_latest_version(package)
            if version:
                file.write(f"{package}=={version}\n")
            else:
                file.write(f"{package}\n")  # If version fetch fails, write package name only
    click.echo(f" Requirements file saved as {output_file}")


@click.command()
@click.option('--dir', required=True, help='Project directory to scan.')
@click.option('--output', default='requirements.txt', help='Output file name.')
def main(dir, output):
    click.echo(" Scanning project for dependencies...")
    dependencies = scan_project_for_imports(dir)
    if not dependencies:
        click.echo(" No dependencies found.")
        sys.exit(0)
    
    click.echo(" Fetching latest versions...")
    generate_requirements_file(dependencies, output)


if __name__ == "__main__":
    main()
