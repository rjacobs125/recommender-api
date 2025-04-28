import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")

)

def get_ai_recommendations(job_title: str, job_responsibility: str, workflows: list):
    workflows_text = ", ".join(workflows)

    messages = [
        {
            "role": "system",
            "content": "You are an expert AI tools recommendation system."
        },
        {
            "role": "user",
            "content": f"""Given:
            - Job Title: {job_title}
            - Job Responsibilities: {job_responsibility}
            - Workflows to Automate: {workflows_text}

            For each workflow, recommend exactly 5 different AI tools that can help automate that workflow.

            Respond in structured JSON format grouped by workflow name.
            """ 
        }
    ]


    tools = [
    {
        "type": "function",
        "function": {
            "name": "recommend_ai_tools",
            "description": "For each workflow, recommend 5 AI tools that help automate it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recommendations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "workflow": {"type": "string"},
                                "tools": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "tool_name": {"type": "string"},
                                            "website_link": {"type": "string"},
                                            "features": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "youtube_tutorials": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "x_handles": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        },
                                        "required": ["tool_name", "website_link", "features", "youtube_tutorials", "x_handles"]
                                    }
                                }
                            },
                            "required": ["workflow", "tools"]
                        }
                    }
                },
                "required": ["recommendations"]
                }
            }
        }
    ]


    response = client.chat.completions.create(
        model="gpt-4.1",  #"gpt-4-1106-preview",  # Or "gpt-3.5-turbo-1106"
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "recommend_ai_tools"}},
        temperature=0.2
    )

    # Extract structured output
    function_args = response.choices[0].message.tool_calls[0].function.arguments
    parsed = json.loads(function_args)

    return parsed
