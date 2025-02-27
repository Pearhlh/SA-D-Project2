import requests

url = "http://localhost:8000/api/auth/verify-token/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNjUwODI0LCJqdGkiOiJhODRmNzg5ZjFlYmM0Y2ViOTYzNTA2NGY4ZDJhZTAzMyIsInVzZXJfaWQiOjF9.L4v6kGFBOumPMAJz53TSCja1r6liiMupX0R6QwqryWM"
}

response = requests.post(url, headers=headers)
print(response.status_code)
print(response.json())  # In ra nội dung phản hồi JSON
