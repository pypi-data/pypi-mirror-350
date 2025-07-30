from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller
from datazone.utils.helpers import get_created_by

extract_columns = [
    "ID",
    "Name",
    "Source ID",
    "Dataset ID",
    "Mode",
    "Deploy Status",
    "Created At",
    "Created By",
]


def list_func(page_size: int = 20):
    response_data = CrudServiceCaller(entity_name="extract").get_entity_list(
        params={"page_size": page_size},
    )

    console = Console()

    table = Table(*extract_columns)
    for datum in response_data.get("items"):
        values = [
            datum.get("id"),
            datum.get("name"),
            datum.get("source").get("id"),
            datum.get("dataset").get("id") if datum.get("dataset") else "-",
            datum.get("mode"),
            datum.get("deploy_status"),
            datum.get("created_at"),
            get_created_by(datum),
        ]
        table.add_row(*values)
    console.print(table)
