import typer

from datazone.cli.pipeline.create import create

app = typer.Typer()
app.command()(create)
