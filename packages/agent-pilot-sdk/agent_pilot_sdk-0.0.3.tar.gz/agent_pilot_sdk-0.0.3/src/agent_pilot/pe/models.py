from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from agent_pilot.models import EventStreamChunk, TaskType


class GeneratePromptStreamRequest(BaseModel):
    """Request model for prompt generation."""

    rule: str = Field(..., alias='Rule')
    temperature: float = Field(1.0, alias='Temperature')
    top_p: float = Field(0.7, alias='TopP')
    model_name: Optional[str] = Field(None, alias='ModelName')
    feedback: Optional[str] = Field(None, alias='Feedback')
    current_prompt: Optional[str] = Field(None, alias='CurrentPrompt')
    task_type: Union[TaskType, str] = Field(TaskType.DEFAULT, alias='TaskType')
    request_id: Optional[str] = Field(None, alias='RequestId')

    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())


class GeneratePromptChunk(BaseModel):
    content: str
    usage: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class GeneratePromptStreamResponseChunk(EventStreamChunk[GeneratePromptChunk]):
    pass
