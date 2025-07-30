import os
import uuid
import re
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Lyzr Single Tool")


# Sanitize tool name
def sanitize_agent_name(agent_name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "", agent_name)[:64]


# Load environment variables
api_key = os.getenv("LYZR_API_KEY")
user_id = os.getenv("LYZR_USER_ID")

if not api_key or not user_id:
    raise ValueError("Missing required env vars: LYZR_API_KEY, LYZR_USER_ID")


def get_agent_config():
    url = "https://agent-prod.studio.lyzr.ai/v3/agents/"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    with httpx.Client() as client:
        response = client.get(url, headers=headers)
    print("Agents fetched")
    return response.json()


# Tool function for Lyzr agent message sending
def send_agent_message(message: str, agent_id: str) -> dict:
    session_id = f"{agent_id}-{str(uuid.uuid4())[:8]}"
    url = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    payload = {
        "user_id": user_id,
        "agent_id": agent_id,
        "session_id": session_id,
        "message": message,
    }

    with httpx.Client() as client:
        try:
            response = client.post(url, headers=headers, json=payload, timeout=30.0)
            if response.status_code == 200:
                print("Message sent")
                return response.json()
            else:
                print(f"API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code} - {response.text}"}
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return {"error": str(e)}


def create_agent_tool(agent_name: str, agent_id: str, agent_description: str):
    @mcp.tool(
        name=f"call_agent_{agent_name}",
        description=f"{agent_description}",
    )
    def agent_tool(message: str) -> str:
        """Auto-generated tool for calling an agent"""
        return send_agent_message(message, agent_id)

    return agent_tool


def main():
    agent_config = get_agent_config()

    for agent in agent_config:
        tool_name = sanitize_agent_name(agent["name"])
        tool_description = agent.get("description", "Tool to interact with Lyzr agent")
        agent_id = agent.get("_id")

        create_agent_tool(tool_name, agent_id, tool_description)
    print("Tools created")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
