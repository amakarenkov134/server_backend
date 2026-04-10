from pydantic import BaseModel, Field

#Requests

class ServiceRequest(BaseModel):
    service_name: str = Field(min_length=2, max_length=20)

class ServiceRequestLogs(BaseModel):
    service_name: str = Field(min_length=2, max_length=20)
    lines: int = Field(ge = 1, le = 200)

#Responses

class CommandResponse(BaseModel):
    service_name: str
    stdout: str
    stderr: str
    returncode: int
