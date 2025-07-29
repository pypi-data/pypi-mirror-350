import shutil
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()

def check_tools(tools: list[str]):
    table = Table(title="Package Check Results")
    table.add_column("Tool")
    table.add_column("Installed")
    table.add_column("Location")
    table.add_column("Version")
    table.add_column("Suggestion")

    for tool in tools:
        path = shutil.which(tool)
        if path:
            try:
                version = subprocess.check_output([tool, "--version"], text=True).strip()
            except Exception:
                version = "Unknown"
            location = "venv" if "venv" in path else "global"
            table.add_row(tool, "✅", location, version, "-")
        else:
            table.add_row(tool, "❌", "-", "-", f"pip install {tool}")

    console.print(table)
