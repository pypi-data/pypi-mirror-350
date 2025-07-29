from mcp.server.fastmcp import FastMCP
import requests
import sys
import os
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

# Create an MCP server instance
mcp = FastMCP("SimpleMCPDemo", dependencies=["mcp[cli]"])

class Glossary(BaseModel):
    id: str = Field(..., description="The id of specific glossary")

class FetchOption:
    targetLangs: List[str] = Field(..., description="languageCode of text need to search, example: enUS, arSA, caES")

class Lang(Enum):
    enUS = (False, "English (United States)")
    arSA = (True, "Arabic")
    caES = (False, "Catalan")

class Mode(str, Enum):
    DEFAULT = "default"
    REGEX = "regex"
    EXACT = "exact"

@dataclass
class GlossarySuggestion(BaseModel):
    projectId: str = Field(..., description="id of project")
    databaseId: str = Field(..., description="id of database")
    sourceTermLang: str = Field(..., description="languageCode of source Text, example: enUS, arSA, caES")
    paragraph: str = Field(..., description="source Text need to get glossary") 

@dataclass
class FetchOption:
    targetLangs: List[str]

@dataclass
class SearchRequest(BaseModel):
    lang: str = Field(..., description="languageCode of search Text, example: enUS, arSA, caES")
    limit: int = Field(default = 100 , description="limit to fetch, defaul is 10")
    offset: int = Field(default = 0 , description="offset to fetch, defaul is 0")
    search: str = Field(default = "", desscsription="Text to search, defaul is empty")
    mode: Mode = Field(default= Mode.DEFAULT, description="Has 3 value, default or regex or exact")
    fetchOption: FetchOption

class SuggestionRequest(BaseModel):
    projectId: str = Field(..., description="id of project")
    dbId: str = Field(default ="", description="id of database")
    gridId: str = Field(default ="", description="id of grid")
    sourceText: str = Field(..., description="source of text is store in translation memory")
    sourceLang: str = Field(..., description="languageCode of source Text, example: enUS, arSA, caES")
    targetLang: str = Field(..., description="languageCode of target Text need to query in translation memory, example: enUS, arSA, caES")

def getURL() -> str:
    return "https://eu-central-1.api.gridly.com" if os.getenv("ENV", "production") == "production" else "https://gateway.integration.gridly.com"

# Define a dynamic resource for a personalized greeting
@mcp.tool()
def list_glossaries() -> int:
    """To list glossary of a company."""
    API_KEY = os.getenv("API_KEY", "")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + "/lqa/v1/glossaries", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def retrieve_glossary(id: str) -> int:
    """Return glossary data in object if succeeded. Otherwise, return an error."""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + "/lqa/v1/glossaries/" + id, headers=headers)
    response.raise_for_status()
    return response.json()

# Define a dynamic resource for a personalized greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a personalized greeting for the given name."""
    return f"Hello, {name}! Welcome to the MCP Demo Server."

@mcp.tool()
def list_translation_memories() -> int:
    """To list translation memories of a company."""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + "/lqa/v1/transmems", headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def retrieve_translation_memory(id: str) -> int:
    """Return translation memory data if succeeded. Otherwise, return an error."""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(getURL() + "/lqa/v1/transmems/" + id, headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def fetch_translation_memory(request: SearchRequest, id: str) -> int:
    """Fetch translation memory data in object By source Text , sourceLangague and targetLanguage. Otherwise, return an error."""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.post(getURL() + f"/lqa/api/v1/transmems/{id}/fetch", json=request.dict(), headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def suggest_translation_in_memory(request: SuggestionRequest) -> int:
    """Suggest translation in memory"""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.post(getURL() + "/lqa/api/v1/transmems/suggestions", json=request.dict(), headers=headers)
    response.raise_for_status()
    return response.json()

@mcp.tool()
def search_glossary_terms(request: GlossarySuggestion) -> int:
    """Search glossary terms in paragraph"""
    API_KEY = os.getenv("API_KEY")
    headers = {
        "Authorization": f"ApiKey " + API_KEY,
        "Accept": "application/json",
    }
    response = requests.post(getURL() + "/lqa/api/v1/terms/searchInParagraph", json=request.dict(), headers=headers)
    response.raise_for_status()
    return response.json()