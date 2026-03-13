import requests

def get_users():

    url = "https://jsonplaceholder.typicode.com/users"

    r = requests.get(url)

    return r.json()