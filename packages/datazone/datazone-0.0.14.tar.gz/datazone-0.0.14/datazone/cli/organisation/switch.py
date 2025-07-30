from typing import Dict

import questionary
from rich import print

from datazone.core.connections.auth import AuthService
from datazone.service_callers.crud import CrudServiceCaller


def switch() -> None:
    response_data = CrudServiceCaller(entity_name="organisation").get_entity_list()

    if len(response_data) == 0:
        print("[bold orange]Error: No organisation found[/bold orange]")

    organisations = response_data.get("items")
    org_map: Dict[str, str] = {f"{org.get('name')} - {org.get('id')}": org.get("id") for org in organisations}

    _source_type = questionary.select("Select source type...", choices=org_map).unsafe_ask()

    org_id = org_map[_source_type]

    AuthService.login(organisation_id=org_id)
    print("[bold green]Switched to organisation successfully[/bold green]")
