from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from config import credential

def _get_default_subscription_id():
    """
    Resolve the default subscription from Azure CLI context.
    """
    sub_client = SubscriptionClient(credential)
    for sub in sub_client.subscriptions.list():
        if sub.state.lower() == "enabled":
            return sub.subscription_id
    raise RuntimeError("No enabled Azure subscription found")

def register(mcp):
    @mcp.tool(
        name="list_resources_in_rg",
        description="List all resources inside a resource group"
    )
    def list_resources(resource_group: str):
        client = ResourceManagementClient(credential, _get_default_subscription_id())
        return [
            {
                "name": r.name,
                "type": r.type,
                "location": r.location,
            }
            for r in client.resources.list_by_resource_group(resource_group)
        ]
