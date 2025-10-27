import requests

url = "https://backstage.taboola.com/backstage/oauth/token"

payload = {
    "client_id": "0d90885f1a9e4313ac03b6e004143c08",
    "client_secret": "00bd96b8478c4e5b84eda0d464e4cb3f",
    "grant_type": "client_credentials"
}
headers = {"content-type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

print(response.text)

import requests

url = "https://backstage.taboola.com/backstage/api/1.0/users/current/account"

response = requests.get(url)

print(response.text)