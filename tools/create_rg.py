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
        name="create_resource_group",
        description=(
            "Create an Azure Resource Group. "
            "⚠️ WRITE operation. "
            "Azure location is mandatory and must be explicitly provided. "
            "This action requires explicit user confirmation before execution."
        )
    )
    def create_resource_group(
        name: str,
        location: str,          # 🔴 REQUIRED → Claude must ask if missing
        confirm: bool = False   # 🔴 REQUIRED → Claude must confirm
    ):
        # Step 1 — Confirmation gate
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": (
                    f"Please confirm creation of the Azure resource group "
                    f"'{name}' in region '{location}'."
                ),
            }

        credential = DefaultAzureCredential()
        subscription_id = _get_default_subscription_id(credential)

        client = ResourceManagementClient(
            credential,
            subscription_id
        )

        rg = client.resource_groups.create_or_update(
            name,
            {"location": location}
        )

        return {
            "status": "created",
            "name": rg.name,
            "location": rg.location,
            "id": rg.id,
        }
