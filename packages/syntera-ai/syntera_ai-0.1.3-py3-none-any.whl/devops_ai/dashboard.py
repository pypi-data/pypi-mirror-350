from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt
from datetime import datetime

from typing import Dict, Callable, Tuple
from .ui.panels import (
    create_header,
    create_tools_panel,
    create_content_panel,
    create_footer,
    create_input_panel,
    create_result_table
)
from .ui.tool_handlers import ToolHandlers

import keyboard

from .core import DevOpsAITools


class TextDashboard:
    """An enhanced text-based dashboard for SynteraAI DevOps with keyboard navigation."""

    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.devops_tools = DevOpsAITools()
        self.tool_handlers = ToolHandlers(self.devops_tools, self.console)

        # Track active tool for highlighting
        self.active_tool_index = 0
        self.github_repo_url = None

    def _display_result(self, result: str, title: str) -> None:
        """Display the result in a structured and visually appealing way."""
        result_group = create_result_table(result, title)
        self.layout["content"].update(create_content_panel(result_group))

    def run(self):
        """Run the dashboard with keyboard navigation and scrolling."""
        self.console.clear()

        # Setup layout structure
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=8),
            Layout(name="input", size=3),
            Layout(name="footer", size=2),
        )

        self.layout["body"].split_row(
            Layout(name="tools", ratio=1),
            Layout(name="content", ratio=3),
        )

        # Initial layout setup
        self.layout["header"].update(create_header())
        self.layout["tools"].update(self._render_tools_panel())
        self.layout["content"].update(create_content_panel())
        self.layout["input"].update(create_input_panel())
        self.layout["footer"].update(create_footer())

        # Prompt for GitHub repository URL at startup
        self.console.print("\n")
        self.github_repo_url = Prompt.ask(
            "[bold green]►[/bold green] [bold cyan]Enter the GitHub repository URL to work on[/bold cyan]",
            default="https://github.com/example/repo "
        )
        clone_output, self.local_repo_path = self.tool_handlers.set_repository(self.github_repo_url)
        if clone_output:
            self._display_result(clone_output, "Git Clone Output")

        handlers = {
            "1": self.tool_handlers.analyze_logs,
            "2": self.tool_handlers.infrastructure,
            "3": self.tool_handlers.security_scan,
            "4": self.tool_handlers.optimize,
            "5": self.tool_handlers.git_ingest,
            "6": self.tool_handlers.code_quality,
            "7": self.tool_handlers.dependency_check,
            "8": self.tool_handlers.contributors,
            "9": self.tool_handlers.docker_generation,
        }

        # Start Live rendering
        with Live(self.layout, refresh_per_second=10, screen=True) as live:
            while True:
                key = self._get_keypress()

                if key == "q":
                    break
                elif key == "KEY_UP" or key == "k":
                    self.active_tool_index = max(0, self.active_tool_index - 1)
                elif key == "KEY_DOWN" or key == "j":
                    self.active_tool_index = min(8, self.active_tool_index + 1)

                # Update only the tools panel with the current tool
                self.layout["tools"].update(self._render_tools_panel())
                live.refresh()  # Refresh is essential for real-time updates

                if key == "\r":  # Enter key pressed
                    active_tool_key = str(self.active_tool_index + 1)
                    self.layout["input"].update(create_input_panel(f"Running {active_tool_key}..."))
                    live.refresh()

                    handler = handlers.get(active_tool_key)
                    if handler:
                        live.stop()
                        result, title = handler()
                        live.start()
                        self._display_result(result, title)

                    self.layout["input"].update(create_input_panel())
                    live.refresh()

    def _render_tools_panel(self):
        tools = [
            {"key": "1", "icon": "📊", "name": "Analyze Logs", "desc": "Analyze log files for patterns and errors"},
            {"key": "2", "icon": "🏗️", "name": "Infrastructure", "desc": "Get infrastructure recommendations"},
            {"key": "3", "icon": "🔒", "name": "Security Scan", "desc": "Perform security vulnerability scanning"},
            {"key": "4", "icon": "⚡", "name": "Optimize", "desc": "Performance optimization suggestions"},
            {"key": "5", "icon": "⚙️", "name": "Git Ingest", "desc": "Ingest and process GitHub repository"},
            {"key": "6", "icon": "🧑‍💻", "name": "Code Quality", "desc": "Analyze code quality and maintainability"},
            {"key": "7", "icon": "📦", "name": "Dependency Check", "desc": "Check outdated or vulnerable dependencies"},
            {"key": "8", "icon": "👥", "name": "Contributors", "desc": "Show contributor statistics and activity"},
            {"key": "9", "icon": "🐳", "name": "Docker Generation", "desc": "Generate Docker and docker-compose files"}
        ]

        # Get the current tool
        current_tool = tools[self.active_tool_index]

        return create_tools_panel(current_tool)

    def _get_keypress(self):
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key == 'up':
                return "KEY_UP"
            elif key == 'down':
                return "KEY_DOWN"
            elif key == 'enter':
                return "\r"
            elif key == 'q':
                return "q"
            elif key.isdigit() and 1 <= int(key) <= 9:
                return key
        return None


def main():
    """Main entry point for the dashboard."""
    dashboard = TextDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()