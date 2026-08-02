import msal
import requests

from config import AZURE_CONFIG
from services.token_service import get_refresh_token

AUTHORITY = f"https://login.microsoftonline.com/{AZURE_CONFIG['tenant_id']}"

SCOPES = [
    "Files.ReadWrite",
    "User.Read"
]

def get_access_token():

    refresh_token = get_refresh_token()

    app = msal.PublicClientApplication(
        AZURE_CONFIG["client_id"],
        authority=AUTHORITY
    )

    result = app.acquire_token_by_refresh_token(
        refresh_token,
        scopes=SCOPES
    )

    if "access_token" not in result:
        raise Exception(result)

    return result["access_token"]
def upload_file(file_bytes, filename):

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }

    url = (
        "https://graph.microsoft.com/v1.0"
        f"/me/drive/root:/BarrieCoffee/{filename}:/content"
    )

    response = requests.put(
        url,
        headers=headers,
        data=file_bytes
    )

    response.raise_for_status()

    return response.json()