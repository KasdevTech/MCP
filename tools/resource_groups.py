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
        name="list_resource_groups",
        description="List all Azure resource groups in the current subscription"
    )
    def list_resource_groups():
        subscription_id = _get_default_subscription_id()

        client = ResourceManagementClient(
            credential,
            subscription_id
        )

        return [
            {
                "name": rg.name,
                "location": rg.location,
                "provisioning_state": rg.properties.provisioning_state,
            }
            for rg in client.resource_groups.list()
        ]
