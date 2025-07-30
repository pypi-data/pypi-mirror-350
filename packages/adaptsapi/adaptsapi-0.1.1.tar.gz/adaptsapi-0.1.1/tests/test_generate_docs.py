from adapts_api.generate_docs import post, PayloadValidationError

payload = {
    "user_id": "user-001",
    "email_address": "user@example.com",
    "user_name": "johndoe",
    "repo_object": {
        "repo_name": "adapts_client",
        "repo_source": "github",
        "repo_url": "https://github.com/adapts-ai/adapts_client",
        "repo_branch": "main",
    },
}

try:
    resp = post("https://httpbin.org/post", "my-token-xyz", payload)
    resp.raise_for_status()
    print(resp.json())
except PayloadValidationError as e:
    print("Invalid payload:", e)
except requests.RequestException as e:
    print("Request failed:", e)
