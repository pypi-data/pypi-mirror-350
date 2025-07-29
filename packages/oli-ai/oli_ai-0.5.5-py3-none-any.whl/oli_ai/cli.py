"""Console script for oli_ai."""
import oli_ai

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for oli_ai."""
    console.print("Replace this message by putting your code into "
               "oli_ai.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
