import requests
import json

HOST_API = 'http://127.0.0.1:8000/api/'
chat_id = 134203883
TOKEN = '994f61ba4bd900112ae616ef66c09fe086576b2e'


# Примеры работы для бота (без авторизации)

# С аргументов выводит только текущего пользователя, без - всех
def get_api_users_list(chat_id: int = None) -> list:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
    if chat_id is not None:
        data = {
            'chat_id': chat_id,
        }
    else:
        data = {}
    users_data = requests.get(HOST_API + 'apiusers/', json=data, headers=headers)
    json_users_data = users_data.json()
    return json_users_data


# С аргументом - только операции пользователя, без - все
def get_operations(chat_id: int = None) -> list:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
    if chat_id is not None:
        data = {
            'chat_id': chat_id,
        }
    else:
        data = {}
    users_data = requests.get(HOST_API + 'operations/', json=data, headers=headers)
    json_users_data = users_data.json()
    return json_users_data


# создание операции. Если указан chat_id -> user игнорируется
def add_operations(title: str, description: str, amount: float, category: int, user: int = 1,
                   chat_id: int = None) -> dict:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
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
    response = requests.post(HOST_API + 'operations/', json=data, headers=headers)
    json_responce = response.json()
    return json_responce


# С аргументом - только операции пользователя, без - все
def get_categories() -> list:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
    users_data = requests.get(HOST_API + 'categories/', headers=headers)
    json_users_data = users_data.json()
    return json_users_data


def add_categories(name: str, cat_type: str = 'EXP') -> dict:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
    data = {
        'name': name,
        'cat_type': cat_type,
    }
    users_data = requests.post(HOST_API + 'categories/', json=data, headers=headers)
    json_users_data = users_data.json()
    return json_users_data


def del_categories(id: int) -> int:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
    users_data = requests.delete(HOST_API + 'categories/' + str(id) + '/', headers=headers)
    # json_users_data = users_data.json()
    return users_data.status_code


def get_balance(chat_id: int) -> dict:
    headers = {
        'Authorization': 'Token ' + TOKEN,
    }
    data = {
        'chat_id': chat_id,
    }
    users_data = requests.get(HOST_API + 'operations/balance/', headers=headers, json=data)
    json_users_data = users_data.json()
    return json_users_data


# use only if token doesn't exist
# !!! NOT 4 BOT !!!
def create_jrf_token(username: str) -> str:
    from rest_framework.authtoken.models import Token
    from main.models import AdvUser
    user = AdvUser.objects.get(username=username)
    token = Token.objects.create(user=user)
    return token.key


# get JWT token. Работает, но пока не используется.
def get_token(username: str, password: str) -> dict:
    data = {
        'username': username,
        'password': password,
    }
    # if is_user_exist(chat_id):
    #     # return requests.post(HOST_API + 'token/', json=data).json()['access']
    #     return requests.post(HOST_API + 'token/', json=data).json()
    # return 'User not registered'
    return requests.post(HOST_API + 'token/', json=data).json()


# Старые примеры. МНогое уже не работает.

# def get_token(chat_id: int) -> str:
#     data = {
#         'username': chat_id,
#         'password': chat_id,
#     }
#     if is_user_exist(chat_id):
#         # return requests.post(HOST_API + 'token/', json=data).json()['access']
#         return requests.post(HOST_API + 'token/', json=data).json()
#     return 'User not registered'


def get_users_list(chat_id: int) -> list:
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
        requests.post(HOST_API + 'users/register/', json=data)


def is_user_exist(chat_id: int) -> bool:
    data = {
        'username': chat_id,
        'password': chat_id,
    }
    if requests.post(HOST_API + 'token/', json=data).status_code == 200:
        return True
    return False
