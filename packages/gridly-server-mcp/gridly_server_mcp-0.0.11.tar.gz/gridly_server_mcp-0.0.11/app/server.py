from app.mcpserver import mcp
import app.gridly

def main():
    print("Starting gridly-server-mcp")
    mcp.run(transport="stdio")

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")