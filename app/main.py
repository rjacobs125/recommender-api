from fastapi import FastAPI, HTTPException, Query
from app.schemas import RecommendRequest, RecommendResponse, WorkflowRecommendation, Tool
from app.openai_chain import get_ai_recommendations
from app.search_utils import search_youtube_tutorials
from fastapi.middleware.cors import CORSMiddleware
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.post("/recommend", response_model=RecommendResponse)
async def recommend_tools(request: RecommendRequest, yt: int = Query(1, description="Set to 0 to disable YouTube API calls, set to 1 to enable them")):
    try:
        parsed = get_ai_recommendations(
            request.job_title,
            request.job_responsibility,
            request.workflows_to_automate
        )

        real_results = []

        for workflow_group in parsed.get("recommendations", []):
            workflow_name = workflow_group.get("workflow")
            tools_list = workflow_group.get("tools", [])

            real_tools = []
            for tool in tools_list:
                tool_name = tool["tool_name"]

                #real_tutorials = search_youtube_tutorials(tool_name)

 # Only make YouTube API call if yt=1
                real_tutorials = None
                if yt == 1:
                    logger.info(f"Making YouTube API call for tool: {tool_name}")
                    real_tutorials = search_youtube_tutorials(tool_name)
                    
                real_tool = Tool(
                    tool_name=tool_name,
                    website_link=tool.get("website_link"),
                    features=tool.get("features", []),
                    youtube_tutorials=real_tutorials if real_tutorials is not None else tool.get("youtube_tutorials", []),
                    x_handles=tool.get("x_handles", [])
                )

                real_tools.append(real_tool)

            real_results.append(WorkflowRecommendation(
                workflow=workflow_name,
                tools=real_tools
            ))

        return RecommendResponse(recommendations=real_results)

    except Exception as e:
        logger.error(f"Error occurred in /recommend endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
