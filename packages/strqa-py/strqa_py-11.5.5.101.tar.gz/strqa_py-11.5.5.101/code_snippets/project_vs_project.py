"""This is a demo script that demonstrates how to compare objects between
Strategy projects using StrQA.
It shows how to set up connections to source and target environments, configure
comparison settings, and perform both automatic and manual object mapping for
comparison between project objects.
"""

from mstrio.connection import Connection
from mstrio.project_objects import OlapCube
from strqa import Config, StrQA

# Define connection information for source Strategy environment
source_url = '<source_url>'
source_username = '<source_username>'
source_password = '<source_password>'
source_project_name = '<source_project_name>'

# Define connection information for target Strategy environment
target_url = '<target_url>'
target_username = '<target_username>'
target_password = '<target_password>'
target_project_name = '<target_project_name>'

# Create a connection to the source Strategy environment
source_conn = Connection(
    base_url=source_url,
    username=source_username,
    password=source_password,
    project_name=source_project_name,
)

# Create a connection to the target Strategy environment
target_conn = Connection(
    base_url=target_url,
    username=target_username,
    password=target_password,
    project_name=target_project_name,
)

# Configure how the comparison should be performed
config = Config(
    cube_config=Config.CubeConfig(
        sql=True,  # Include SQL in the comparison
        sql_case_sensitive=True,  # SQL comparison should be case-sensitive
    ),
    map_objects_by_id=True,  # Match objects using their IDs
    map_objects_by_location=True,  # Match objects using their location
    map_objects_manually=False,  # Don't require manual mapping of objects
    create_matching_sql_file=False,  # Don't create SQL files for comparison
)

# Define the list of objects to compare
# These objects will be searched for in the target environment
source_cube_1 = OlapCube(source_conn, id='<source_cube_id_1>')
source_cube_2 = OlapCube(source_conn, id='<source_cube_id_2>')

objects = [source_cube_1, source_cube_2]

# Create a StrQA object to perform the comparison
strqa = StrQA(
    objects=objects,  # Objects to compare
    config=config,  # Configuration for comparison
    path='',  # Path where to store results (empty means current directory)
)

# Run the comparison between the projects
# This will find matching objects in the target environment and compare them
# Results will be stored in a newly created folder with date/time as name
result = strqa.project_vs_project(target_connection=target_conn)
print(result)


# Configure with case-insensitive SQL comparison and manual mapping
config = Config(
    cube_config=Config.CubeConfig(
        sql=True,  # Include SQL in the comparison
        sql_case_sensitive=False,  # Case-insensitive SQL comparison
    ),
    map_objects_manually=True,  # We'll provide explicit source-target mappings
    create_matching_sql_file=True,  # Create SQL files for comparison
)

# Get source objects
source_cube_1 = OlapCube(source_conn, id='<source_cube_id_1>')
source_cube_2 = OlapCube(source_conn, id='<source_cube_id_2>')

# Get target objects
target_cube_1 = OlapCube(target_conn, id='<target_cube_id_1>')
target_cube_2 = OlapCube(target_conn, id='<target_cube_id_2>')

# Create a list of tuples for manual object mapping
# Each tuple contains (source_object, target_object)
objects = [
    (source_cube_1, target_cube_1),  # Compare the first pair of cubes
    (source_cube_2, target_cube_2),  # Compare the second pair of cubes
]

# Initialize StrQA with the manual object mappings
strqa = StrQA(
    objects=objects,  # List of tuples for manual mapping
    config=config,
    path='',  # Results will be stored in this folder
)

# Run the comparison
result = strqa.project_vs_project(target_connection=target_conn)
print(result)
