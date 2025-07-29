

# import requests
#
# BASE_URL = "https://finceptapi.share.zrok.io"
# USERNAME = "tilakisbest"
# API_KEY = "059951aa-cc88-4bfb-ba3c-33e38343a48b"  # Ensure this is valid!
#
# HEADERS = {"X-API-Key": API_KEY}  # ✅ Ensure API Key is always included!
#
# def generate_api_key():
#     """Generate a new API key. Requires username & API Key."""
#     global API_KEY  # ✅ Ensure we store the new key
#
#     payload = {"username": USERNAME}
#     response = requests.post(f"{BASE_URL}/generate-api-key", headers=HEADERS, json=payload)
#
#     if response.status_code == 200:
#         data = response.json()
#         new_api_key = data.get("new_api_key")
#         if new_api_key:
#             API_KEY = new_api_key  # ✅ Store new API key
#             print(f"✅ New API Key Generated: {API_KEY}")
#         else:
#             print("⚠️ Failed to retrieve a new API key.")
#     else:
#         print(f"❌ Failed to generate API key: {response.json()}")
#
# if __name__ == "__main__":
#     print("🚀 Generating New API Key...")
#     generate_api_key()
#


# import requests
# import json
#
# # Base URL for your API
# BASE_URL = "https://finceptapi.share.zrok.io"
#
# def register_user(username: str, email: str, password: str):
#     """
#     Call the /register endpoint to create a new user.
#     """
#     url = f"{BASE_URL}/register"
#     payload = {
#         "username": username,
#         "email": email,
#         "password": password
#     }
#     response = requests.post(url, json=payload)
#     print("=== Register Response ===")
#     print("Status Code:", response.status_code)
#     try:
#         print("Response JSON:", json.dumps(response.json(), indent=2))
#     except Exception as e:
#         print("Response Text:", response.text)
#     return response
#
# def verify_otp(email: str, otp: int):
#     """
#     Call the /verify-otp endpoint to verify the user using the OTP provided by the user.
#     """
#     url = f"{BASE_URL}/verify-otp"
#     payload = {
#         "email": email,
#         "otp": otp
#     }
#     response = requests.post(url, json=payload)
#     print("\n=== Verify OTP Response ===")
#     print("Status Code:", response.status_code)
#     try:
#         print("Response JSON:", json.dumps(response.json(), indent=2))
#     except Exception as e:
#         print("Response Text:", response.text)
#     return response
#
# def login_user(email: str, password: str):
#     """
#     Call the /login endpoint to authenticate the user.
#     """
#     url = f"{BASE_URL}/login"
#     payload = {
#         "email": email,
#         "password": password
#     }
#     response = requests.post(url, json=payload)
#     print("\n=== Login Response ===")
#     print("Status Code:", response.status_code)
#     try:
#         print("Response JSON:", json.dumps(response.json(), indent=2))
#     except Exception as e:
#         print("Response Text:", response.text)
#     return response
#
#
# if __name__ == "__main__":
#     # Define test user details
#     username = "testuser122"
#     email = "nikultilak@gmail.com"
#     password = "TestPassword123"
#
#     # 1. Register the user
#     register_resp = register_user(username, email, password)
#
#     # 2. Prompt the user to enter the OTP sent via email
#     otp_input = input("Please enter the OTP sent to your email: ")
#     try:
#         otp = int(otp_input)
#     except ValueError:
#         print("Invalid OTP format. OTP should be numeric.")
#         exit(1)
#
#     # 3. Verify the OTP
#     verify_resp = verify_otp(email, otp)
#
#     # 4. Log in the user
#     login_resp = login_user(email, password)


