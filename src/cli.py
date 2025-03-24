import click
from .core import scan_project_for_imports
from .converter import generate_requirements, generate_pipfile, generate_pyproject

@click.command()
@click.option('--dir', required=True, help='Project directory to scan.')
@click.option('--format', type=click.Choice(['requirements', 'pipfile', 'pyproject'], case_sensitive=False), 
              default='requirements', help='Output format (requirements, pipfile, pyproject).')
@click.option('--output', default=None, help='Output file name (default: auto-generated).')
def main(dir, format, output):
    """CLI for Dependency Fetcher"""
    click.echo("🔍 Scanning project for dependencies...")
    dependencies = scan_project_for_imports(dir)
    
    if not dependencies:
        click.echo("🚫 No dependencies found.")
        return
    
    click.echo(f"📦 Generating {format} file...")
    if output is None:
        output = f"{format}.txt" if format == "requirements" else f"{format}.toml"
    
    if format == "requirements":
        generate_requirements(dependencies, output)
    elif format == "pipfile":
        generate_pipfile(dependencies, output)
    elif format == "pyproject":
        generate_pyproject(dependencies, output)

if __name__ == "__main__":
    main()
