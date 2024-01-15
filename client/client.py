import requests

def create_user(url, username, password):
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response

def get_users(url):
    response = requests.get(url)
    return response

def update_user(url, user_id, username=None, password=None):
    data = {}
    if username:
        data['username'] = username
    if password:
        data['password'] = password

    response = requests.put(f'{url}/{user_id}', json=data)
    return response


def get_access_token(url, username, password):
    response = requests.post(url, json={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None

def access_protected_route(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    return requests.get(url, headers=headers)

if __name__ == '__main__':
    # URL for your create user endpoint
    url = 'http://127.0.0.1:5000/users'
    login_url = 'http://127.0.0.1:5000/login'

    # User details
    username = 'Allan'
    password = 'wwer63453535'
    token = get_access_token(login_url, username, password)

    if token:
        print("Access Token:", token)
    # Send request to create a new user
    # response = create_user(url, username, password)
    # response = get_users(url)
    # breakpoint()

    # Print the response from the server
    # print('Status Code:', response.status_code)
    # print('Response:', response)