# import requests
# from datetime import datetime
#
# # Base URL of your hosted API
# BASE_URL = "https://finceptapi.share.zrok.io"
#
# # Endpoints
# REGISTER_ENDPOINT = f"{BASE_URL}/register"
# VERIFY_OTP_ENDPOINT = f"{BASE_URL}/verify-otp"
# DATABASES_ENDPOINT = f"{BASE_URL}/databases"
# SUBSCRIBE_ENDPOINT = f"{BASE_URL}/subscribe/IndiaPriceData"
# TABLES_ENDPOINT = f"{BASE_URL}/IndiaPriceData/tables"
#
# # Generate unique username
# timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# SAMPLE_USER = {
#     "username": f"testuser_{timestamp}",
#     "email": f"testuser_{timestamp}@example.com",
#     "password": "securepassword123"
# }
#
# SAMPLE_OTP = 111111  # Fixed OTP for testing
#
#
# def register_user():
#     """Test user registration."""
#     print(f"Registering user: {SAMPLE_USER['username']}")
#     response = requests.post(REGISTER_ENDPOINT, json=SAMPLE_USER)
#     print("Register Response Status Code:", response.status_code)
#     print("Register Response Text:", response.text)
#     try:
#         return response.json()
#     except requests.exceptions.JSONDecodeError:
#         print("Failed to parse JSON response")
#         return {}
#
#
# def verify_otp():
#     """Test OTP verification."""
#     payload = {"email": SAMPLE_USER["email"], "otp": SAMPLE_OTP}
#     response = requests.post(VERIFY_OTP_ENDPOINT, json=payload)
#     print("Verify OTP Response Status Code:", response.status_code)
#     print("Verify OTP Response Text:", response.text)
#     try:
#         return response.json()
#     except requests.exceptions.JSONDecodeError:
#         print("Failed to parse JSON response")
#         return {}
#
#
# def get_databases(api_key):
#     """Test fetching list of databases."""
#     headers = {"X-API-Key": api_key}
#     response = requests.get(DATABASES_ENDPOINT, headers=headers)
#     print("Databases Response Status Code:", response.status_code)
#     try:
#         print("Databases Response:", response.json())
#     except requests.exceptions.JSONDecodeError:
#         print("Failed to parse JSON response")
#
#
# def subscribe_database(api_key):
#     """Test subscribing to a database."""
#     headers = {"X-API-Key": api_key}
#     response = requests.post(SUBSCRIBE_ENDPOINT, headers=headers)
#     print("Subscribe Response Status Code:", response.status_code)
#     print("Subscribe Response Text:", response.text)
#     try:
#         return response.json()
#     except requests.exceptions.JSONDecodeError:
#         print("Failed to parse JSON response")
#         return {}
#
#
# def get_tables(api_key):
#     """Test fetching list of tables in a subscribed database."""
#     headers = {"X-API-Key": api_key}
#     response = requests.get(TABLES_ENDPOINT, headers=headers)
#     print("Tables Response Status Code:", response.status_code)
#     try:
#         print("Tables Response:", response.json())
#     except requests.exceptions.JSONDecodeError:
#         print("Failed to parse JSON response")
#
#
# def run_ip_limiting_test(ip, headers=None):
#     """
#     Simulates requests to test IP-based rate limits.
#     """
#     print(f"\nTesting rate limiting for IP: {ip}")
#     for i in range(12):  # Test with 12 requests to exceed both limits
#         response = requests.get(DATABASES_ENDPOINT, headers=headers)
#         print(f"Request {i + 1} - Status Code: {response.status_code}")
#         if response.status_code == 429:
#             print("Rate limit exceeded!")
#             break
#
#
# if __name__ == "__main__":
#     # Step 1: Register a user
#     registration_data = register_user()
#     if "api_key" in registration_data:
#         api_key = registration_data["api_key"]
#         print(f"API Key: {api_key}")
#
#         # Step 2: Verify OTP
#         verify_otp_response = verify_otp()
#         if verify_otp_response.get("message") == "Email verified successfully!":
#             print("OTP verification successful.")
#
#             # Step 3: Get list of databases
#             get_databases(api_key)
#
#             # Step 4: Subscribe to a database
#             subscribe_response = subscribe_database(api_key)
#             if subscribe_response.get("message"):
#                 print("Subscription successful.")
#
#                 # Step 5: Fetch tables in a subscribed database
#                 get_tables(api_key)
#
#             # Step 6: Test fetching tables in a non-subscribed database
#             print("\nTesting non-subscribed database access...")
#             headers = {"X-API-Key": api_key}
#             response = requests.get(f"{BASE_URL}/metaData/tables", headers=headers)
#             print("Non-Subscribed Database Response Status Code:", response.status_code)
#             print("Non-Subscribed Database Response:", response.json())
#
#             # Step 7: Test rate limits for IP
#             run_ip_limiting_test("unregistered_ip")  # Unregistered IP test
#             run_ip_limiting_test("registered_ip", headers=headers)  # Registered IP test
#         else:
#             print("OTP verification failed.")
#     else:
#         print("Registration failed. Cannot proceed with tests.")
#
#
# # import requests
# #
# # # Base URL of the API (replace with your actual deployed endpoint)
# # BASE_URL = "https://finceptapi.share.zrok.io"
# #
# # # Endpoints
# # SUBSCRIBE_ENDPOINT = f"{BASE_URL}/subscribe"
# # TABLES_ENDPOINT = f"{BASE_URL}/{{database_name}}/tables"
# # DATA_ENDPOINT = f"{BASE_URL}/{{database_name}}/{{table_name}}/data"
# #
# # # Replace these with valid names and a valid API key
# # DATABASE_NAME = "IndiaPriceData"
# # TABLE_NAME = "stock_rites_price_data_nse"  # Replace with an actual table from your DB
# # API_KEY = "7b186f32-d353-4754-a30f-d382e4188684"
# #
# #
# # def subscribe_to_database(api_key, database_name):
# #     """
# #     Subscribes to a specific database.
# #     """
# #     url = f"{SUBSCRIBE_ENDPOINT}/{database_name}"
# #     headers = {"X-API-Key": api_key}
# #
# #     try:
# #         response = requests.post(url, headers=headers)
# #         print("Subscribe Response Status Code:", response.status_code)
# #         print("Subscribe Response Text:", response.text)
# #         return response.status_code, (
# #             response.json() if response.status_code == 200 else response.text
# #         )
# #     except requests.exceptions.RequestException as e:
# #         print("An error occurred while making the request:", e)
# #         return None, None
# #
# #
# # def get_tables_in_database(api_key, database_name):
# #     """
# #     Fetches the list of tables in the subscribed database.
# #     """
# #     url = TABLES_ENDPOINT.format(database_name=database_name)
# #     headers = {"X-API-Key": api_key}
# #
# #     try:
# #         response = requests.get(url, headers=headers)
# #         print("Tables Response Status Code:", response.status_code)
# #         print("Tables Response Text:", response.text)
# #         return response.status_code, (
# #             response.json() if response.status_code == 200 else response.text
# #         )
# #     except requests.exceptions.RequestException as e:
# #         print("An error occurred while making the request:", e)
# #         return None, None
# #
# #
# # def get_table_data(api_key, database_name, table_name, page=1, limit=15):
# #     """
# #     Fetch paginated data from a specific table in the database.
# #     """
# #     url = DATA_ENDPOINT.format(database_name=database_name, table_name=table_name)
# #     headers = {"X-API-Key": api_key}
# #     params = {"page": page, "limit": limit}  # Send as query parameters
# #
# #     try:
# #         response = requests.get(url, headers=headers, params=params)
# #         print("Data Endpoint Response Status Code:", response.status_code)
# #         print("Data Endpoint Response Text:", response.text)
# #         return response.status_code, (
# #             response.json() if response.status_code == 200 else response.text
# #         )
# #     except requests.exceptions.RequestException as e:
# #         print("An error occurred while making the request:", e)
# #         return None, None
# #
# #
# # if __name__ == "__main__":
# #     # 1) Subscribe to the database
# #     print(f"Subscribing to database: {DATABASE_NAME}")
# #     subscribe_status, subscribe_response = subscribe_to_database(API_KEY, DATABASE_NAME)
# #
# #     if subscribe_status == 200:
# #         print(f"Successfully subscribed to {DATABASE_NAME}. Now fetching tables...")
# #     elif subscribe_status == 400 and "Already subscribed" in str(subscribe_response):
# #         print(f"Already subscribed to {DATABASE_NAME}. Proceeding to fetch tables...")
# #     else:
# #         print("Error subscribing to the database:", subscribe_response)
# #         exit()
# #
# #     # 2) Fetch tables in the subscribed database
# #     tables_status, tables_response = get_tables_in_database(API_KEY, DATABASE_NAME)
# #     if tables_status == 200:
# #         print("Tables in database:", tables_response.get("tables", []))
# #     else:
# #         print("Error fetching tables:", tables_response)
# #         exit()
# #
# #     # 3) Now fetch data from a specific table with pagination
# #     print(f"\nFetching data from table: {TABLE_NAME}")
# #     data_status, data_response = get_table_data(API_KEY, DATABASE_NAME, TABLE_NAME, page=1, limit=15)
# #
# #     if data_status == 200:
# #         print("Data fetched successfully. Here is a preview:")
# #         print(data_response)
# #     else:
# #         print("Error fetching data:", data_response)
