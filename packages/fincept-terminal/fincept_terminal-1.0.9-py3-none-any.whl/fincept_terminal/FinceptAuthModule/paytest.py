import requests

# Base URL (your API is exposed via Zrok)
BASE_URL = "https://finceptapi.share.zrok.io"

# Existing user's API key
API_KEY = "1b9fc78f-a46c-4f2b-a310-ebc88e7d8b5a"

# Headers for authentication
HEADERS = {"X-API-Key": API_KEY}


def fetch_user_details():
    """Fetch user details using the existing API key."""
    url = f"{BASE_URL}/user-details"
    params = {"username": "tilakisbest"}  # Replace with actual username
    response = requests.get(url, headers=HEADERS, params=params)
    print("User Details Response:", response.json())


def regenerate_api_key():
    """Regenerate API key for the user."""
    url = f"{BASE_URL}/regenerate-api-key"
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        new_api_key = response.json().get("new_api_key")
        print("✅ New API Key Generated:", new_api_key)
        return new_api_key
    else:
        print("❌ API Key Regeneration Failed:", response.json())
        return None


def verify_new_api_key(new_api_key):
    """Verify the newly generated API key."""
    if not new_api_key:
        print("❌ No new API key available for verification.")
        return

    headers = {"X-API-Key": new_api_key}
    url = f"{BASE_URL}/user-details"
    params = {"username": "tilakisbest"}  # Replace with actual username
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ New API Key is working correctly!")
    else:
        print("❌ New API Key verification failed:", response.json())


if __name__ == "__main__":
    print("🔹 Fetching User Details...")
    fetch_user_details()

    print("\n🔹 Regenerating API Key...")
    new_api_key = regenerate_api_key()

    print("\n🔹 Verifying New API Key...")
    verify_new_api_key(new_api_key)




