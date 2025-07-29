import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from mstrio.types import ExtendedType, ObjectSubTypes, ObjectTypes
from mstrio.utils.enum_helper import get_enum_val

from strqa.utils.types import SUPPORTED_TYPE_NAMES, SupportedTypes, is_supported_type

if TYPE_CHECKING:
    from strqa import Config


def create_json_baseline_file(
    objects: list[SupportedTypes], config: 'Config', filename: str
) -> None:
    """Create a JSON baseline file based on the given objects.
    The JSON file contains information about the environment,
    configuration, and the objects being compared.
    Args:
        objects (list[SupportedTypes]): List of objects to make up a baseline.
        config (Config): Configuration object for the comparison.
        filename (str): Path to the JSON file to be created.
    """

    if not is_supported_type(objects):
        msg = (
            "For baseline creation, objects must be a list of individual objects"
            f" of a supported type ({', '.join(SUPPORTED_TYPE_NAMES)})."
        )
        raise ValueError(msg)

    conn = objects[0].connection

    baseline_dict = {
        'environment': {
            'url': conn.base_url,
            'iserver_version': conn.iserver_version,
            'project_id': conn.project_id,
            'project_name': conn.project_name,
            'login_mode': conn.login_mode,
            'username': conn.username,
        },
        'config': asdict(config),
        'objects': [
            {
                'id': obj.id,
                'name': obj.name,
                'type': get_enum_val(obj.type, ObjectTypes),
                'subtype': get_enum_val(obj.subtype, ObjectSubTypes),
                'ext_type': get_enum_val(obj.ext_type, ExtendedType),
                'location': obj.location,
                'date_created': obj.date_created.isoformat(),
                'date_modified': obj.date_modified.isoformat(),
                'version': obj.version,
            }
            for obj in objects
        ],
    }

    with open(filename, 'w') as f:
        json.dump(baseline_dict, f, indent=4)
