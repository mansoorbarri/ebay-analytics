import requests

url = "http://127.0.0.1:8000/auth/register"

payload = {
    "email": "admin@example.com",
    "password": "admin123"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())