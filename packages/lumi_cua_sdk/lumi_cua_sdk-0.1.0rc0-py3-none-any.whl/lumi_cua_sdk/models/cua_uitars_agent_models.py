from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    """Request model for agent runnint a task prompt"""
    query: str = Field("", description="task prompt")
    sandbox_id: str = Field("0", description="sandbox id")
    sandbox_endpoint: str = Field("0", description="sandbox tool server endpoint")


class AgentStreamMessage(BaseModel):
    """Represents a single message/event streamed from the agent's run method."""
    summary: Optional[str] = Field("", description="A summary of the current step or observation.")
    action: Optional[str] = Field("", description="The specific action taken or proposed by the agent.")
    screenshot: Optional[str] = Field(None, description="A base64 encoded screenshot relevant to the current step, if available.")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of when this event was created.")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp of when this event was last updated.")


class AgentStreamResponse(BaseModel):
    data: AgentStreamMessage = Field(None, description="The response from the agent.")
