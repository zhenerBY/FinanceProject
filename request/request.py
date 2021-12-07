import requests

HOST_API = 'http://127.0.0.1:8000/api/'
chat_id = 134203883


def get_token(chat_id: int) -> str:
    data = {
        'username': chat_id,
        'password': chat_id,
    }
    if is_user_exist(chat_id):
        return requests.post(HOST_API + 'token/', data=data).json()['access']
    return 'User not registered'


def get_users_list(chat_id: int) -> dict:
    headers = {
        'Authorization': 'Bearer ' + get_token(chat_id),
    }
    users_data = requests.get(HOST_API + 'users/', headers=headers)
    json_users_data = users_data.json()
    return json_users_data


def user_registration(chat_id: int) -> None:
    if not is_user_exist(chat_id):
        data = {
            'username': chat_id,
            'password': chat_id,
        }
        requests.post(HOST_API + 'users/register/', data=data)


def is_user_exist(chat_id: int) -> bool:
    data = {
        'username': chat_id,
        'password': chat_id,
    }
    if requests.post(HOST_API + 'token/', data=data).status_code == 200:
        return True
    return False
