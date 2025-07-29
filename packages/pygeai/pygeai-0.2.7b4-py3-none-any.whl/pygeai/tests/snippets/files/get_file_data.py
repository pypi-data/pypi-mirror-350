from pygeai.core.models import Organization, Project
from pygeai.core.files.managers import FileManager
from pygeai.core.files.models import File

organization = Organization(id="4aa15b61-d3c7-4a5c-99b8-052d18a04ff2")
project = Project(id="1956c032-3c66-4435-acb8-6a06e52f819f")
file = File(id="9984b837-fe88-4014-ad14-91e1596c8ead")

file_manager = FileManager(organization_id=organization.id, project_id=project.id)

response = file_manager.get_file_data(file_id=file.id)
print(response)
