from pydantic import BaseModel

class ContentRequest(BaseModel):
    content: str
    role: str

class ContentResponse(BaseModel):
    filtered_content: str
