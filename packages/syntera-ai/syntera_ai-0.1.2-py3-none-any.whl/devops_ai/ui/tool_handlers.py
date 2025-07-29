import os
import subprocess
from typing import Optional, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from ..core import DevOpsAITools


class ToolHandlers:
    """Handlers for each tool in the DevOps AI Dashboard."""

    def __init__(self, devops_tools: DevOpsAITools, console: Console):
        self.devops_tools = devops_tools
        self.console = console
        self.github_repo_url = None
        self.local_repo_path = None

    def set_repository(self, github_repo_url: str) -> Tuple[str, str]:
        """Set and clone the GitHub repository."""
        self.github_repo_url = github_repo_url

        # Clone the repo if not already present
        repo_name = github_repo_url.rstrip('/').split('/')[-1]
        local_repo_path = os.path.join(os.getcwd(), repo_name)
        clone_output = ""

        if not os.path.exists(local_repo_path):
            self.console.print(f"[bold cyan]Cloning repository to:[/] [italic blue]{local_repo_path}[/italic blue]")
            try:
                result = subprocess.run([
                    "git", "clone", github_repo_url, local_repo_path
                ], capture_output=True, text=True, check=True)
                clone_output = result.stdout + "\n" + result.stderr
            except subprocess.CalledProcessError as e:
                clone_output = e.stdout + "\n" + e.stderr
        else:
            self.console.print(f"[bold green]Repository already cloned at:[/] [italic blue]{local_repo_path}[/italic blue]")

        self.local_repo_path = local_repo_path
        self.console.print(f"[bold cyan]Working with repository:[/] [italic blue]{github_repo_url}[/italic blue]")

        return clone_output, local_repo_path

    def analyze_logs(self) -> Tuple[str, str]:
        """Handle log analysis tool."""
        # Get log file path from user
        log_file = self.console.input("[bold green]►[/bold green] [bold cyan]Enter log file path[/bold cyan]")

        # Process the log file
        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Analyzing logs...[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]Please wait[/bold cyan]"),
        ) as progress:
            task = progress.add_task("Analyzing", total=100)
            progress.update(task, advance=50)
            result = self.devops_tools._analyze_logs(log_file)
            progress.update(task, advance=50)

        return result, "📊 Log Analysis Results"

    def infrastructure(self) -> Tuple[str, str]:
        """Handle infrastructure suggestions tool."""
        result = ""

        # Check if GitHub repo URL is available
        if self.github_repo_url:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold cyan]Analyzing repository and generating infrastructure suggestions...[/bold cyan]"),
                BarColumn(bar_width=40),
                TextColumn("[bold cyan]Please wait[/bold cyan]"),
            ) as progress:
                task = progress.add_task("Infrastructure Analysis", total=100)
                progress.update(task, advance=50)
                try:
                    # Use local repo path for deeper analysis and generate IAC
                    result = self.devops_tools._infra_suggest(
                        context="",
                        repo_path=self.local_repo_path,
                        generate_iac=True
                    )
                except Exception as e:
                    result = f"Error generating infrastructure suggestions: {str(e)}\nPlease try again or provide more specific context."
                progress.update(task, advance=50)
        else:
            # No GitHub repo set, ask for manual context input
            context = self.console.input("[bold green]►[/bold green] [bold cyan]Enter infrastructure context[/bold cyan]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold cyan]Generating infrastructure suggestions...[/bold cyan]"),
                BarColumn(bar_width=40),
            ) as progress:
                task = progress.add_task("Generating", total=100)
                progress.update(task, advance=50)
                try:
                    result = self.devops_tools._infra_suggest(
                        context=context,
                        generate_iac=True
                    )
                except Exception as e:
                    result = f"Error generating infrastructure suggestions: {str(e)}\nPlease try again or provide more specific context."
                progress.update(task, advance=50)

        # Ensure we always return a non-empty result
        if not result or result.strip() == "":
            result = "No infrastructure suggestions could be generated. Please try again with a different repository or more specific context."

        return result, "🏗️ Infrastructure Recommendations"

    def security_scan(self) -> Tuple[str, str]:
        """Handle security scan tool."""
        # Get target from user
        target = self.console.input("[bold green]►[/bold green] [bold cyan]Enter target to scan[/bold cyan]")

        # Process the security scan
        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Scanning for security issues...[/bold cyan]"),
            BarColumn(bar_width=40),
        ) as progress:
            task = progress.add_task("Scanning", total=100)
            progress.update(task, advance=50)
            result = self.devops_tools._security_scan(target)
            progress.update(task, advance=50)

        return result, "🔒 Security Scan Results"

    def optimize(self) -> Tuple[str, str]:
        """Handle optimization tool."""
        # Get context from user
        context = self.console.input("[bold green]►[/bold green] [bold cyan]Enter optimization context[/bold cyan]")

        # Process the optimization
        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Generating optimization recommendations...[/bold cyan]"),
            BarColumn(bar_width=40),
        ) as progress:
            task = progress.add_task("Optimizing", total=100)
            progress.update(task, advance=50)
            result = self.devops_tools._optimize(context)
            progress.update(task, advance=50)

        return result, "⚡ Optimization Recommendations"

    def git_ingest(self) -> Tuple[str, str]:
        """Handle git ingest tool."""
        if not self.github_repo_url:
            return "GitHub repository URL not set. Please restart or set it.", "⚙️ Git Ingest Error"

        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Ingesting repository...[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]Please wait[/bold cyan]"),
        ) as progress:
            task = progress.add_task("Ingesting", total=100)
            progress.update(task, advance=50)
            try:
                result = self.devops_tools._git_ingest(self.github_repo_url)
            except AttributeError:
                result = f"Git ingest functionality for '{self.github_repo_url}' is under development."
            progress.update(task, advance=50)

        return result, "⚙️ Git Ingest Results"

    def code_quality(self) -> Tuple[str, str]:
        """Handle code quality tool."""
        if not self.github_repo_url:
            return "GitHub repository URL not set. Please restart or set it.", "🧑‍💻 Code Quality Error"

        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Analyzing code quality...[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]Please wait[/bold cyan]"),
        ) as progress:
            task = progress.add_task("CodeQuality", total=100)
            progress.update(task, advance=50)
            result = self.devops_tools._code_quality(self.github_repo_url)
            progress.update(task, advance=50)

        return result, "🧑‍💻 Code Quality Analysis"

    def dependency_check(self) -> Tuple[str, str]:
        """Handle dependency check tool."""
        if not self.github_repo_url:
            return "GitHub repository URL not set. Please restart or set it.", "📦 Dependency Check Error"

        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Checking dependencies...[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]Please wait[/bold cyan]"),
        ) as progress:
            task = progress.add_task("DependencyCheck", total=100)
            progress.update(task, advance=50)
            result = self.devops_tools._dependency_check(self.github_repo_url)
            progress.update(task, advance=50)

        return result, "📦 Dependency Check Results"

    def contributors(self) -> Tuple[str, str]:
        """Handle contributors tool."""
        if not self.github_repo_url:
            return "GitHub repository URL not set. Please restart or set it.", "👥 Contributors Error"

        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Fetching contributor statistics...[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]Please wait[/bold cyan]"),
        ) as progress:
            task = progress.add_task("Contributors", total=100)
            progress.update(task, advance=50)
            result = self.devops_tools._contributors(self.github_repo_url)
            progress.update(task, advance=50)

        return result, "👥 Contributor Statistics"

    def docker_generation(self) -> Tuple[str, str]:
        """Handle docker generation tool."""
        if not self.github_repo_url:
            return "GitHub repository URL not set. Please restart or set it.", "🐳 Docker Generation Error"

        result = ""
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Analyzing repository and generating Docker files...[/bold cyan]"),
            BarColumn(bar_width=40),
            TextColumn("[bold cyan]Please wait[/bold cyan]"),
        ) as progress:
            task = progress.add_task("DockerGeneration", total=100)
            progress.update(task, advance=50)
            # Use the local repo path for Docker generation
            result = self.devops_tools._docker_generation(self.local_repo_path)
            progress.update(task, advance=50)

        return result, "🐳 Docker Generation Results"