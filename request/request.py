import requests
import json

HOST_API = 'http://127.0.0.1:8000/api/'
chat_id = 134203883


# Примеры работы для бота (без авторизации)

# С аргументов выводит только текущего пользователя, без - всех
def get_api_users_list(chat_id: int = None) -> dict:
    if chat_id is not None:
        data = {
            'chat_id': chat_id,
        }
    else:
        data = {}
    users_data = requests.get(HOST_API + 'apiusers/', data=data)
    json_users_data = users_data.json()
    return json_users_data


# С аргументом - только операции пользователя, без - все
def get_operations(chat_id: int = None) -> dict:
    if chat_id is not None:
        data = {
            'chat_id': chat_id,
        }
    else:
        data = {}
    users_data = requests.get(HOST_API + 'operations/', data=data)
    json_users_data = users_data.json()
    return json_users_data


# создание операции. Если указан chat_id -> user игнорируется
def add_operations(title: str, description: str, amount: float, user: int, category: int, chat_id: int = None) -> dict:
    if chat_id is not None:
        data = {
            "title": title,
            "description": description,
            "amount": amount,
            "category": category,
            "chat_id": chat_id,
        }
    else:
        data = {
            "title": title,
            "description": description,
            "amount": amount,
            "user": user,
            "category": category,
        }
    # print(data)
    # data = json.dump(data)
    print(data)
    response = requests.post(HOST_API + 'operations/', data=data)
    print(response)
    json_responce = response.json()
    return json_responce


# Старые примеры. МНогое уже не работает.

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
