import requests
import sys
import os
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional
from app.mcpserver import mcp

def getURL() -> str:
    return "https://eu-central-1.api.gridly.com" if os.getenv("ENV", "production") == "production" else "https://ap-southeast-1.gateway.integration.gridly.com"

@mcp.tool()
def list_projects() -> int:
    """To list projects of a company."""
    API_KEY = os.getenv("API_KEY", "")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + "/organization/v1/projects", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def retrieve_project(id: str) -> int:
    """Get project by id if succeeded. Otherwise, return an error."""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + f"/organization/v1/project/{id}", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def list_database(projectId: str = "") -> int:
    """To list databases of a project."""
    API_KEY = os.getenv("API_KEY", "")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + "/gridly/api/v1/databases?projectId={projectId}", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def retrieve_database(id: str) -> int:
    """Get database by id if succeeded. Otherwise, return an error."""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + f"/gridly/api/v1/databases/{id}", headers=headers)
    response.raise_for_status()
    return response.json()