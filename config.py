from azure.identity import AzureCliCredential
import subprocess

# Credential (local dev with MFA)
credential = AzureCliCredential()

def get_subscription_id():
    result = subprocess.run(
        ["az", "account", "show", "--query", "id", "-o", "tsv"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError("Azure CLI not logged in or no subscription access")
    return result.stdout.strip()

SUBSCRIPTION_ID = get_subscription_id()
