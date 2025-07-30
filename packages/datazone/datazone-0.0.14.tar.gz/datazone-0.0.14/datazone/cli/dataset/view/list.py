from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller
from datazone.utils.helpers import get_created_by

transaction_columns = [
    "ID",
    "Name",
    "Dataset ID",
    "Created At",
    "Created By",
]


def list_func(dataset_id: str, page_size: int = 20):
    response_data = CrudServiceCaller(entity_name="transaction").get_entity_list(
        params={"filters": f"[dataset.$id][$eq]:{dataset_id}", "page_size": page_size},
    )

    console = Console()

    table = Table(*transaction_columns)
    for datum in response_data.get("items"):
        values = [
            datum.get("id"),
            datum.get("name"),
            datum.get("dataset").get("id"),
            datum.get("created_at"),
            get_created_by(datum),
        ]
        table.add_row(*values)
    console.print(table)
