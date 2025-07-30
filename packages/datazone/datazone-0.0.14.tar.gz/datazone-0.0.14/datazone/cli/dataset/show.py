from typing import Optional

from rich.console import Console
from rich.table import Table
from rich import print

from datazone.service_callers.datazone import DatazoneServiceCaller


def show(
    dataset_id: str,
    size: int = 10,
    transaction_id: Optional[str] = None,
) -> None:
    """
    Show dataset sample data. It fetches sample data from dataset service and prints out as rich table
    Args:
        dataset_id (str): dataset id
        size (int): table size
        transaction_id (Optional[str]): specific transaction id
    """
    response_data = DatazoneServiceCaller.get_sample_data(dataset_id=dataset_id, transaction_id=transaction_id)

    if len(response_data) == 0:
        print("[bold orange]No data[/bold orange]")

    data = response_data[:size]
    columns = data[0].keys()

    console = Console()

    table = Table(*columns)
    for datum in data:
        values = [str(value) for value in datum.values()]
        table.add_row(*values)
    console.print(table)
