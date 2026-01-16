from mcp.server.fastmcp import FastMCP

from tools import (
    subscriptions,
    resource_groups,
    create_rg,
    resources,
    delete_resource_group,
    storage
)

    

def create_mcp():
    mcp = FastMCP(name="azure-mcp-local")

    subscriptions.register(mcp)
    resource_groups.register(mcp)
    create_rg.register(mcp)
    resources.register(mcp)
    delete_resource_group.register(mcp)
    storage.register(mcp)

    return mcp


if __name__ == "__main__":
    mcp = create_mcp()
    mcp.run()   # STDIO MODE (Claude Desktop)
