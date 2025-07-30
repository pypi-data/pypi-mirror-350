from .schema import CrudAction

def url_for_crud(model_name: str, action: str|CrudAction, entity_id=None, entity_id_key: str = "item_id") -> str:
    """
    Generate a CRUD URL based on your router's naming convention using a predefined map.

    The URL map:
      - 'crud_view':  '/plugin/crud_tools/{model_name}/view/{item_id}'
      - 'crud_new':   '/plugin/crud_tools/{model_name}/create'
      - 'crud_edit':  '/plugin/crud_tools/{model_name}/edit/{item_id}'
      - 'crud_delete':'/plugin/crud_tools/{model_name}/delete/{item_id}'

    The action parameter should be one of "VIEW", "CREATE", "EDIT", or "DELETE".
    For actions requiring an entity ID (all except CREATE), the entity_id must be provided.

    Args:
        model_name (str): The name of the model.
        action (str): The action (e.g., "VIEW", "CREATE", "EDIT", "DELETE").
        entity_id: The ID of the entity (required for actions other than CREATE).
        entity_id_key (str, optional): The parameter name for the entity ID in the route (default "item_id").

    Returns:
        A URL string built by formatting the corresponding route pattern.
    """
    # Mapping of route keys to URL patterns.
    from fastpluggy.fastpluggy import FastPluggy
    url_map = FastPluggy.get_global('crud_routes')

    action = CrudAction.from_any(action)

    # Get the corresponding route key.
    route_key = action.to_route_name()
    if route_key is None:
        raise ValueError(f"Unsupported action: {action}")

    # Retrieve the URL pattern.
    pattern = url_map[route_key]
    params = {'model_name': model_name}

    # For routes that include the entity ID, ensure it's provided.
    if '{item_id}' in pattern:
        if entity_id is None:
            raise ValueError(f"entity_id must be provided for action {action}")
        params[entity_id_key] = entity_id

    # Generate and return the URL by formatting the pattern.
    return pattern.format(**params)
