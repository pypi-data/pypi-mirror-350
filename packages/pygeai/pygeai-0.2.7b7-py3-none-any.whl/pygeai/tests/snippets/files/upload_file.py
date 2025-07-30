from pygeai.core.models import Organization, Project
from pygeai.core.files.managers import FileManager
from pygeai.core.files.models import UploadFile

organization = Organization(id="4aa15b61-d3c7-4a5c-99b8-052d18a04ff2")
project = Project(id="1956c032-3c66-4435-acb8-6a06e52f819f")

file = UploadFile(
    path="test.txt",
    name="TestyFile",
    folder="TestyTestTemp"
)

file_manager = FileManager(organization_id=organization.id, project_id=project.id)

response = file_manager.upload_file(file)
print(response)
