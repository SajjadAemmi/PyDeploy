import requests

url = "http://127.0.0.1:8080"

data={}
headers = {}

response = requests.request("GET", url, headers=headers, data=data)

print(response.text)
