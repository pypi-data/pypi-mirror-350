from mstrio.project_objects import OlapCube, SuperCube

# Union type for all object types supported by StrQA in general.
SupportedTypes = OlapCube | SuperCube

SUPPORTED_TYPE_NAMES = ["OlapCube", "SuperCube"]


def is_supported_type(obj: SupportedTypes | list[SupportedTypes]) -> bool:
    """Check if the objects are of a type supported by StrQA.

    Args:
        obj (SupportedTypes | list[SupportedTypes]):
            Object or list of objects to check.

    Returns:
        bool: True if the objects are of a supported type, False otherwise
    """
    obj_list = obj if isinstance(obj, list) else [obj]
    return all(isinstance(item, (OlapCube, SuperCube)) for item in obj_list)


# Union type for all object types supported by StrQA cube comparison.
SupportedCubes = OlapCube | SuperCube
