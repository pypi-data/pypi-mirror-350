from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from mcp_jenkins.models.build import Build


class JobBase(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    class_: str = Field(..., alias='_class')
    name: str
    url: str
    fullname: str = Field(None, alias='fullName')


class Job(JobBase):
    color: str

    buildable: bool = None
    builds: list['Build'] = None
    lastBuild: Optional['Build'] = None
    nextBuildNumber: int = None
    inQueue: bool = None


class Folder(JobBase):
    jobs: list[Union['Job', 'Folder']]
