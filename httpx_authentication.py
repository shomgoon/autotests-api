import httpx
from sqlalchemy import except_

payload = {
    "email": "user@example.com",
    "password": "string"
}
try:
    response = httpx.post('http://localhost:8000/api/v1/authentication/login')
    print(response.json())
    print(response.status_code)
except:
