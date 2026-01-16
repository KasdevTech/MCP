from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import SubscriptionClient
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
    # -------------------------------
    # LIST STORAGE ACCOUNTS
    # -------------------------------
    @mcp.tool(
        name="list_storage_accounts",
        description="List Azure storage accounts"
    )
    def list_storage_accounts():
        client = StorageManagementClient(
            credential,
            _get_default_subscription_id()
        )

        return [
            {
                "name": s.name,
                "location": s.location,
                "sku": s.sku.name,
                "kind": s.kind,
            }
            for s in client.storage_accounts.list()
        ]

    # -------------------------------
    # CREATE STORAGE ACCOUNT
    # -------------------------------
    @mcp.tool(
        name="create_storage_account",
        description=(
            "Create an Azure Storage Account. "
            "⚠️ WRITE operation. "
            "Requires explicit user confirmation."
        )
    )
    def create_storage_account(
        name: str,
        resource_group: str,
        location: str,
        sku: str = "Standard_LRS",
        kind: str = "StorageV2",
        confirm: bool = False
    ):
        # 🔐 Confirmation gate
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": (
                    f"Please confirm creation of storage account '{name}' "
                    f"in resource group '{resource_group}' "
                    f"at location '{location}' "
                    f"with SKU '{sku}'."
                ),
            }

        client = StorageManagementClient(
            credential,
            _get_default_subscription_id()
        )

        poller = client.storage_accounts.begin_create(
            resource_group_name=resource_group,
            account_name=name,
            parameters={
                "location": location,
                "sku": {"name": sku},
                "kind": kind,
                "enable_https_traffic_only": True,
                "minimum_tls_version": "TLS1_2",
            },
        )

        account = poller.result()

        return {
            "status": "created",
            "name": account.name,
            "location": account.location,
            "sku": account.sku.name,
            "kind": account.kind,
            "id": account.id,
        }
