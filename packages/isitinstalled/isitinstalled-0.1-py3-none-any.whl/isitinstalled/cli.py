import typer
from .checker import check_tools

app = typer.Typer()

@app.command()
def main(tools: list[str]):
    check_tools(tools)
