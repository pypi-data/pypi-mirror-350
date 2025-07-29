from pydantic.main import BaseModel

from pygeai.core.models import Assistant, Project, ProjectToken, \
    RequestItem


class AssistantListResponse(BaseModel):
    assistants: list[Assistant]


class ProjectListResponse(BaseModel):
    projects: list[Project]


class ProjectDataResponse(BaseModel):
    project: Project


class ProjectTokensResponse(BaseModel):
    tokens: list[ProjectToken]


class ProjectItemListResponse(BaseModel):
    items: list[RequestItem]
