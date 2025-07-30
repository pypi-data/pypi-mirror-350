from pydantic import BaseModel, Field
from typing import List, Optional

class MCPRequest(BaseModel):
    """Sample MCPRequest model."""
    message: str = Field(..., description="The message content")
    context: Optional[List[str]] = Field(default=None, description="Optional context for the request")

class MCPResponse(BaseModel):
    """Sample MCPResponse model."""
    response: str = Field(..., description="The response content")
    status: str = Field(default="success", description="Status of the response")
