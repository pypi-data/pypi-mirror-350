from rich import print

from datazone.service_callers.crud import CrudServiceCaller


def delete(view_id: str):
    CrudServiceCaller(entity_name="view").delete_entity(entity_id=view_id)

    print("View has deleted successfully :fire:")
