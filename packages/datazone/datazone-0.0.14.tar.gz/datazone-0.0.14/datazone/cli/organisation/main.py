import typer

from datazone.cli.organisation.list import list_func
from datazone.cli.organisation.switch import switch

app = typer.Typer()
app.command(name="list")(list_func)
app.command()(switch)
