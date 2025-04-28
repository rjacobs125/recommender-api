from pydantic import BaseModel
from typing import List, Optional

class Tool(BaseModel):
    tool_name: str
    website_link: Optional[str]
    features: List[str]
    youtube_tutorials: List[str]
    x_handles: List[str]

class WorkflowRecommendation(BaseModel):
    workflow: str
    tools: List[Tool]

class RecommendRequest(BaseModel):
    job_title: str
    job_responsibility: str
    workflows_to_automate: List[str]

class RecommendResponse(BaseModel):
    recommendations: List[WorkflowRecommendation]
