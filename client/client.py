import requests

def create_user(url, username, password):
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    return response

if __name__ == '__main__':
    # URL for your create user endpoint
    url = 'http://127.0.0.1:5000/users'

    # User details
    username = 'newuser'
    password = 'password123'

    # Send request to create a new user
    response = create_user(url, username, password)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response:', response)
