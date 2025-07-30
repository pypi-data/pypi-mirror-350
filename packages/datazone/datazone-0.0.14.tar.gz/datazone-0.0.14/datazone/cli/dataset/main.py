import typer

from datazone.cli.dataset.show import show
from datazone.cli.dataset.transactions import transactions
from datazone.cli.dataset.list import list_func
from datazone.cli.dataset.view.main import app as view_app

app = typer.Typer()
app.command()(show)
app.command()(transactions)
app.command(name="list")(list_func)
app.add_typer(view_app, name="view")
