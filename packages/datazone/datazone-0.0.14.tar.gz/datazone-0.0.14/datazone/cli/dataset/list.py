from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

extract_columns = ["ID", "Name", "Source", "Created At"]


def list_func(page_size: int = 20):
    response_data = CrudServiceCaller(entity_name="dataset").get_entity_list(
        params={"page_size": page_size},
    )

    console = Console()

    table = Table(*extract_columns)
    items = response_data.get("items")
    if len(items) == 0:
        console.print("[bold orange]Not created any dataset yet[/bold orange]")
        return

    for datum in items:
        values = [
            datum.get("id"),
            datum.get("name"),
            datum.get("source") or "-",
            datum.get("created_at"),
        ]
        table.add_row(*values)
    console.print(table)
