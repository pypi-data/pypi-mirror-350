from .mcp_server import mcp

def main():
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp") 