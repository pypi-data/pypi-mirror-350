# Gridly MCP Server

MCP Server for the GitLab API, enabling project management, file operations, and more.

## Tools

1. `list_projects`
    - To list projects of a company
    - Input: None

2. `retrieve_project`
   - Get project by id if succeeded. Otherwise, return an error.
   - Inputs:
    - `id` (string): Project ID

3. `list_database`
   - To list databases in a project.
   - Inputs:
     - `projectId` (string): Project ID
   - Returns: Project search results

4. `retrieve_database`
   - Get database by id 
   - Inputs:
     - `id` (string): database id
   - Returns: Created project details

5. `list_glossaries()`
    - List all glossaries.
    - Input: None
   
6. `list_translation_memories`
   - List all translation memories.
   - Input: None

7. `retrieve_translation_memory`
    - Return translation memory data by Id
    - Inputs:
        - `id` (string): tm id

8. `retrieve_glossary`
   - retrieve detail of a glossary by Id
   - Inputs:
     - `id` (str): The ID of the glossary.

9. `fetch_translation_memory`(request: SearchRequest, id: str)
   - Create a new merge request
   - Inputs:
        - `id` (str): Translation memory ID
        - `request` (object):
            - `lang` (str): Language code of the search text
            - `limit` (int, default=100): Max number of results
            - `offset` (int, default=0): Offset for pagination
            - `search` (str, default=""): Text to search
            - `mode` (str, default="default"): Search mode (default, regex, exact)
            - `fetchOption`:
                - `targetLangs` (List[str]): List of language codes to translate into

10. `suggest_translation_in_memory`
   - Suggest translation in memory
   - Inputs:
        - `projectId` (str): Project ID
        - `dbId` (str, default=""): Database ID
        - `gridId` (str, default=""): Grid ID
        - `sourceText` (str): Text stored in translation memory
        - `sourceLang` (str): Source language code
        - `targetLang` (str): Target language code

11. `search_glossary_terms`
   - Search glossary terms in paragraph
   - Inputs : 
        - `projectId` (str): Project ID
        - `databaseId` (str): Database ID
        - `sourceTermLang` (str): Language code of the source term (e.g., enUS)
        - `paragraph` (str): Text to search within

## Setup

### Api key
[Create a Gridly Api key follow instructions](https://help.gridly.com/360017915857-API-Key-Management) with appropriate permissions:
1. In your Gridly Dashboard, clicknext to your company name and select Company Settings. 
2. Select API Keys from the left-hand side menu to get to the API Keys page. 
3. Click Create API key.

### Usage with Claude Desktop (Recommended):
Follow instructions : https://modelcontextprotocol.io/quickstart/user
Add the following to your `claude_desktop_config.json`:

#### UVX

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "uvx",
      "args": [
        "gridly-server-mcp@0.0.11"
      ],
      "env": {
        "API_KEY": "<YOUR_TOKEN>",
        "ENV": "integration" // Optional, for self-hosted instances
      }
    }
  }
}
```

## Environment Variables

- `API_KEY`: Your Gridly Api Key (required)
- `ENV`: Base enviroment for Gridly API (optional, defaults to `integration`)