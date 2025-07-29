import os
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from dotenv import load_dotenv
from .core import DevOpsAITools
from .dashboard import TextDashboard
from devops_ai.agents.infra_suggest import InfraSuggestAgent  # Assuming this contains initialized InfraSuggestAgent
import pkg_resources

# Initialize Typer app
app = typer.Typer(help="SynteraAI - AI-powered DevOps CLI tool")
console = Console()

# Load environment variables
load_dotenv()

# Initialize tools
devops_tools = DevOpsAITools()

def _display_result(result: str, title: str):
    """Display results in a formatted table"""
    table = Table(
        title=title,
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
        title_style="bold cyan"
    )
    table.add_column("Content", style="dim")
    
    # Split the result into sections and format them
    sections = result.split("\n\n")
    for section in sections:
        if section.strip():
            # Try to detect code blocks and apply syntax highlighting
            if "```" in section:
                code_blocks = section.split("```")
                for i, block in enumerate(code_blocks):
                    if i % 2 == 1:  # Code block
                        try:
                            highlighted = Syntax(block, "python", theme="monokai")
                            table.add_row(highlighted)
                        except:
                            table.add_row(block)
                    else:  # Regular text
                        table.add_row(block)
            else:
                table.add_row(section)
    
    console.print(table)

@app.command()
def dashboard():
    """Launch the SynteraAI DevOps Dashboard."""
    TextDashboard().run()

@app.command()
def analyze_logs(
    log_file: str = typer.Argument(..., help="Path to the log file to analyze")
):
    """📊 Analyze log files for errors and patterns."""
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing logs...", total=100)
        result = devops_tools._analyze_logs(log_file)
        progress.update(task, completed=100)
    
    _display_result(result, "📊 Log Analysis Results")

@app.command()
def infra_suggest(
    context: Optional[str] = typer.Argument(
        None,
        help="Optional natural language context for infrastructure suggestions"
    ),
    repo_path: Optional[str] = typer.Option(
        None,
        "--repo",
        "-r",
        help="Path to local Git repository for contextual analysis"
    )
):
    """
    🏗️ Get AI-powered infrastructure suggestions.
    
    Example:
      infra-suggest "Python Flask app with Redis cache and PostgreSQL DB" --repo ./myapp
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Generating infrastructure suggestions...[/bold cyan]"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    ) as progress:
        task = progress.add_task("Processing", total=100)
        progress.update(task, advance=20)

        try:
            if repo_path:
                logger.info(f"Using repository context from {repo_path}")
                result = devops_tools._infra_suggest(context=context, repo_path=repo_path)
            else:
                logger.info("No repository provided, using only manual context")
                result = devops_tools._infra_suggest(context=context)
        except Exception as e:
            logger.error(f"Error generating infrastructure suggestion: {e}")
            result = f"[ERROR] {str(e)}"

        progress.update(task, completed=100)

    _display_result(result, "🏗️ Infrastructure Recommendations")

@app.command()
def security_scan(
    target: str = typer.Argument(None, help="Optional target to scan")
):
    """🔒 Perform security analysis and get recommendations."""
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning for security issues...", total=100)
        result = devops_tools._security_scan(target)
        progress.update(task, completed=100)
    
    _display_result(result, "🔒 Security Scan Results")

@app.command()
def optimize(
    context: str = typer.Argument(None, help="Optional context for optimization")
):
    """⚡ Get performance optimization recommendations."""
    with Progress() as progress:
        task = progress.add_task("[cyan]Generating optimization recommendations...", total=100)
        result = devops_tools._optimize(context)
        progress.update(task, completed=100)
    
    _display_result(result, "⚡ Optimization Recommendations")

@app.command()
def version():
    """Show version information for syntera-ai and its dependencies."""
    try:
        # Get syntera-ai version
        syntera_version = pkg_resources.get_distribution("syntera-ai").version
        
        # Get gitingest version
        gitingest_version = pkg_resources.get_distribution("gitingest").version
        
        console.print("\n[bold cyan]Version Information:[/bold cyan]")
        console.print(f"syntera-ai: [bold green]{syntera_version}[/bold green]")
        console.print(f"gitingest: [bold green]{gitingest_version}[/bold green]")
        
    except pkg_resources.DistributionNotFound as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error getting version information:[/bold red] {str(e)}")

@app.command()
def dependencies():
    """Show all dependencies and their versions used in the project."""
    try:
        # Get all installed packages
        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        
        # Create a table to display dependencies
        table = Table(
            title="Project Dependencies",
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
            title_style="bold cyan"
        )
        table.add_column("Package", style="dim")
        table.add_column("Version", style="green")
        
        # Core dependencies
        core_deps = [
            "typer",
            "rich",
            "python-dotenv",
            "gitingest",
            "langchain",
            "openai",
            "anthropic",
            "pydantic",
            "fastapi",
            "uvicorn",
            "jinja2",
            "pyyaml",
            "requests",
            "python-multipart",
            "python-jose",
            "passlib",
            "bcrypt",
            "aiofiles",
            "python-magic",
            "watchdog"
        ]
        
        # Add core dependencies to table
        for dep in sorted(core_deps):
            version = installed_packages.get(dep.lower(), "Not installed")
            table.add_row(dep, version)
        
        console.print("\n[bold cyan]Core Dependencies:[/bold cyan]")
        console.print(table)
        
        # Show syntera-ai version
        try:
            syntera_version = pkg_resources.get_distribution("syntera-ai").version
            console.print(f"\n[bold cyan]syntera-ai version:[/bold cyan] [bold green]{syntera_version}[/bold green]")
        except pkg_resources.DistributionNotFound:
            console.print("\n[bold red]syntera-ai is not installed as a package[/bold red]")
        
    except Exception as e:
        console.print(f"[bold red]Error getting dependency information:[/bold red] {str(e)}")

def main():
    """Main entry point for the CLI"""
    app()

if __name__ == "__main__":
    main() 