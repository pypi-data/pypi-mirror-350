import typer

from datazone.cli.dataset.view.create import create
from datazone.cli.dataset.view.list import list_func
from datazone.cli.dataset.view.delete import delete

app = typer.Typer()
app.command()(create)
app.command(name="list")(list_func)
app.command()(delete)
