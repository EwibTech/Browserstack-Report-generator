import requests
import json

USERNAME = "abhyudayapathak_WTr9zi"
ACCESS_KEY = "ALysQQQwMwyiyJkKwouR"
BASE_URL = "https://test-management.browserstack.com/api/v2"
auth = (USERNAME, ACCESS_KEY)

# Waggle project ID from the screenshot URL
project_id = "PR-1091"  
test_run_id = "TR-294459"

print(f"Fetching test run details for Waggle project...")
print(f"Project ID: {project_id}")
print(f"Test Run ID: {test_run_id}\n")

url = f"{BASE_URL}/projects/{project_id}/test-runs/{test_run_id}"
print(f"URL: {url}\n")

response = requests.get(url, auth=auth)
response.raise_for_status()

data = response.json()
print("Full API Response:")
print(json.dumps(data, indent=2))
