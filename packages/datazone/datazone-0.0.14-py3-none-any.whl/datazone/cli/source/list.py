from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller
from datazone.utils.helpers import get_created_by

source_columns = [
    "ID",
    "Name",
    "Type",
    "Created At",
    "Created By",
]


def list_func(page_size: int = 20):
    response_data = CrudServiceCaller(entity_name="source").get_entity_list(
        params={"page_size": page_size, "fetch_links": True},
    )

    console = Console()

    table = Table(*source_columns)
    for datum in response_data.get("items"):
        values = [
            datum.get("id"),
            datum.get("name"),
            datum.get("connection_parameters", {}).get("source_type", "-"),
            datum.get("created_at"),
            get_created_by(datum),
        ]
        table.add_row(*values)
    console.print(table)
