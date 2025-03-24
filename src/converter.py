def generate_requirements(dependencies, output_file):
    """Generate a requirements.txt file"""
    with open(output_file, "w", encoding="utf-8") as file:
        for package in dependencies:
            version = get_latest_version(package)
            file.write(f"{package}=={version}\n" if version else f"{package}\n")
    print(f"✅ Requirements file saved as {output_file}")

def generate_pipfile(dependencies, output_file):
    """Generate a Pipfile"""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("[packages]\n")
        for package in dependencies:
            version = get_latest_version(package)
            file.write(f'"{package}" = "*"\n' if not version else f'"{package}" = "{version}"\n')
    print(f"✅ Pipfile saved as {output_file}")

def generate_pyproject(dependencies, output_file):
    """Generate a pyproject.toml file"""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("[tool.poetry.dependencies]\npython = \">=3.7\"\n")
        for package in dependencies:
            version = get_latest_version(package)
            file.write(f'"{package}" = "*"\n' if not version else f'"{package}" = "{version}"\n')
    print(f"✅ pyproject.toml saved as {output_file}")
