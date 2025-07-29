from pygeai.lab.managers import AILabManager
from pygeai.lab.models import FilterSettings
from pygeai.core.base.responses import ErrorListResponse

manager = AILabManager()

project_id = "2ca6883f-6778-40bb-bcc1-85451fb11107"

response = manager.list_jobs(
    project_id=project_id,
    filter_settings=FilterSettings(start="0", count="100"),
    topic=None,
    token=None
)

if isinstance(response, ErrorListResponse):
    print("Error retrieving jobs:")
    for error in response:
        print(f"- {error}")
else:
    jobs = response
    print("Jobs retrieved successfully:")
    for job in jobs:
        print(f"- Job: {job.name}, Token: {job.token}, Topic: {job.topic}, Caption: {job.caption}")
        if job.parameters:
            print("  Parameters:")
            for param in job.parameters:
                print(f"    - {param.Name}: {param.Value}")
        if job.info:
            print(f"  Info: {job.info}")