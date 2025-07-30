from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller
from datazone.service_callers.datazone import DatazoneServiceCaller

organisation_columns = ["ID", "Name", "DB Name", "Current", "Created At"]


def list_func(page_size: int = 20):
    response_data = CrudServiceCaller(entity_name="organisation").get_entity_list(
        params={"page_size": page_size},
    )

    current_organisation = DatazoneServiceCaller.get_current_organisation()
    current_organisation_id = current_organisation.get("id")

    console = Console()

    table = Table(*organisation_columns)
    items = response_data.get("items")
    if len(items) == 0:
        console.print("[bold orange]Not created any dataset yet[/bold orange]")
        return

    for datum in items:
        values = [
            datum.get("id"),
            datum.get("name"),
            datum.get("sql_db_name"),
            "Yes" if datum.get("id") == current_organisation_id else "No",
            datum.get("created_at"),
        ]
        table.add_row(*values)
    console.print(table)
