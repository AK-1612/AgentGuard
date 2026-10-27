from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Literal

class ToolExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    
    tool_name: str = Field(..., description="Target tool name")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Parsed arguments")
    raw_prompt: Optional[str] = Field(None, description="Original user prompt")

class SecurityEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    
    status: Literal["ALLOW", "BLOCK"]
    error_code: Optional[str] = None
    reason: Optional[str] = None