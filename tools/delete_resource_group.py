from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient


def _get_default_subscription_id(credential):
    sub_client = SubscriptionClient(credential)
    for sub in sub_client.subscriptions.list():
        if sub.state.lower() == "enabled":
            return sub.subscription_id
    raise RuntimeError("No enabled Azure subscription found")


def register(mcp):
    @mcp.tool(
        name="delete_resource_group",
        description=(
            "Delete an Azure Resource Group and ALL resources inside it. "
            " DESTRUCTIVE operation. "
            "This action is irreversible and requires explicit user confirmation."
        )
    )
    def delete_resource_group(
        name: str,
        confirm: bool = False
    ):
        #  Confirmation gate
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": (
                    f"Please confirm deletion of the Azure resource group "
                    f"'{name}'. This will permanently delete all resources."
                ),
            }

        credential = DefaultAzureCredential()
        subscription_id = _get_default_subscription_id(credential)

        client = ResourceManagementClient(
            credential,
            subscription_id
        )

        # Azure RG deletion is async
        poller = client.resource_groups.begin_delete(name)
        poller.wait()

        return {
            "status": "deleted",
            "name": name,
        }
