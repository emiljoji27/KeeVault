import requests
from getpass import getpass

endpoint="http://localhost:8000/api-token-auth/"

data={
    "username":"Whatsapp",
    "password":"somepass123#"
}

auth_token=requests.post(endpoint,json=data)
print(auth_token.json())


endpoint="http://localhost:8000/api/50/delete/"
token=auth_token.json().get('token')
headers={
    "Authorization":f'tester {token}'
}
data={
    "name":"Snapchat",
    "login_username":"email123@email.com",
    "login_password":"somepass123#",
    "login_url":"www.snapchat.com",
}

get_response=requests.delete(endpoint,headers=headers,json=data)
print(get_response.status_code)