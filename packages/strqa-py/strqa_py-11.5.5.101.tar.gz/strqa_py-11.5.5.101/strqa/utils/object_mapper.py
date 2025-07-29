from typing import TYPE_CHECKING

from mstrio.connection import Connection
from mstrio.helpers import IServerError
from mstrio.object_management import Folder

if TYPE_CHECKING:
    from strqa import Config, SupportedTypes


def _try_to_get_folder(target_conn: Connection, obj_path: str) -> Folder | None:
    """Try to get a folder by path in the target connection.

    Attempts to locate a folder in the target environment by converting
    the source path to use the target project name.

    Args:
        target_conn (Connection): Target Strategy connection
        obj_path (str): Original object path including project name

    Returns:
        Folder object if found, None otherwise
    """
    # Extract project name from a path
    project_name = obj_path.split("/")[1]
    # Replace source project name with target project name in the path
    new_path = obj_path.replace(project_name, target_conn.project_name)
    try:
        return Folder(target_conn, path=new_path)
    except (ValueError, IServerError):
        # Return None if the folder doesn't exist or other server error occurs
        return None


def _try_to_init_obj_by_id(
    obj: 'SupportedTypes', target_conn: Connection, obj_type: type['SupportedTypes']
) -> 'SupportedTypes | None':
    """Try to initialize an object in the target environment by ID.

    Attempts to find and initialize the corresponding object in the target
    connection using the source object's ID.

    Args:
        obj (SupportedTypes): Source object to find a match for
        target_conn (Connection): Target Strategy connection
        obj_type (type[SupportedTypes]): Type of the object (class)
            to initialize

    Returns:
        Initialized object in target connection if found, None otherwise
    """
    try:
        return obj_type(target_conn, id=obj.id)
    except IServerError:
        # Return None if an object doesn't exist in target environment
        return None


def _try_to_init_target_obj(
    obj: 'SupportedTypes', target_conn: Connection, config: 'Config'
) -> 'SupportedTypes | None':
    """Try to initialize the target object by ID or location.

    Attempts to find a matching object in the target connection using
    strategies defined in the configuration. First try to match by ID
    if enabled, then by location if enabled.

    Args:
        obj (SupportedTypes): Source object to find a match for
        target_conn (Connection): Target connection to search in
        config (Config): Configuration controlling search strategies

    Returns:
        Matching object in target connection or None if no match found
    """
    obj_type: type[SupportedTypes] = type(obj)

    # Try to match by ID if enabled in config
    if config.map_objects_by_id:
        target_obj = _try_to_init_obj_by_id(obj, target_conn, obj_type)
        if target_obj:
            return target_obj

    # Try to match by location and name if enabled in config
    if config.map_objects_by_location:
        # Get the parent folder path (everything except the object name)
        obj_path = obj.location.rsplit('/', 1)[0]
        # Try to get the corresponding folder in the target environment
        folder = _try_to_get_folder(target_conn, obj_path)
        if not folder:
            return None

        # Search for an object with matching name in the folder contents
        for folder_obj in folder.get_contents():
            if obj.name == folder_obj.name:
                return folder_obj

    return None


def map_objects(
    objects: list['SupportedTypes'], target_conn: Connection, config: 'Config'
) -> list[tuple['SupportedTypes', 'SupportedTypes | None']]:
    """Map objects from source to target connection.

    For each object in the source list, attempts to find a matching object
    in the target environment using the configured mapping strategies.
    Returns a list of tuples containing (source_object, target_object) pairs.

    Args:
        objects (list[SupportedTypes]): List of source objects to map
        target_conn (Connection): Target Strategy connection
        config (Config): Configuration controlling mapping behavior

    Returns:
        List of tuples with source objects and their matching target objects
        (or None if no match found)
    """
    return [(obj, _try_to_init_target_obj(obj, target_conn, config)) for obj in objects]
