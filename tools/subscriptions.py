from azure.mgmt.resource import SubscriptionClient
from config import credential

def register(mcp):
    @mcp.tool(
        name="list_azure_subscriptions",
        description="List Azure subscriptions"
    )
    def list_subscriptions():
        client = SubscriptionClient(credential)
        return [
            {
                "id": s.subscription_id,
                "name": s.display_name,
                "state": s.state,
            }
            for s in client.subscriptions.list()
        ]
