import requests

def get_user_id(event):
  token = event['headers']['authorization']
  response = requests.get('https://login.yandex.ru/info', headers={'authorization': token})
  json_response = response.json() 
  return json_response['id']